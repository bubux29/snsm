import xlsxwriter

BLUE = '#000099'
GREEN = '#009999'
ORANGE = '#FF6600'
ORANGE1 = '#FFCC00'
GREY = '#DDDDDD'
WHITE = '#FFFFFF'
DARK = '#000000'

IMG_PATH='static/img'

CA_VALIDE=u'☒'
CA_VALIDE_PAS_ENCORE=u'☐'

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
    #def __init__(self, filename, **bilan_eleve):
    def __init__(self, workbook, worksheet, bilan_eleve, prenom_eleve, nom_eleve):
        self.workbook = workbook
        self.worksheet = worksheet
        self.check_dic(bilan_eleve)
        self.infos = bilan_eleve
        self.prenom_eleve = prenom_eleve
        self.nom_eleve = nom_eleve

    # devrait raise une exception en cas d'erreur
    def check_dic(self, bilan_eleve):
        pass

    def ajout_tech_module(self, nom_module, mise_en_page_titre,
                          mise_en_page_test, col_debut, col_fin, ligne_debut):
        infos = self.infos
        worksheet = self.worksheet
        try:
            module = infos[nom_module]
        except:
            raise
        def en_int(ascii_char):
            return ord(ascii_char) - ord('A')
        col_debut = en_int(col_debut)
        col_fin   = en_int(col_fin)
        worksheet.merge_range(ligne_debut, col_debut,
                              ligne_debut, col_fin,
                              nom_module.upper(), mise_en_page_titre)
        ligne = ligne_debut + 1
        col_fin -= 1
        for test in module.liste_tests:
            worksheet.merge_range(ligne, col_debut,
                                  ligne, col_fin,
                                  test.description_test, mise_en_page_test)

            c = CA_VALIDE_PAS_ENCORE
            if test.bilan_test() == 1:
                c = CA_VALIDE
            worksheet.write(ligne, col_fin+1, c, mise_en_page_test)
            ligne += 1

    def page_layout(self):
        worksheet = self.worksheet
        worksheet.set_zoom(80)
        worksheet.set_landscape()
        worksheet.set_page_view()
        worksheet.hide_gridlines(1)
        worksheet.fit_to_pages(1, 0)
        worksheet.print_area(0, 0, 76, 16)
        worksheet.set_h_pagebreaks([43])
        worksheet.set_margins(.39, .39, .39, .39)

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
        self.page_layout()

    def _body_tpc(self, first_row):
        _first_row = first_row
        workbook = self.workbook
        worksheet = self.worksheet
        set_rows(worksheet, _first_row - 1, _first_row, 13)
        HEADER_SUBTITLE_FORMAT_BLUE = workbook.add_format({
                                                 'font_name': 'Liberation Sans',
                                                 'font_size': 14,
                                                 'font_color': '#FFFFFF',
                                                 'bold': 1,
                                                 'border': 1,
                                                 'align': 'center', 
                                                 'valign': 'vcenter', 
                                                 'fg_color': BLUE,
                                                 })
        HEADER_SUBTITLE_FORMAT_GREEN = workbook.add_format({
                                                 'font_name': 'Liberation Sans',
                                                 'font_size': 14,
                                                 'font_color': '#FFFFFF',
                                                 'bold': 1,
                                                 'border': 1,
                                                 'align': 'center', 
                                                 'valign': 'vcenter', 
                                                 'fg_color': GREEN,
                                                 })
        HEADER_SUBTITLE_FORMAT_NORMAL = workbook.add_format({
                                                 'font_name': 'Liberation Sans',
                                                 'font_size': 10,
                                                 'border': 1,
                                                 'align': 'center', 
                                                 'valign': 'vcenter', 
                                                 })
        HEADER_SUBTITLE_FORMAT_VALIDATION_BLUE = workbook.add_format({
                                                 'font_name': 'Liberation Sans',
                                                 'font_size': 9,
                                                 'font_color': BLUE,
                                                 'bold': 1,
                                                 'border': 1,
                                                 'align': 'center', 
                                                 'valign': 'vcenter', 
                                                 })
        HEADER_SUBTITLE_FORMAT_VALIDATION_GREEN = workbook.add_format({
                                                 'font_name': 'Liberation Sans',
                                                 'font_size': 9,
                                                 'font_color': GREEN,
                                                 'border': 1,
                                                 'align': 'center', 
                                                 'valign': 'vcenter', 
                                                 })
        worksheet.merge_range('A' + str(_first_row) + ':A' + str(_first_row + 1),
                              'CRITERES', HEADER_SUBTITLE_FORMAT_BLUE)
        worksheet.merge_range('M' + str(_first_row) + ':O' + str(_first_row + 1),
                              'CAPACTIES', HEADER_SUBTITLE_FORMAT_GREEN)
        worksheet.merge_range('B' + str(_first_row) + ':G' + str(_first_row),
                             'MISE EN SITUATION', HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.write('B' + str(_first_row+1), 'MS1⁽¹⁾',
                                                 HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.write('C' + str(_first_row+1), 'MS2⁽¹⁾',
                                                 HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.write('D' + str(_first_row+1), 'MS3⁽¹⁾',
                                                 HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.write('E' + str(_first_row+1), 'MS4⁽¹⁾',
                                                 HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.write('F' + str(_first_row+1), 'MS5⁽¹⁾',
                                                 HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.write('G' + str(_first_row+1), 'MS...⁽¹⁾',
                                                 HEADER_SUBTITLE_FORMAT_NORMAL)
        worksheet.merge_range('H' + str(_first_row) + ':I' + str(_first_row+1),
                              'Validation des\ncritères⁽¹⁾⁽²⁾',
                              HEADER_SUBTITLE_FORMAT_VALIDATION_BLUE)
        worksheet.merge_range('P' + str(_first_row) + ':Q' + str(_first_row+1),
                              'Validation des\ncapacités⁽¹⁾',
                              HEADER_SUBTITLE_FORMAT_VALIDATION_BLUE)

def exporte_resultat(classe, filedir, nom_eleve, prenom_eleve, bilans_par_module):
    filename = filedir + '/' + '_'.join([nom_eleve, prenom_eleve])
    workbook = xlsxwriter.Workbook(filename + '.xlsx')
    worksheet = workbook.add_worksheet()
    pt = classe(workbook, worksheet, bilans_par_module, prenom_eleve, nom_eleve)
    pt.populate_workbook()

