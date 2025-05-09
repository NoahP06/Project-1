from PyQt6.QtWidgets import QApplication
from television import MainTVApp 
import sys



def main():
    app = QApplication(sys.argv)
    window = MainTVApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
