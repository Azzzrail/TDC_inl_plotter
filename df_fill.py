import sys
import pandas as pd
import os

df = {}
names = []


def df_fill(filenames):
    j: int = 0

    while j < len(filenames):

        df[j] = pd.read_csv(filenames[j], skipinitialspace=True, skiprows=1, header=None, sep='[_]|[=]|[,]|s+]',
                            engine='python')  # Вычитываем файлы в датафрейм, пропуская первую строку, без имён столбцов
        # Разделители подобраны по тому, что есть в файле. Возможно, надо запилить ручной ввод разделителей.
        # get length of df's columns
        num_cols = 1025  # len(list(df[j])) Я знаю размер таблицы, поэтому число, но можно вычислить автоматом.
        # Но это не оптимальное решение
        df[j] = df[j].dropna()  # выкидываем строки с NaN в элементах
        df[j].columns = list([i for i in range(0, num_cols)])  # Создаю имена столцов - список с числами от 0 до 1025
        df[j] = df[j].set_index(0)  # Запихиваем нулевой столбец(номера каналов в файле) в индексы
        df[j].index = pd.to_numeric(
            df[j].index)  # Превращаем индексы из объектов в числа, чтобы можно было их итерировать
        df[j].index.names = [None]  # удаляем имя для индексов(там был 0 - номер столбца)
        name = os.path.basename(filenames[j])  # Вычленяем имя файла из полного пути к нему
        names.insert(j, name)  # Записываем в список, потом будем имена использовать в качестве легенды к линиям в плоте
        j += 1  # Записываем в список, потом будем имена использовать в качестве легенды к линиям в плоте

    return names, df
