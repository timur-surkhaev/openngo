# exec(open('make_dataset.py', encoding = 'UTF-8').read())

# Извлекает переменные из базы, представленной набором json-файлов.
# База и её спецификация: https://openngo.ru/opendata/ [15.02.2020]

# Скрипт незатейливо проходит по каждому файлу, извлекает из него искомые поля 
# и собирает их в итоговый датафрейм ngo_df. Затем фильтрует данные по Саратовской
# области и сохраняет в csv. 

# Вход: 15 json-файлов полной базы openngo.
# Выход: csv-файл c отобранными переменными и фильтарцией по Саратовской области.


import json
import pandas as pd

numbers = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
           '11', '12', '13', '14', '15']

#numbers = ['01']

ngos_min = []
for number in numbers: 
    ngos = []
    filename = 'ngo_dump_' + number + '.json'
    
    print(filename)
    with open(filename, 'r', encoding = 'UTF-8') as json_file:
        for i,line in enumerate(json_file):
            ngos.append(json.loads(line))
            if i % 5000 == 0:
                print('Line ', str(i))     
        print('Total: ', str(len(ngos)))

      
    for ngo in ngos: 
        # ИНН
        try:
            inn = ngo['inn']
        except:
            inn = None
        
        
        # Полное название
        try:    
            fullName = ngo['fullName']
        except:
            fullName = None
        
        # Тип ОПФ
        try:
            opfType = ngo['opfType']
        except:
            opfType = None
        
        # Сборка ОКВЭДов
        try:
            mainOkved = ngo['mainOkved']['code'] + ' ' + ngo['mainOkved']['name'] + '\n'
        except:
            mainOkved = ''
        
        try:
            addOkved = ngo['addOkved']
            if addOkved:
                addOkveds = [okved['code']+' '+okved['name']+'\n' for okved in addOkved]
            else:
                addOkveds = ''
        except:
            addOkveds = ''
        
        if mainOkved or addOkved:
            allOkveds = mainOkved + ''.join(addOkveds)
        else:
            allOkveds = None
        
        # Тип основателей
        try:
            foundersType = ngo['foundersType']
        except:
            foundersType = None
        
        
        # Регион
        try:
            regionName = ngo['regionName']
        except:
            regionName = None
        
        # Статус из ЕГРЮЛ
        try:
            egrulStatus = ngo['egrulStatus']
        except:
            egrulStatus = None
            
        ngos_min.append({'inn':inn,
                         'fullName':fullName, 
                         'opfType':opfType,
                         'foundersType':foundersType,
                         'allOkveds':allOkveds,
                         'regionName':regionName,
                         'egrulStatus':egrulStatus})    


ngo_df = pd.DataFrame(ngos_min)
ngo_df[ngo_df['regionName'] =='Саратовская область'].to_csv('saratovsk_v1.csv', encoding = 'UTF-8', index = False)



