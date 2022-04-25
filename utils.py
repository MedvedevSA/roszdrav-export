import re
import csv

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

legend = {
    "А": "A",
    "В": "B",
    "Е": "E",
    "К": "K",
    "М": "M",
    "Н": "H",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
    "У": "Y",
    "Х": "X",
}

def translit (word : str, dic : dict):
    for idx, char in enumerate(word):
        for i, j in dic.items():
            word = word.replace(i, j)
    return word

def import_1c(file_name):
    if(not file_name):
        root = tk.Toplevel()
        root.withdraw()
        mb.showerror("Внимание","Не указан файл откуда выгружать.")
        return
    # 01.01.01.01
    p1 = r'\d{2}.\d{2}.\d{2}.\d{2}'
    p1 = re.compile(p1)

    #Патерн наименование детали
    p2 = r'\s([A-Z]{1}[-.0-9A-ZА-Я]{1,})'
    p2 = re.compile(p2)

    #Патенрн расходная накладная
    p3 = r'\s(\d{3,4})'
    p3 = re.compile(p3)
    
    
    #(Партия) (дата)
    #(УПД) (ДАТА)
    p4 = r'(\d{2,3})[\s\S]*(\d{2}.\d{2}.\d{4})'
    p4 = re.compile(p4)

    #file_name = '1c.csv'
    arr = []
    with open(file_name, "r", encoding='utf-8') as f:
        sheet = csv.reader(f, delimiter=';')
        sheet = [ row for row in sheet]


    del sheet[0:3]

    data = list()
    el = dict()

    for idx, row in enumerate(sheet):
        try :
            if row[1] == 'шт':
                name = p2.findall(row[0])[0]
                el['name'] = translit(name, legend)
        
            elif 'name' in el.keys() and 'bach' not in el.keys():
                bach, date = p4.findall(row[0])[0]
                el['bach'] = bach
                el['dt_manufacture'] = date

            elif 'id_no' in el.keys():
                data.append(el.copy())
                no, dt = p4.findall(row[0])[0]
                try :
                    quantity = str(
                        int(
                            row[2].split('.')[0]
                    ))
                except:
                    quantity = row[2]
                el['quantity'] = quantity
                el['id_no'] = no
                el['id_dt'] = dt

            elif 'bach' in el.keys() and 'id_no' not in el.keys() :
                no, dt = p4.findall(row[0])[0]

                try :
                    quantity = str(
                        int(
                            row[2].split('.')[0]
                    ))
                except:
                    quantity = row[2]
                el['quantity'] = quantity
                el['id_no'] = no
                el['id_dt'] = dt
        
            if idx + 1 < len(sheet) and sheet[idx+1][1] != "":
                if el :
                    data.append(el)
                el = dict()
        except :
            el = {}

    return data



