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

# Chaque module doit avoir :
#  - une liste de bilans
#  - une liste de tests
# Chaque test doit avoir :
#  - une liste de résultats

def pic(color):
    if color == GREY:
        return IMG_PATH + '/grey_arrow.png'
    if color == WHITE:
        return IMG_PATH + '/white_arrow.png'

class _Implem():
    def __init__(self, workbook, worksheet, **bilan_eleve):
        self.workbook = workbook
        self.worksheet = worksheet
        self.check_dic(bilan_eleve)
        self.infos = bilan_eleve

    # devrait raise une exception en cas d'erreur
    def check_dic(self):
        pass

    def populate_workbook(self):
        self.set_print_format()
        self.header()
        self.body()
        self.footer()
    def header(self):
        pass
    def body(self):
        pass
    def footer(self):
        pass
    def set_print_format(self):
        pass
    def populate_file(filename, **bil):
        pass
