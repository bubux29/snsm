import unicodedata

def sans_accents(string):
    licorn = string.encode('utf-8')
    kk = unicodedata.normalize('NFKD', string)
    return u''.join([c for c in kk if not unicodedata.combining(c)])
