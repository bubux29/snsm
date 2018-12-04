import xlsxwriter
from diplomes.base import BLUE, GREEN, ORANGE, ORANGE1, GREY, WHITE, DARK, IMG_PATH, set_rows, pic, _Implem, CA_VALIDE, CA_VALIDE_PAS_ENCORE

def set_column_widths(worksheet):
    # Set column A width
    worksheet.set_column(0, 0, 49)
    # B:I
    worksheet.set_column(1, 8, 4.7)
    # Set column J width
    worksheet.set_column(9, 9, 1)
    # K:L
    worksheet.set_column(10, 11, 4.7)
    # Set column M width
    worksheet.set_column(12, 12, 29)
    # N
    worksheet.set_column(13, 13, 2.5)
    # Set column O width
    worksheet.set_column(14, 14, 22)
    # P:Q
    worksheet.set_column(15, 16, 4.7)

class ssa_tech(_Implem):
    def header(self):
        workbook = self.workbook
        worksheet = self.worksheet
        HEADER_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                             'font_size': 14,
                                             'align': 'center', 
                                             'valign': 'vcenter', 
                                             'bold': 1
                                            })
    
        worksheet.merge_range('A1:Q1', 'FICHE INDIVIDUELLE D\'EVALUATION DES TECHNICITES\nSURVEILLANCE et SAUVETAGE AQUATIQUE sur le LITTORAL avec option Pilotage', HEADER_FORMAT)
        worksheet.set_row(0,52)
        worksheet.set_row(1,31)
        worksheet.set_row(2,17)
        set_rows(worksheet, 4, 41, 17)
    
        set_column_widths(worksheet)
    
        worksheet.insert_image('A1', 'static/img/logo_snsm_240x240.png',
                               {'y_offset': 20, 'x_scale': .4, 'y_scale': .4,
                                'positioning': 3})
    
        HEADER_PARTICIPANT_FORMAT = workbook.add_format({
                                                  'font_name': 'Liberation Sans',
                                                  'font_size': 14,
                                                  'bold': 1,
                                                  'valign': 'vcenter', 
                                                  'indent': 7,
                                                 })
    
        HEADER_DATE_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                                  'font_size': 14,
                                                  'bold': 1,
                                                  'valign': 'vcenter', 
                                                 })
    
        HEADER_FAIT_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                                  'font_size': 10,
                                                  'align': 'center', 
                                                  'valign': 'vcenter', 
                                                 })
        worksheet.merge_range('A2:I2', 'Participant : ' +
                                       ' '.join([self.prenom_eleve, self.nom_eleve]),
                                       HEADER_PARTICIPANT_FORMAT)
        worksheet.merge_range('K2:M2', 'Date du', HEADER_DATE_FORMAT)
        worksheet.merge_range('N2:Q2', 'au', HEADER_DATE_FORMAT)
    
        worksheet.merge_range('A3:H4', 'SSA Littoral', HEADER_FORMAT)
        worksheet.merge_range('K3:P4', 'Mention Pilotage', HEADER_FORMAT)
        worksheet.write('I4', 'Fait⁽¹⁾', HEADER_FAIT_FORMAT)
        worksheet.write('Q4', 'Fait⁽¹⁾', HEADER_FAIT_FORMAT)
    

    def body(self):
        workbook = self.workbook
        worksheet = self.worksheet
        HEADER_SUBTITLE_FORMAT = workbook.add_format({
                                                  'font_name': 'Liberation Sans',
                                                  'font_size': 11,
                                                  'bold': 1,
                                                  'border': 1,
                                                  'valign': 'vcenter', 
                                                  'fg_color': ORANGE,
                                                 })
        worksheet.merge_range('A5:I5', 'TECHNIQUES DE SAUVETAGE',
                              HEADER_SUBTITLE_FORMAT)
        worksheet.merge_range('K5:Q5', 'TECHNIQUES PRE-OPERATIONNELLES',
                              HEADER_SUBTITLE_FORMAT)
        worksheet.merge_range('K13:Q13', 'TECHNIQUES', HEADER_SUBTITLE_FORMAT)
    
        HEADER_SUBSUBTITLE_FORMAT = workbook.add_format({
                                                  'font_name': 'Liberation Sans',
                                                  'font_size': 11,
                                                  'bold': 1,
                                                  'border': 1,
                                                  'valign': 'vcenter', 
                                                  'fg_color': ORANGE1,
                                                 })
        HEADER_FOREIGN_SUBSUBTITLE_FORMAT = workbook.add_format({
                                                  'font_name': 'Liberation Sans',
                                                  'font_size': 11,
                                                  'bold': 1,
                                                  'border': 1,
                                                  'italic': 1,
                                                  'valign': 'vcenter', 
                                                  'fg_color': ORANGE1,
                                                 })
        HEADER_TEST_DESCRIPTION_FORMAT = workbook.add_format({
                                                  'font_name': 'Liberation Sans',
                                                  'font_size': 11,
                                                  'bold': 0,
                                                  'border': 1,
                                                  'italic': 1,
                                                  'valign': 'vcenter', 
                                                  'fg_color': WHITE,
                                                 })
        self.ajout_tech_module('Sans matériel',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'A', 'I', 5)
        self.ajout_tech_module('Montage et préparation',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'K', 'Q', 5)
        self.ajout_tech_module('Rescue Tube',
                               HEADER_FOREIGN_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'A', 'I', 19)
        self.ajout_tech_module('Vérifications pré-opérationnelles',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'K', 'Q', 8)
        self.ajout_tech_module('Manoeuvres d\'urgence',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'K', 'Q', 13)
        self.ajout_tech_module('Mise en oeuvre',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'K', 'Q', 18)
        self.ajout_tech_module('Récupération de victime',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'K', 'Q', 29)
        self.ajout_tech_module('Planche de sauvetage',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'A', 'I', 29)
        self.ajout_tech_module('Communication',
                               HEADER_SUBSUBTITLE_FORMAT, HEADER_TEST_DESCRIPTION_FORMAT,
                               'A', 'I', 37)
    
    def footer(self):
        workbook = self.workbook
        worksheet = self.worksheet
        FOOTER_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                             'font_size': 8,
                                             'valign': 'vcenter', 
                                             'italic': 1,
                                            })
        worksheet.set_row(42, 12)
        worksheet.merge_range('A43:Q43', "⁽¹⁾ Les cases vides sont à renseigner d'une croix lorsque la technique est parfaitement réalisée",
                              FOOTER_FORMAT)
    
        BILAN_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                            'font_size': 10,
                                            'align': 'top',
                                            'bold': 1, 'italic': 1,
                                           })
        worksheet.merge_range('K39:Q40', 'Observations :', BILAN_FORMAT)
        worksheet.merge_range('K41:M42', 'Signature du\nresponsable pédagogique :', BILAN_FORMAT)
        worksheet.merge_range('N41:Q42', 'Signature du\nparticipant :', BILAN_FORMAT)

class ssa_tpc(_Implem):
    def header(self):
        first_row = 43
        _first_row = first_row + 1 # On compte différemment selon les formats
        workbook = self.workbook
        worksheet = self.worksheet

        set_column_widths(worksheet)

        HEADER_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                             'font_size': 14,
                                             'align': 'center', 
                                             'valign': 'vcenter', 
                                             'bold': 1
                                            })
    
        worksheet.merge_range('A' + str(_first_row) + ':Q' + str(_first_row), 
                              'FICHE INDIVIDUELLE D\'EVALUATION DES CAPACITES THEORIQUES, PRATIQUES ET COMPORTEMENTALES\nSURVEILLANCE et SAUVETAGE AQUATIQUE sur le LITTORAL avec option Pilotage', HEADER_FORMAT)
        worksheet.set_row(first_row,52)
        worksheet.set_row(first_row+1,31)
    
        worksheet.insert_image('A' + str(_first_row),
                               'static/img/logo_snsm_240x240.png',
                               {'y_offset': 0, 'x_scale': .4, 'y_scale': .4,
                                'positioning': 3})
    
        HEADER_PARTICIPANT_FORMAT = workbook.add_format({
                                                  'font_name': 'Liberation Sans',
                                                  'font_size': 14,
                                                  'bold': 1,
                                                  'valign': 'vcenter', 
                                                  'indent': 7,
                                                 })
    
        HEADER_DATE_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                                  'font_size': 14,
                                                  'bold': 1,
                                                  'valign': 'vcenter', 
                                                 })
    
        HEADER_FAIT_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                                  'font_size': 10,
                                                  'align': 'center', 
                                                  'valign': 'vcenter', 
                                                 })
        worksheet.merge_range('A' + str(_first_row+1) + ':I' + str(_first_row+1),
                              'Participant :', HEADER_PARTICIPANT_FORMAT)
        worksheet.merge_range('K' + str(_first_row + 1) + ':M' + str(_first_row + 1) + '',
                              'Date du', HEADER_DATE_FORMAT)
        worksheet.merge_range('N' + str(_first_row + 1) + ':Q' + str(_first_row + 1) + '',
                              'au', HEADER_DATE_FORMAT)
    
    def body(self):
        _first_row = 46
        workbook = self.workbook
        worksheet = self.worksheet
        self._body_tpc(_first_row)

        # On descend dans le tableau
        _row = _first_row + 2
        set_rows(worksheet, _row - 1, _row+16, 26)

        colsel = 0
        for (description, module) in self.infos.items():
            if colsel:
                color = WHITE
            else:
                color = GREY
            colsel = not colsel
            _row += self.module(_row, color, description,
                    [test.description_test for test in module.liste_tests])
        return

    def footer(self):
        workbook = self.workbook
        worksheet = self.worksheet
        _first_row = 65
        FORMAT_INFO = workbook.add_format({'font_name': 'Liberation Sans',
                                           'font_size': 8,
                                           'align': 'center',
                                           'valign': 'vcenter',
                                          })
        worksheet.merge_range('A' + str(_first_row) + ':Q' + str(_first_row),
                              "⁽¹⁾ Renseigner les cases avec A ou B (A = Acquis / B = en cours d'acquisition) - ⁽²⁾ La présence d'au moins un A sur la ligne valide le critère - ⁽³⁾ Renseigner les cases avec OUI lorsque l'ensemble des critères de la capacité est acquis et NON dans le cas contraire",
                              FORMAT_INFO)

    def module(self, rownum, color, module_desc, criteres):

        worksheet = self.worksheet
        workbook = self.workbook
        _first_row = rownum
        CRITERE_FORMAT_TOP = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 10,
                                            'border': 1,
                                            'valign': 'vcenter', 
                                            'indent': 1,
                                            'fg_color': color,
                                            'text_wrap': 1,
                                            'top_color': BLUE,
                                            })
        CRITERE_FORMAT_BOTTOM = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 10,
                                            'border': 1,
                                            'valign': 'vcenter', 
                                            'indent': 1,
                                            'fg_color': color,
                                            'text_wrap': 1,
                                            'bottom_color': BLUE,
                                            })
        CRITERE_FORMAT = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 10,
                                            'border': 1,
                                            'valign': 'vcenter', 
                                            'indent': 1,
                                            'fg_color': color,
                                            'text_wrap': 1,
                                            })
        CAPACITE_FORMAT = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 10,
                                            'border': 1,
                                            'align': 'center', 
                                            'valign': 'vcenter', 
                                            'fg_color': color,
                                            'text_wrap': 1,
                                            'border_color': GREEN,
                                            })
        VALIDATION_FORMAT = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 14,
                                            'border': 1,
                                            'bold': 1,
                                            'align': 'center', 
                                            'valign': 'vcenter', 
                                            'fg_color': color,
                                            'left_color': BLUE,
                                            'right_color': BLUE,
                                            })
        VALIDATION_FORMAT_TOP = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 14,
                                            'border': 1,
                                            'bold': 1,
                                            'align': 'center', 
                                            'valign': 'vcenter', 
                                            'fg_color': color,
                                            'top_color': BLUE,
                                            'left_color': BLUE,
                                            'right_color': BLUE,
                                            })
        VALIDATION_FORMAT_BOTTOM = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 14,
                                            'border': 1,
                                            'bold': 1,
                                            'align': 'center', 
                                            'valign': 'vcenter', 
                                            'fg_color': color,
                                            'bottom_color': BLUE,
                                            'left_color': BLUE,
                                            'right_color': BLUE,
                                            })
        VALIDATION_CAP_FORMAT = workbook.add_format({
                                            'font_name': 'Liberation Sans',
                                            'font_size': 14,
                                            'border': 1,
                                            'bold': 1,
                                            'align': 'center', 
                                            'valign': 'vcenter', 
                                            'fg_color': color,
                                            'border_color': GREEN,
                                            })
        _row = _first_row
        img_path = pic(color)
        worksheet.insert_image('J' + str(_row - 1), img_path,
                               {'y_offset': 30, 'x_offset': 0,
                                'x_scale': .5, 'y_scale': .6,
                                'positioning': 2})
        self._fill_criteres(_row, criteres[0], CRITERE_FORMAT_TOP, VALIDATION_FORMAT_TOP)
        _row += 1
        for c in criteres[1:-1]:
            self._fill_criteres(_row, c, CRITERE_FORMAT, VALIDATION_FORMAT)
            _row += 1
        self._fill_criteres(_row, criteres[-1], CRITERE_FORMAT_BOTTOM, VALIDATION_FORMAT_BOTTOM)

        tot = len(criteres)
        deb = rownum; end = rownum + tot - 1
        _DUMMY = workbook.add_format({'fg_color': WHITE, 'border': 1})
        worksheet.merge_range('J' + str(deb) + ':L' + str(end), '', _DUMMY)
        worksheet.merge_range('M' + str(deb) + ':O' + str(end),
                              module_desc, CAPACITE_FORMAT)
        worksheet.merge_range('P' + str(deb) + ':Q' + str(end),
                              'NON', VALIDATION_CAP_FORMAT)
        return len(criteres)

    def _fill_criteres(self, _row, c, f, fv):
        worksheet = self.worksheet
        worksheet.write('A' + str(_row), c, f)
        for col in ['B', 'C', 'D', 'E', 'F', 'G']:
            #worksheet.write_blank(col + str(_first_row), VALIDATION_FORMAT)
            worksheet.write(col + str(_row), ' ', fv)
        worksheet.merge_range('H' + str(_row) + ':I' + str(_row),
                              '', fv)

class ssa_bilan(_Implem):
    def header(self):
        workbook = self.workbook
        worksheet = self.worksheet
        start_row = 66
        FORMAT_TITLE = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 14,
                                      'bold': 1, 'fg_color': ORANGE1, 'align': 'center',
                                      'valign': 'vcenter', 'border': 1,
                                    })
        FORMAT_TITLE_SMALL = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 12,
                                      'bold': 1, 'fg_color': ORANGE1, 'align': 'center',
                                      'valign': 'vcenter', 'border': 1,
                                    })
        FORMAT_TITLE_ORANGE = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 12,
                                      'bold': 1, 'fg_color': ORANGE, 'align': 'center',
                                      'valign': 'vcenter', 'border': 1,
                                    })
        FORMAT_PARTICIPANT = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 12,
                                       'align': 'left', 'valign': 'top',
                                    })

        FORMAT_EVALUATION = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 12,
                                       'align': 'left', 'valign': 'vcenter', 'bold': 1,
                                      'indent': 1, 'border': 1,
                                    })
        FORMAT_EVALUATION_BIS = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 12,
                                      'align': 'center', 'valign': 'vcenter', 'bold': 1,
                                      'border': 1,
                                    })
        FORMAT_NOTE = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 8,
                                       'align': 'left', 'valign': 'top', 
                                    })
        FORMAT_NOMS_SIGNATURES = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 10,
                                      'align': 'left', 'valign': 'top', 'bold': 1, 'underline': 1,
                                    })
        FORMAT_NOMS_SIGNATURES_RIGHT = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 10,
                                      'align': 'left', 'valign': 'top', 'bold': 1, 'underline': 1,
                                      'right': 1
                                    })
        FORMAT_LIEUX_COMMENTAIRES = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 10,
                                      'align': 'left', 'valign': 'top'
                                    })
        FORMAT_LIEUX_COMMENTAIRES_RIGHT = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 10,
                                      'align': 'left', 'valign': 'top', 'right': 1,
                                      'right_color': DARK
                                    })
        FORMAT_OBSERVATIONS_LEFT = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 10,
                                      'align': 'left', 'valign': 'top', 'bottom_color': DARK,
                                      'border_color': DARK
                                    })
        FORMAT_OBSERVATIONS_RIGHT = workbook.add_format({
                                      'font_name': 'Liberation Sans', 'font_size': 10,
                                      'align': 'left', 'valign': 'top', 'bottom': 1, 'right': 1,
                                      'right_color': DARK
                                    })

        worksheet.set_row(start_row, 12)
        worksheet.merge_range('A' + str(start_row) + ':Q' + str(start_row),
                              'EVALUATION DE CERTIFICATION', FORMAT_TITLE)
        worksheet.merge_range(start_row, 0, start_row + 1, 11, 'LE CANDIDAT :',
                              FORMAT_PARTICIPANT)
        start_row += 1
        worksheet.set_row(start_row, 17)
        worksheet.merge_range(start_row, 12, start_row, 16,
                              'APTITUDE INTERMEDIAIRE ⁽⁶⁾',
                              FORMAT_TITLE_SMALL)

        start_row += 1
        worksheet.set_row(start_row, 17)
        worksheet.merge_range(start_row, 0, start_row, 11,
                        'maîtrise les techniques et procédures relatives au "SSA LITTORAL" ⁽⁴⁾',
                        FORMAT_EVALUATION)
        start_row += 1
        worksheet.set_row(start_row, 17)
        worksheet.merge_range(start_row, 0, start_row, 11,
                  'maîtrise les techniques et procédures relatives à la "MENTION PILOTAGE" ⁽⁴⁾',
                  FORMAT_EVALUATION)
        start_row += 1
        worksheet.set_row(start_row, 17)
        worksheet.merge_range(start_row, 0, start_row, 11,
                  'met en oeuvre les capacités demandées ⁽⁵⁾', FORMAT_EVALUATION)
        start_row += 1
        set_rows(worksheet, start_row, start_row + 2, 17)
        worksheet.merge_range(start_row, 0, start_row + 2, 7,
                  "⁽⁴⁾ a obtenu une croix à chaque technique sur la fiche individuelle de l'évaluation des techniques\n"
                  "⁽⁵⁾ a obtenu un OUI dans chacune des capacités définies dans l'arrêté du 19 février 2014\n"
                  "⁽⁶⁾ rayer la mention inutile", FORMAT_NOTE)

        worksheet.merge_range(start_row, 12, start_row, 16, 'APTITUDE FINALE⁽⁶⁾',
                              FORMAT_TITLE_ORANGE)
        start_row += 1
        worksheet.merge_range(start_row, 8, start_row, 11, 'SSA LITTORAL', FORMAT_EVALUATION)
        start_row += 1
        worksheet.merge_range(start_row, 8, start_row, 11, 'Mention Pilotage', FORMAT_EVALUATION_BIS)

        start_row += 1
        worksheet.set_row(start_row, 25)
        worksheet.merge_range(start_row, 0, start_row, 11,
                             'Noms et signatures de l\'équipe pédagogique :', FORMAT_NOMS_SIGNATURES)
        worksheet.merge_range(start_row, 12, start_row, 16, 'Nom et signature du candidat',
                              FORMAT_NOMS_SIGNATURES_RIGHT)
        start_row += 1
        worksheet.set_row(start_row, 25)
        worksheet.merge_range(start_row, 0, start_row, 11, 'Lieu et date :', FORMAT_LIEUX_COMMENTAIRES)
        worksheet.merge_range(start_row, 12, start_row, 16, "Lieu et date :", FORMAT_LIEUX_COMMENTAIRES_RIGHT)
        start_row += 1
        worksheet.set_row(start_row, 37)
        worksheet.merge_range(start_row, 0, start_row, 11, 'Observations :', FORMAT_OBSERVATIONS_LEFT)
        worksheet.merge_range(start_row, 12, start_row, 16, 'Observations :', FORMAT_OBSERVATIONS_RIGHT)
        
def populate_file(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_zoom(80)
    worksheet.set_landscape()
    worksheet.set_page_view()
    worksheet.hide_gridlines(1)
    worksheet.fit_to_pages(1, 0)
    worksheet.print_area(0, 0, 76, 16)
    worksheet.set_h_pagebreaks([43])
    worksheet.set_margins(.39, .39, .39, .39)

    st = ssa_tech(workbook, worksheet)
    st.populate_workbook()

    stpc = ssa_tpc(workbook, worksheet)
    stpc.populate_workbook()

    bilan = ssa_bilan(workbook, worksheet)
    bilan.populate_workbook()

    workbook.close()


if __name__ == '__main__':
    populate_file('Example.xlsx')
