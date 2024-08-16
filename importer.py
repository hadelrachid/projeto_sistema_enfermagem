import sqlite3
from PyQt6.QtWidgets import QFileDialog, QMessageBox

class Importer:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_db(self, db_path):
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Failed to connect to database: {e}")

    def close_db(self):
        if self.connection:
            self.connection.close()

    def fetch_all_data(self):
        data = {}
        for table_name in ["form1", "form2", "form3"]:
            try:
                self.cursor.execute(f"SELECT * FROM {table_name}")
                rows = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                data[table_name] = [dict(zip(columns, row)) for row in rows]
            except sqlite3.OperationalError:
                data[table_name] = []
        return data
    
    
    def generate_js_script(self, table_name, data):
        js_code = ""
        if table_name == "form2":
            row_count = int(data[0].get('rowCountInput', 0))  # Obtenha o valor de rowCountInput
            js_code += f"document.getElementById('rowCountInput').value = {row_count};\n"
            for _ in range(row_count - 1):  # Adicione linhas extras conforme necessário
                js_code += "addRow();\n"
            js_code += "updateRowIds();\n"

        for entry in data:
            for key, value in entry.items():
                if key != 'rowCountInput':  # Ignorar rowCountInput ao definir valores
                    js_code += f"""
                    var element = document.getElementById('{key}');
                    if (element) {{
                        if (element.tagName === 'SELECT') {{
                            element.value = '{value}';
                        }} else if (element.type === 'checkbox') {{
                            element.checked = {'true' if value == 'checked' else 'false'};
                        }} else if (element.type === 'radio') {{
                            var radios = document.getElementsByName(element.name);
                            for (var i = 0; i < radios.length; i++) {{
                                if (radios[i].value === '{value}') {{
                                    radios[i].checked = true;
                                }}
                            }}
                        }} else {{
                            element.value = '{value}';
                        }}
                    }}
                    """
        return js_code

    def import_data_to_forms(self, browsers):
        file_dialog = QFileDialog()
        db_path, _ = file_dialog.getOpenFileName(None, "Selecionar Banco de Dados", "", "Database Files (*.db);;Todos os Arquivos (*)")
        if db_path:
            self.connect_db(db_path)
            all_data = self.fetch_all_data()
            for idx, browser in enumerate(browsers):
                table_name = f"form{idx+1}"
                if table_name in all_data:
                    js_code = self.generate_js_script(table_name, all_data[table_name])
                    print(js_code)  # Para depuração, imprimir o código JavaScript gerado
                    browser.page().runJavaScript(js_code)
            self.close_db()
            QMessageBox.information(None, "Success", "Data imported successfully!")
