import sys
import os
from gui import GUI, QApplication

def main():
    # Cria uma instância de QApplication
    app = QApplication(sys.argv)

    # Cria uma instância da classe GUI
    gui = GUI(app)
    gui.show()  # Exibe a janela principal

    # Inicia o loop de eventos
    sys.exit(app.exec())
    

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    main()
    
