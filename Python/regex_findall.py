import re


sentence = '\\frac{\\tan{4y}}{\\tan{6y}}'
goal = '( \\tan{4y} ) / ( \\tan{6y} )'

numerator = re.findall(r'(?<=frac\{).+(?=\}\{)', sentence)[0]
denominator = re.findall(r'(?<=\}\{).+(?=\})', sentence)[0]
_sentence = f'({numerator})/({denominator})'

print(_sentence)
