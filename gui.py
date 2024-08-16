# Importa as classes indispensáveis para a construção visual dos componentes GUI do PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QLocale

from database import Database # importa a classe Database do arquivo database.py
from importer import Importer # importa a classe Importer do arquivo importer.py
from print import PrintWindow # importa a classe PrintWindow do arquivo print.py
from update import Update     # importa a classe Update do arquivo update.py
import os

class GUI(QMainWindow):             # Define a classe principal da janela, herdando de QMainWindow
    def __init__(self, app):        # Método construtor inicializador da classe
        super().__init__()          # Chama o inicializador da classe pai QMainWindow
        self.app = app
        
    # ########################### # Definição da Aparência da Janela GUI # ###########################
        
        self.setWindowTitle('SISTEMATIZAÇÃO DA ASSISTÊNCIA DE ENFERMAGEM') # Define o título da janela
        self.setGeometry(100, 100, 800, 600) # Define a posição e o tamanho da janela
        
        # Definir localidade para português do Brasil
        self.locale = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
        QLocale.setDefault(self.locale)
        
        self.initUI()         # Chama o método que inicializa a interface do usuário

    def initUI(self):         # Método que inicializa a interface do usuário
        
        tab_widget = QTabWidget()  # Cria um widget de abas
        self.setCentralWidget(tab_widget)
        
        tab1 = QWidget()  # Cria um widget para a primeira aba
        tab2 = QWidget()  # Cria um widget para a segunda aba
        tab3 = QWidget()  # Cria um widget para a terceira aba
        
        tab_widget.addTab(tab1, "Formulário 1")  # Adiciona a primeira aba ao widget de abas
        tab_widget.addTab(tab2, "Formulário 2")  # Adiciona a segunda aba ao widget de abas
        tab_widget.addTab(tab3, "Formulário 3")  # Adiciona a terceira aba ao widget de abas
        
        layout1 = QVBoxLayout()  # Cria um layout vertical para a primeira aba
        layout2 = QVBoxLayout()  # Cria um layout vertical para a segunda aba
        layout3 = QVBoxLayout()  # Cria um layout vertical para a terceira aba
        
        browser1 = QWebEngineView()  # Cria um widget de visualização web para a primeira aba
        browser2 = QWebEngineView()  # Cria um widget de visualização web para a segunda aba
        browser3 = QWebEngineView()  # Cria um widget de visualização web para a terceira aba

        # Ajusta o caminho para os arquivos HTML
        html_path1 = os.path.join(os.getcwd(), '_pages', 'form1.html') # Arquivo form1.html na pasta _pages do projeto
        html_path2 = os.path.join(os.getcwd(), '_pages', 'form2.html') # Arquivo form2.html na pasta _pages do projeto
        html_path3 = os.path.join(os.getcwd(), '_pages', 'form3.html') # Arquivo form3.html na pasta _pages do projeto
        
        # Adicionar os visualizadores widgets
        layout1.addWidget(browser1)  # Adiciona o widget de visualização web ao layout da primeira aba
        layout2.addWidget(browser2)  # Adiciona o widget de visualização web ao layout da segunda aba
        layout3.addWidget(browser3)  # Adiciona o widget de visualização web ao layout da terceira aba
        
        # Definir os Layouts
        tab1.setLayout(layout1)  # Define o layout da primeira aba
        tab2.setLayout(layout2)  # Define o layout da segunda aba
        tab3.setLayout(layout3)  # Define o layout da terceira aba
        
        # Layout principal que incluirá o layout das abas e os botões
        main_layout = QVBoxLayout()

        # Adiciona o widget de abas ao layout principal
        main_layout.addWidget(tab_widget)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()
              
        # Chama a função para carregar o estilo dos botões a partir do arquivo CSS na pasta _css
        # Esta função load_button_styles() foi definida a seguir
        self.load_button_styles()
        
        # Cria botões
        new_button = QPushButton('Novo', self)         # Cria o botão para cadastrar um novo usuário   
        save_button = QPushButton('Salvar', self)      # Cria o botão para salvar os dados 
        import_button = QPushButton('Importar', self)  # Cria o botão para importar os dados
        print_button = QPushButton('Imprimir', self)   # Cria o botão para imprimir os dados
        
        # Adiciona os botões ao layout horizontal
        button_layout.addWidget(new_button)    # Adciona o botão 'Novo'
        button_layout.addWidget(save_button)   # Adciona o botão 'Salvar'
        button_layout.addWidget(import_button) # Adciona o botão 'Importar'
        button_layout.addWidget(print_button)  # Adciona o botão 'Imprimir'
        
        # Adiciona o layout dos botões ao layout principal
        main_layout.addLayout(button_layout)

        # Cria um widget central para conter o layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Define o widget central na janela principal
        self.setCentralWidget(central_widget)    
        
        # Cria uma lista de Navegadores (browsers)
        self.browsers_list = [browser1, browser2, browser3]
        
        # Cria uma lista de Navegadores (browsers) temporários
        self.browsers_list_temp = [browser1, browser3]
        
        # Cria uma lista para guias ou tabs (para quando alternar entre browser1 e browser2)
        self.tabs_changed = [browser1, browser3]
        
    # ################################### Eventos das abas e botões ###################################
                
        # Quando alternar a aba 1 para a aba3 fazer uma atualização
        # do formulário 3 que pega do formulário 1 (chama a função tab_changed)
        tab_widget.currentChanged.connect(self.tab_changed) 
        
        # Quando os botões forem clicados
        new_button.clicked.connect(self.newUser)   # Conecta o clique do botão à função newUser
        save_button.clicked.connect(self.saveData) # Conecta o clique do botão à função saveData
        import_button.clicked.connect(self.importData)  # Conecta o clique do botão à função importData
        print_button.clicked.connect(self.printWindow) # Conecta o clque do botão à função printWindow
        
    # ###################### Carrega os Browsers por último para não haver delay ######################
    
        self.html_path = (html_path1, html_path2, html_path3) # Tuplas de atalhos dos arquivos html na pasta _pages
        self.browser = (browser1, browser2, browser3) # Tuplas de navegadores ou browsers
        self.load_html_pages() # Chama a função para carregar as páginas HTML nos browsers
            
    # ################################ Funções ou Métodos da Classe GUI ################################
        
    # Essa função tem como objetivo abrir e ler o arquivo button_styles.css
    # da pasta _css para estilizar os botões
    def load_button_styles(self):
        try:
            with open("_css/button_styles.css", "r") as file: # Abrir como arquivo
                button_styles_css = file.read()               # Ler o arquivo
                self.setStyleSheet(button_styles_css)         # Aplicar os estilos
        except Exception as e:
            print(f"Erro ao carregar o arquivo CSS: {e}")
            
    # Função caso a aba 3 seja clicada
    def tab_changed(self, index):
        if index == 2:                         # Índice da aba 3   # Carrega um a lista de browsers da aba 1 e aba 3
            update = Update(self.tabs_changed) # Instancia um objeto Update
            del update                         # Deleta o objeto update da memória
            
    # Função para carregar as páginas dos navegadores (browsers) nas Guias
    def load_html_pages(self):        
        for path, tab in zip(self.html_path, self.browser):
            tab.load(QUrl.fromLocalFile(path))       
                       
    # Função que cria uma nova instância da janela (novo objeto) na memória       
    def newUser(self):  # Cria uma nova instância da janela
        self.new_window = GUI(self.app)  # Cria uma nova instância da janela
        self.new_window.show()  # Exibe a nova janela
    
    def saveData(self):
        db = Database(self.browsers_list)
        db.save_form_data()
        
    def importData(self):
        importer = Importer()
        importer.import_data_to_forms(self.browsers_list)

    def printWindow(self):
        print_pages = ["form1_print.html", "form2_print.html"]
        folder_path = "_models_print"
        self.print_window = PrintWindow(print_pages, folder_path, self.browsers_list_temp)
        self.print_window.show()
    