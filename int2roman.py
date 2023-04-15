'''
a snippet of code that translate integers into roman letters usin recursive function.
'''

roman = {'I':1,'IV':4,'V':5,'IX':9,'X':10,'XL':40,'L':50,'XC':90,'C':100,'CD':400, 'D':500,'CM':900,'M':1000}
#n = 0
rom = ' '
out = ''
def rekurs(n, out):

    res = 0
    for i,y in roman.items():
        if n >= y:
            res = y
            rom = i
    n -= res
    out = out + rom
    if n > 0:
        rekurs(n, out)
    else:
        print(f'integer \'{liczba}\' can be converse into roman letter \'{out}\'')

liczba = int(input('input integer that you want to converse into roman letter(s): '))
rekurs(liczba, '')
