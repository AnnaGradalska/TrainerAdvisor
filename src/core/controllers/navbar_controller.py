class NavbarController:
    def __init__(self, ui):
        self.ui = ui

    def open_page(self, page):
        self.ui.stackedWidget.setCurrentWidget(page)
