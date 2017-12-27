import xlsxwriter

ORANGE = '#FF6600'
ORANGE1 = '#FFCC00'

def header(workbook, worksheet):
    HEADER_FORMAT = workbook.add_format({'font_name': 'Liberation Sans',
                                         'font_size': 14,
                                         'align': 'center', 
                                         'valign': 'vcenter', 
                                         'bold': 1
                                        })

    worksheet.merge_range('A1:Q1', 'FICHE INDIVIDUELLE D\'EVALUATION DES TECHNICITES\nSURVEILLANCE et SAUVETAGE AQUATIQUE sur le LITTORAL avec option Pilotage', HEADER_FORMAT)
    worksheet.set_row(0,52)
    worksheet.set_row(1,31)

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
    worksheet.write('I4', 'Fait*', HEADER_FAIT_FORMAT)
    worksheet.write('Q4', 'Fait*', HEADER_FAIT_FORMAT)

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

def populate_file(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_zoom(80)

    header(workbook, worksheet)
    workbook.close()


if __name__ == '__main__':
    populate_file('Example.xlsx')
