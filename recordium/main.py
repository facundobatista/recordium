
# FIXME: license

# from urllib import request
import sys

from PyQt5 import QtWidgets, QtGui


"""
TODO!

- interafz
    - menu:
        - N notifs sin leer: abre una ventana con una notif por linea
        - acerca de: imitar el de launcherposta
        - salir: sale y cierra
    - que cuando tenga sin leer esté "activado", sino apagado
    - un icono:
        - disquito con flechita de telegram opuesta
        - pasivo: centro blanco grisoide
        - activo: centro amarillo
- dinamica:
    - pollee 1xmin, usando ult
    - si tiene algo lo graba local
"""

API_BASE = "https://api.telegram.org/bot{token}/{method}"


TOKEN = "245852664:AAETsEcmK2aed2T6_Af_PoQujD8COgFti_I"


class SysTray:
    def __init__(self, app):
        icon = QtGui.QIcon("media/icon-192.png")

        self.sti = sti = QtWidgets.QSystemTrayIcon(icon)
        self.menu = menu = QtWidgets.QMenu()
        action = menu.addAction("N messages")
        action.triggered.connect(self.show_messages)
        menu.addSeparator()
        action = menu.addAction("Configure")
        action.triggered.connect(self.configure)
        action = menu.addAction("About")
        action.triggered.connect(self.about)
        action = menu.addAction("Quit")
        action.triggered.connect(lambda _: app.quit())
        sti.setContextMenu(menu)

        sti.show()

    def show_messages(self, _):
        print("========= messa")

    def configure(self, _):
        print("========= config")

    def about(self, _):
        print("========= about")


def go():
    print("start")
    # url = API_BASE.format(token=TOKEN, method="getUpdates")
    # print("=========url", url)
    # req = request.urlopen(url)
    # resp = req.read()
    # print("========= resp", repr(resp))

    app = QtWidgets.QApplication(sys.argv)
    ss = SysTray(app)
    sys.exit(app.exec_())
