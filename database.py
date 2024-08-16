import sqlite3
import json
import os
from PyQt6.QtWidgets import QFileDialog

class Database:
    def __init__(self, browsers):
        self.browsers = browsers
        self.conn = None
        self.cursor = None
        self.db_path = None

    def connect(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def save_form_data(self):
        self.db_path = self.save_data_dialog()
        if self.db_path:
            self.remove_existing_db(self.db_path)
            self.connect(self.db_path)
            js_code = '''
                (function() {
                    const inputs = document.querySelectorAll('input, textarea, select');
                    const dados = {};

                    inputs.forEach(input => {
                        const name = input.id || input.name;
                        if (name) {
                            if (input.type === 'checkbox') {
                                dados[name] = input.checked ? 'checked' : 'unchecked';
                            } else if (input.type === 'radio') {
                                if (input.checked) {
                                    dados[name] = input.value;
                                }
                            } else {
                                dados[name] = input.value;
                            }
                        }
                    });

                    return JSON.stringify(dados);
                })();
            '''
            self.pending_saves = len(self.browsers)
            for idx, browser in enumerate(self.browsers):
                browser.page().runJavaScript(js_code, lambda result, idx=idx: self.process_save_results(result, f"form{idx+1}"))

    def process_save_results(self, result, table_name):
        self.save_form_data_to_db(result, table_name)
        self.pending_saves -= 1
        if self.pending_saves == 0:
            self.save_database()
            self.export_to_txt()  # Exporta para TXT após salvar no banco de dados

    def create_table(self, table_name, fields):
        sanitized_fields = [f.replace('-', '_') for f in fields]
        field_definitions = ", ".join([f"{field} TEXT" for field in sanitized_fields])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})"
        self.cursor.execute(create_table_query)

    def insert_data(self, table_name, data):
        sanitized_data = {k.replace('-', '_'): v for k, v in data.items()}
        placeholders = ", ".join(["?" for _ in sanitized_data.keys()])
        insert_query = f"INSERT INTO {table_name} ({', '.join(sanitized_data.keys())}) VALUES ({placeholders})"
        self.cursor.execute(insert_query, list(sanitized_data.values()))
        self.conn.commit()

    def save_form_data_to_db(self, json_data, table_name):
        data = json.loads(json_data)
        self.create_table(table_name, data.keys())
        self.insert_data(table_name, data)

    def save_database(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def save_data_dialog(self):
        options = QFileDialog.Option.DontUseNativeDialog  # Exemplos de opções: Pode ser None ou outra combinação de opções
        file_name, _ = QFileDialog.getSaveFileName(None, "Salvar Banco de Dados", "", "Database Files (*.db)", options=options)
       
        # Adicionar extensão .db se não estiver presente
        if file_name and not file_name.endswith('.db'):
            file_name += '.db'
        return file_name if file_name else None

    def remove_existing_db(self, db_path):
        if os.path.exists(db_path):
            os.remove(db_path)

    def export_to_txt(self):
        if not self.db_path:
            print("No database path set. Save the data first.")
            return
        
        # Gerar o caminho do arquivo de texto no mesmo diretório do banco de dados
        output_path = os.path.splitext(self.db_path)[0] + '.txt'

        self.connect(self.db_path)
        with open(output_path, 'w') as file:
            for table_name in ["form1", "form2", "form3"]:
                file.write(f"Table: {table_name}\n")
                try:
                    self.cursor.execute(f"SELECT * FROM {table_name}")
                    rows = self.cursor.fetchall()
                    for row in rows:
                        file.write(f"{row}\n")
                except sqlite3.OperationalError:
                    file.write("No data found.\n")
                file.write("\n")
        self.conn.close()
        print(f"Dados exportados para {output_path}")
