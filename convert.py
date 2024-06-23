import xlsxwriter
import json


infile = open('out.json', 'r')
columns = ['ecode', 'price', 'status']

while True:
    jl = infile.readline()
    if not jl: break
    ja = json.loads(jl)
    for k in ja:
        if k not in columns:
            columns.append(k)










workbook = xlsxwriter.Workbook('result.xlsx')
cf = workbook.add_format({'align': 'center'})
money_format = workbook.add_format({'num_format': '#,##0.00[$ ₴]'})

worksheet = workbook.add_worksheet('Autoglass')





row = 0
col = 0

                       
ids = {}

for n, k in enumerate(columns):
    if k == 'ecode': k = "Еврокод"
    if k == 'price': k = "Цена"
    if k == 'status': k = "Наличие"
    worksheet.write(0, n, k, cf)

infile = open('out.json', 'r')

while True:
    
    jl = infile.readline()
    if not jl: break
    ja = json.loads(jl)

    ecode = ja['ecode']

    if ecode in ids:
        if jl == ids[ecode]:
            print('dup', ecode)
            continue
        else:
            print('not dup', ecode)

    ids[ecode] = jl


    row += 1
   
    for k in ja:
        n = columns.index(k)
        v = ja[k]
        if k == 'status': v = v.replace('\n', ' ')
        try:
            if k == 'price': v = float(v.replace('грн.', '').strip())
        except:
            pass

        try:
            if k == 'ecode': v = int(v.strip())
        except:
            pass


        worksheet.write(row, n, v, money_format if k == 'price' else None)
        






length_list = [10, 15, 30, 15, 15, 15, 20, 5, 20, 15, 15, 15, 15, 15, 15]
for i, width in enumerate(length_list):
    worksheet.set_column(i, i, width)












workbook.close()
print('result.xlsx saved')