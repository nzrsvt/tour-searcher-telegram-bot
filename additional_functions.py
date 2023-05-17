import re

def addSpacesAfterComma(text):
    return ', '.join(text.split(','))
def checkCorrectnessOfInput(text):
    return re.match(r'^[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\s-]+$', text)