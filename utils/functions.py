import pandas as pd


def del_nan(list_name):
    L1 = [item for item in list_name if not (pd.isnull(item)) is True]
    L1, list_name = list_name, L1
    return list_name

def get_unique_only(st):
    # Empty list
    lst1 = []
    count = 0
    # traverse the array
    for i in st:
        if i != 0:
            if i not in lst1:
                count += 1
                lst1.append(i)
    return lst1

# Функция "обрезки" строки до нужного символа
def cut_list(lstt_act):
    last_act = []
    for lst_act in lstt_act:
        try:
            if lst_act != 'nan':
                last_act.append(lst_act.partition(' (')[0])
        except AttributeError:
            continue
    return last_act
