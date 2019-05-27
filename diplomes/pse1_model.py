import xlsxwriter
from diplomes.base import BLUE, GREEN, ORANGE, ORANGE1, GREY, WHITE, DARK, IMG_PATH, set_rows, pic, _Implem, CA_VALIDE, CA_VALIDE_PAS_ENCORE

import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

#worksheet.write(0, 0, CA_VALIDE)
FONT_NAME='Liberation Sans'

class pse1_tech(_Implem):
    def header(self):
        workbook = self.workbook
        worksheet = self.worksheet
        HEADER_FORMAT = workbook.add_format({
                                             'font_name': FONT_NAME,
                                             'font_size': 18,
                                             'align': 'center', 'valign': 'vcenter',
                                             'bold': 1
                                            })
        DETAILS_FORMAT = workbook.add_format({
                                             'font_name': FONT_NAME,
                                             'font_size': 12,
                                             'valign': 'vcenter',
                                            })
        DETAILS_FORMAT_CENTER = workbook.add_format({
                                             'font_name': FONT_NAME,
                                             'font_size': 12,
                                             'align': 'center', 'valign': 'vcenter',
                                            })
        NOM_PARTICIPANT_FORMAT = workbook.add_format({
                                             'font_name': FONT_NAME,
                                             'font_size': 12,
                                             'align': 'center', 'valign': 'vcenter',
                                             'bold': 1,
                                             'fg_color': WHITE,
                                             'font_scheme': 'major',
                                            })
        worksheet.set_column(0, 1, 26)
        worksheet.set_column(2, 4, 10)
        worksheet.set_column(5, 5, 60)
        worksheet.set_row(0, 13)
        worksheet.set_row(4, 13)
        worksheet.set_row(6, 13)
        set_rows(worksheet, 1, 3, 23)
        set_rows(worksheet, 10, 11, 13)

        worksheet.merge_range(1, 0, 1, 7,
                              'FICHE INDIVIDUELLE - EVALUATION DE LA TECHNICITE',
                              HEADER_FORMAT)
        worksheet.merge_range(2, 0, 2, 7,
                              'PREMIERS SECOURS EN EQUIPRE DE NIVEAU 1',
                              HEADER_FORMAT)

        worksheet.write(5, 0, 'Nom du participant :', DETAILS_FORMAT)
        worksheet.write(7, 0, 'Date formation :   du ', DETAILS_FORMAT)
        worksheet.write(7, 2, 'au', DETAILS_FORMAT_CENTER)
        worksheet.merge_range(5, 1, 5, 3,
                       self.nom_eleve + ' ' + self.prenom_eleve,
                       NOM_PARTICIPANT_FORMAT)

    def body(self):
        workbook = self.workbook
        worksheet = self.worksheet
        _first_line=12

        TITRE_FORMAT = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 11,
                                          'valign': 'vcenter',
                                          'fg_color': ORANGE1,
                                          'border': 1,
                                          })
        DESC_FORMAT = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 11,
                                          'valign': 'vcenter',
                                          'border': 1,
                                          })
        DESC_FORMAT_CENTER = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 14,
                                          'align': 'center', 'valign': 'vcenter',
                                          'border': 1,
                                          })

        at = _first_line
        columns=(0, 3)
        nmomo = 0
        for module_name, bilan in self.infos.items():
            if nmomo == 4:
                at = _first_line
                columns = (5, 7)
            at += self.ajout_tech_module(module_name, TITRE_FORMAT, DESC_FORMAT,
                    columns[0], columns[1], at)
            #at = self._add_module(at, columns[0], columns[1], bilan)
            nmomo += 1

        worksheet.write(35, 5,
                        '(1) Renseigner la case par une croix',
                        workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 11,
                                          'valign': 'vcenter',
                                          }))

    def _add_module(self, first_line, first_column, last_column, module):
        workbook = self.workbook
        worksheet = self.worksheet
        TITRE_FORMAT = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 11,
                                          'valign': 'vcenter',
                                          'fg_color': ORANGE1,
                                          'border': 1,
                                          })
        DESC_FORMAT = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 11,
                                          'valign': 'vcenter',
                                          'border': 1,
                                          })
        DESC_FORMAT_SMALL = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 9,
                                          'valign': 'vcenter',
                                          'border': 1,
                                          })
        DESC_FORMAT_CENTER = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 14,
                                          'align': 'center', 'valign': 'vcenter',
                                          'border': 1,
                                          })

        worksheet.merge_range(first_line, first_column, first_line, last_column,
                              module.nom_module.upper() + ' ⁽¹⁾', TITRE_FORMAT)

        line  = first_line + 1
        for test in module.liste_tests:
            if test.synthese() == 1:
                resultat = CA_VALIDE 
            else:
                resultat = CA_VALIDE_PAS_ENCORE
            worksheet.write(line, last_column,
                            resultat, DESC_FORMAT_CENTER)
            worksheet.write(line, last_column - 1,
                            'FT', DESC_FORMAT_SMALL)
            if last_column - 2 == first_column:
                worksheet.write(line, first_column,
                                test.description_test, DESC_FORMAT)
            else:
                worksheet.merge_range(line, first_column,
                                line, last_column - 2,
                                test.description_test, DESC_FORMAT)
            line += 1
        return line

    def footer(self):
        workbook = self.workbook
        worksheet = self.worksheet
        _first_line = 47
        DESC_FORMAT = workbook.add_format({
                                          'font_name': FONT_NAME,
                                          'font_size': 11,
                                          'valign': 'vcenter',
                                          'underline': 1,
                                          })
        worksheet.write(_first_line, 0,
                        'Nom et signature du responsable pédagogique :',
                        DESC_FORMAT)
        worksheet.write(_first_line, 5,
                        'Nom et signature du candidat :',
                        DESC_FORMAT)

    def set_print_format(self):
        worksheet = self.worksheet
        worksheet.set_zoom(70)
        worksheet.set_landscape()
        #worksheet.set_page_view()
        worksheet.hide_gridlines(1)
        worksheet.fit_to_pages(1, 1)
        worksheet.print_area(0, 0, 56, 7)
        worksheet.set_margins(.43, .24, .75, .32)
        # set paper: A4
        worksheet.set_paper(9)

def populate_file(filename, **bilan_eleve):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    pt = pse1_tech(workbook, worksheet, **bilan_eleve)
    pt.populate_workbook()

if __name__ == '__main__':
    import formation_db
    cours = formation_db.trouver_cours(['PSE1 Technicités'])
    modules = formation_db.trouver_modules_par_cours(cours)
    if not modules:
        exit
    bilan = list()
    groupes = formation_db.trouver_groupe(['1A'])
    if not groupes:
        exit
    eleves = sorted(set([gr.participants for gr in groupes]))
    bilans = formation_db.trouver_bilans_par_eleve(eleves, modules)
    bilans_par_eleve = dict()
    for bilan in bilans:
        populate_file('Example_pse1.xlsx', bilan.eleve.__str__())
