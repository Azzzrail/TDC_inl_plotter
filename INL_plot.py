# coding=utf-8
import typing
import glob
import os
import numpy as np
import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as Palette  # Палитра цветов для линий
import itertools  # Для перебора цветов в графиках

import gui as gui  # импортируем самописный модуль gui
import cli_input as cli_i

# Chann = int(cli_i.cli_input(0, "enter channel number"))
Channel = gui.draw_gui()  # вызываем модуль gui, в котором обращаемся к функции draw_gui, она возвращает номер канала
i: int = 0
filenames: typing.List[str] = []
df = {}
names = []
path = os.getcwd()  # получаем путь до директории, где лежит скрипт и рядом лежат файлы данных
for filename in glob.iglob(path + '/**/TDC72VXS*.*', recursive=True):  # рекурсивно перебираем файлы в папках по шаблону
    i += 1
    # if filename not in filenames:
    filenames.insert(i, filename)  # И записываем имена файлов в список

j: int = 0
i = 0

with open('filename.txt', "w") as g:
    for item in filenames:
        g.write("%s\n" % item)  # Записываем имена файлов в текстовый файл
#names, df = df_fill(filenames)
while j < len(filenames):
    df[j] = pd.read_csv(filenames[j], skipinitialspace=True, skiprows=1, header=None, sep='[_]|[=]|[,]|s+]',
                        engine='python')  # Вычитываем файлы в датафрейм, пропуская первую строку, без имён столбцов
    # Разделители подобраны по тому, что есть в файле. Возможно, надо запилить ручной ввод разделителей.
    # get length of df's columns
    num_cols = 1025  # len(list(df[j])) Я знаю размер таблицы, поэтому число, но можно вычислить автоматом. Но это не
    # оптимальное решение
    df[j] = df[j].dropna()  # выкидываем строки с NaN в элементах
    df[j].columns = list([i for i in range(0, num_cols)])  # Создаю имена столцов - список с числами от 0 до 1025
    df[j] = df[j].set_index(0)  # Запихиваем нулевой столбец(номера каналов в файле) в индексы
    df[j].index = pd.to_numeric(df[j].index)  # Превращаем индексы из объектов в числа, чтобы можно было их итерировать
    df[j].index.names = [None]  # удаляем имя для индексов(там был 0 - номер столбца)

    name = os.path.basename(filenames[j])  # Вычленяем имя файла из полного пути к нему
    names.insert(j, name)  # Записываем в список, потом будем имена использовать в качестве легенды к линиям в плоте

    j += 1
output_file("log_lines.html")  # Создаём выходной файл с плотом
# набор инструментов для работы с нарисованным графиком
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select,crosshair,hover"
# create a new plot
p = figure(
    tools=TOOLS, width=1500, height=1000,
    y_axis_type="linear", title="TDC72_INL",
    x_axis_label='buf_place', y_axis_label='counts'  # TODO: Исправить неполное отображение имён в легенде
)

i = 0
j = 0
Max_line = int(0)
colors = itertools.cycle(Palette)

for Max_line, color in zip(range(0, len(names)), colors):

    try:  # Пытаемся нарисовать выбранный канал, итерируя датафреймы(файлы)
        output_file = p.line(x=range(1024), y=[i for i in df[Max_line].loc[Channel]],
                             legend_label=names[Max_line], color=color)
        print(names[Max_line])
    except KeyError:  # В случае появления номера канала, который отсутствует в таблице, обрабатываем возможную ошибку
        continue  # Делаем нихера, просто пропуская эту итерацию и ждём следующей.
    except NameError:
        break
        #  В случае, если нет ни одного канала в данных, получаем пустой плот

show(p)
