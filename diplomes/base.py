import xlsxwriter

BLUE = '#000099'
GREEN = '#009999'
ORANGE = '#FF6600'
ORANGE1 = '#FFCC00'
GREY = '#DDDDDD'
WHITE = '#FFFFFF'
DARK = '#000000'

IMG_PATH='static/img'

def set_rows(worksheet, first, last, height):
    for i in range(first, last+1):
        worksheet.set_row(i, height)


def pic(color):
    if color == GREY:
        return IMG_PATH + '/grey_arrow.png'
    if color == WHITE:
        return IMG_PATH + '/white_arrow.png'

       
class _Implem():
    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

    def populate_workbook(self):
        self.header()
        self.body()
        self.footer()
    def header(self):
        pass
    def body(self):
        pass
    def footer(self):
        pass
