import re

def addSpacesAfterComma(text):
    return ', '.join(text.split(','))
def checkCorrectnessOfInputForText(text):
    return re.match(r'^[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\s-]+$', text)
def checkCorrectnessOfInputForNumbers(text):
    return re.match(r'^\d+$', text)