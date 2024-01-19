import pandas as pd


def del_nan(list_name):
    L1 = [item for item in list_name if not (pd.isnull(item)) is True]
    L1, list_name = list_name, L1
    return list_name
