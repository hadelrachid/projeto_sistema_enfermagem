from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton, QTabWidget, QMainWindow, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer
import os
import tempfile
from PyPDF2 import PdfMerger

class PrintWindow(QMainWindow):
    def __init__(self, print_pages, folder_path, browsers_list): # Método construtor inicializador da classe
        super().__init__()                        # Chama o inicializador da classe pai QMainWindow
        
        self.print_pages = print_pages # Lista de QWebEngineView
        self.folder_path = folder_path
        self.browsers_list = browsers_list
        self.print_pages_list = []
        
        self.setWindowTitle("Print Preview") # Define o título da janela
        self.setGeometry(100, 100, 800, 600) # Define a posição e o tamanho da janela
        
        self.tab_widget = QTabWidget() # Cria um widget de abas
        self.setCentralWidget(self.tab_widget)
        
        # Chama a função load_print_pages() para carregar os modelos de impressão
        # nas guias correspondentes
        self.load_print_pages()
        
        # Layout principal que incluirá o layout das abas e os botões
        main_layout = QVBoxLayout()
        
        # Adiciona o widget de abas ao layout principal
        main_layout.addWidget(self.tab_widget)
        
        # Layout horizontal para os botões
        button_layout = QHBoxLayout()
        
        self.load_button_styles()
        
        # Cria botões
        self.pdf_button = QPushButton('Salvar como PDF', self)   # Cria o botão para salvar em PDF
        # self.print_button = QPushButton('Impressora', self) # Cria o botão para Impressora
        
        # Adiciona os botões ao layout horizontal
        button_layout.addWidget(self.pdf_button)    # Adciona o botão 'PDF'
        # button_layout.addWidget(self.print_button)  # Adciona o botão 'Imprimir'
        
        # Adiciona o layout dos botões ao layout principal
        main_layout.addLayout(button_layout)

        # Cria um widget central para conter o layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Define o widget central na janela principal
        self.setCentralWidget(central_widget)  
        
        self.JavaScript_Browsers()
        
        # ################################### Eventos para botões ###################################
        
        self.pdf_button.clicked.connect(self.save_as_pdf)
        # self.print_button.clicked.connect(self.printer)
        
        # ###########################################################################################
        
        
    def load_print_pages(self):
        count = 0 # controla o índice do da guia ou aba (Tab)
        for page in self.print_pages:
            view = QWebEngineView()
            file_path = os.path.join(os.getcwd(), self.folder_path, page) 
            view.setUrl(QUrl.fromLocalFile(file_path))
            self.tab_widget.addTab(view, page)
            self.tab_widget.setTabText(count, f"Formulario {count + 1}")
            count += 1
            self.print_pages_list.append(view)
            
    # Essa função tem como objetivo abrir e ler o arquivo button_styles.css
    # da pasta _css para estilizar os botões
    def load_button_styles(self):
        try:
            with open("_css/button_styles.css", "r") as file: # Abrir como arquivo
                button_styles_css = file.read()               # Ler o arquivo
                self.setStyleSheet(button_styles_css)         # Aplicar os estilos
        except Exception as e:
            print(f"Erro ao carregar o arquivo CSS: {e}")
            

    def save_as_pdf(self):
        pdf_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")

        if pdf_path:
            self.temp_files = []
            self.current_tab = 0
            self.pdf_path = pdf_path
            self.print_next_tab_to_pdf()

    def print_next_tab_to_pdf(self):
        if self.current_tab < self.tab_widget.count():
            tab = self.tab_widget.widget(self.current_tab)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            self.temp_files.append(temp_file.name)
            tab.page().printToPdf(lambda data: self.on_pdf_printed(data, temp_file.name))
        else:
            self.combine_pdfs()

    def on_pdf_printed(self, data, file_path):
        with open(file_path, 'wb') as f:
            f.write(data.data())
        self.current_tab += 1
        QTimer.singleShot(1000, self.print_next_tab_to_pdf)

    def combine_pdfs(self):
        merger = PdfMerger()

        for pdf in self.temp_files:
            merger.append(pdf)

        merger.write(self.pdf_path)
        merger.close()

        for pdf in self.temp_files:
            os.remove(pdf)

        print(f"PDF saved to {self.pdf_path}")
        
    def JavaScript_Browsers(self):
        
        print(f"Quantidade de navegadores: {len(self.browsers_list)}")
        print(f"Quantidade de paginas: {len(self.print_pages)}")

        self.browsers_list[0].page().runJavaScript("saveFormData()", self.handle_result)
        self.print_pages_list[0].page().runJavaScript("loadFormData()", self.handle_result)
        
        self.browsers_list[1].page().runJavaScript("saveFormData()", self.handle_result)
        self.print_pages_list[1].page().runJavaScript("loadFormData()", self.handle_result)
        
    def handle_result(self, result):
        # Imprimir ou lidar com o resultado da execução do JavaScript
        if result:
            print("Resultado da execução do JavaScript:", result)
        else:
            print("Nenhum resultado retornado ou erro.")