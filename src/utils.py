import textwrap
import datetime

def wrap_text(text, width):
    splittedText = text.split('\n')
    output = ''
    
    for _, line in enumerate(splittedText):
        if line == '' and output != '':
            output += '\n\n'
            
        output += "\n".join(textwrap.wrap(line, width))
            
    return output

def isValidDate(date) -> bool:
    '''Check if date is valid. Date must be in the format dd-mm-yyyy'''
    
    try:
        day, month, year = date.split('-')
        datetime.date.fromisoformat(f"{year}-{month}-{day}")
        return True
    except Exception as e:
        return False
    
def isValidAge(age) -> bool:
    try:
        age = int(age)
        if age >= 5 and age <= 80:
            return True
        else:
            return False
    except Exception as e:
        return False