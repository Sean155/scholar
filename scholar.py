from src.gui import main_w2, QApplication
from src.creat_session import creat_session
import sys

app = QApplication(sys.argv)
session = creat_session()

gui = main_w2(session)
gui.show()
sys.exit(app.exec_())
