from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datetime import datetime


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(950, 650)

        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)

        self.webtabs = QtWidgets.QTabWidget(Frame)
        self.webtabs.setObjectName("webtabs")

        self.addTab(url="https://duckduckgo.com")

        add_tab_layout = QtWidgets.QHBoxLayout()

        self.addTabButton = QtWidgets.QPushButton("+")
        self.addTabButton.setObjectName("addTabButton")
        self.addTabButton.clicked.connect(lambda: self.addTab(url="https://duckduckgo.com"))

        self.goTo = QtWidgets.QPushButton(">")
        self.goTo.setObjectName("goTo")

        self.searchbar = QtWidgets.QLineEdit()
        self.searchbar.setObjectName("searchbar")
        self.searchbar.setText("DuckDuckGo! ile arama yapın")
        self.searchbar.returnPressed.connect(lambda: self.addTab(url=f"https://duckduckgo.com?t=h_&q={self.searchbar.text()}"))
        self.goTo.clicked.connect(lambda: self.addTab(url=f"https://duckduckgo.com?t=h_&q={self.searchbar.text()}"))

        add_tab_layout.addWidget(self.addTabButton, stretch=1)
        add_tab_layout.addWidget(self.goTo, stretch=1)
        add_tab_layout.addWidget(self.searchbar, stretch=7)

        self.verticalLayout.addLayout(add_tab_layout)
        self.verticalLayout.addWidget(self.webtabs)

        self.retranslateUi(Frame)
        self.webtabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Hüma"))

    def addTab(self, url):
        new_tab = QtWidgets.QWidget()
        webEngineView = QWebEngineView(new_tab)
        webEngineView.setUrl(QtCore.QUrl(url))
        webEngineView.setObjectName("webEngineView")

        urlbar_layout = QtWidgets.QHBoxLayout()

        self.urlbar = QtWidgets.QLineEdit(new_tab)
        self.urlbar.setObjectName("urlbar")
        self.urlbar.setText(url)  # Sekme oluşturulurken URL çubuğuna varsayılan URL'yi yerleştir
        urlbar_layout.addWidget(self.urlbar, stretch=7)

        self.goBackButton = QtWidgets.QPushButton("<")
        self.goBackButton.setObjectName("goBackButton")
        self.goBackButton.clicked.connect(webEngineView.back)
        urlbar_layout.addWidget(self.goBackButton, stretch=1)

        self.goForwardButton = QtWidgets.QPushButton(">")
        self.goForwardButton.setObjectName("goForwardButton")
        self.goForwardButton.clicked.connect(webEngineView.forward)
        urlbar_layout.addWidget(self.goForwardButton, stretch=1)

        self.addBookmarks = QtWidgets.QPushButton("+")
        self.addBookmarks.setObjectName("addBookmarks")
        self.addBookmarks.clicked.connect(lambda: self.addBookmark(url=webEngineView.url()))
        urlbar_layout.addWidget(self.addBookmarks, stretch=1)

        self.reloadButton = QtWidgets.QPushButton("Yenile")
        self.reloadButton.setObjectName("reloadButton")
        self.reloadButton.clicked.connect(webEngineView.reload)
        urlbar_layout.addWidget(self.reloadButton, stretch=1)

        layout = QtWidgets.QVBoxLayout(new_tab)
        layout.addLayout(urlbar_layout)
        layout.addWidget(webEngineView)

        webEngineView.loadFinished.connect(lambda: self.urlbar.setText(webEngineView.url().toString()))  # URL çubuğunun değerini güncelle

        webEngineView.loadFinished.connect(lambda: self.webtabs.setTabText(self.webtabs.indexOf(new_tab), webEngineView.page().title()))
        webEngineView.loadFinished.connect(lambda: self.addHistory(webEngineView.url(), datetime.now()))

        self.webtabs.addTab(new_tab, "Yeni sekme {}".format(self.webtabs.count() + 1))
    def addHistory(self, url, time):
        with open("./history", "a") as f:
            f.write(f"tarih: {time}, URL: {url}\n")
            return None
    def addBookmark(self, url):
        with open("./bookmarks", "a") as f:
            f.write(f"URL: {url}\n")
            return None
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
