import xlsxwriter
from diplomes.base import BLUE, GREEN, ORANGE, ORANGE1, GREY, WHITE, DARK, IMG_PATH, set_rows, pic, _Implem


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
        worksheet.merge_range('A2:I2', 'Participant :', HEADER_PARTICIPANT_FORMAT)
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
        worksheet.merge_range('A6:I6', 'SANS MATERIEL', HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('K6:Q6', 'MONTAGE ET PREPARATION',
                              HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('A20:I20', 'RESCUE TUBE',
                              HEADER_FOREIGN_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('K9:Q9', 'VERIFICATION PRE-OPERATIONNELLES',
                              HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('K14:Q14', 'MANOEUVRES D\'URGENCE',
                              HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('K19:Q19', 'MISE EN OEUVRE',
                              HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('K30:Q30', 'RECUPERATION DE VICTIME',
                              HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('A30:I30', 'PLANCHE DE SAUVETAGE',
                              HEADER_SUBSUBTITLE_FORMAT)
        worksheet.merge_range('A38:I38', 'COMMUNICATION', HEADER_SUBSUBTITLE_FORMAT)
    
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

        # On descend dans le tableau
        _row = _first_row + 2
        set_rows(worksheet, _row - 1, _row+16, 26)

        _row += self.module(_row, GREY,
                        "Situer son rôle et sa mission au sein d'un dispositif évolutif et adaptable aux conditions du moment",
                        ["met en œuvre les différentes missions du SSA littoral",
                        "rend compte à son responsable / autorité d'emploi"])

        _row += self.module(_row, WHITE,
                        "Effectuer une analyse des risques particuliers présents sur sa zone",
                        ["identifie les risques liés à l'environnement et aux phénomènes naturels",
                        "identifie les risques d'une activité par rapport à l'environnement observé"])

        _row += self.module(_row, GREY,
                         "Développer des actions de prévention adaptées aux risques et pratiques sur zone",
                        ["renseigne le tableau d'information à partir d'un bulletin météo",
                         "réalise l'action de prévention adaptée",
                         "respecte les règles de communication et de construction du message de prévention"])

        _row += self.module(_row, WHITE,
                         "Participer à un dispositif de surveillance en mettant en œuvre des techniques opérationnelles adaptées et mettant éventuellement en œuvre des moyens spécifiques",
                         ["réalise une surveillance active et constante en tenant compte des contraintes liées au milieu naturel",
                          "se positionne dans un dispositif de surveillance en respectant le rôle défini et en utilisant le matériel adapté si nécessaire",
                          "détecte les signes visibles d'une détresse"])
        _row += self.module(_row, GREY,
                         "Réaliser des gestes de premier secours adaptés",
                         ["prend en compte les contraintes du milieu naturel dans les gestes de premier secours",
                          "réalise les gestes adaptés conformément au référentiel technique SNSM"])
        _row += self.module(_row, WHITE,
                         "Participer à une action coordonnée de sauvetage, dans sa zone, ou à proximité immédiate de celle-ci, à l'aide de techniques opérationnelles adaptées ou en mettant en œuvre des matériels spécifiques",
                         ["applique les procédures en respectant les différentes étapes",
                          "évolue en sécurité sur la plage et dans l'eau (à la nage et en planche de sauvetage)",
                          "réalise une action de sauvetage avec ou sans matériel",
                          "participe à une action coordonnée de sauvetage"])
        _row += self.module(_row, GREY,
                          "",
                          ["réalise une action de sauvetage en tant que pilote d'une embarcation motorisée (UNIQUEMENT POUR LA MENTION PILOTAGE)"])

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
