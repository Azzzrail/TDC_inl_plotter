# coding=utf-8
import typing
import glob
import os
import numpy as np


from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as Palette  # Палитра цветов для линий
import itertools  # Для перебора цветов в графиках

import gui as gui  # импортируем самописные модули
import cli_input as cli_i
import df_fill as df_fill

# Chann = int(cli_i.cli_input(0, "enter channel number"))
Channel = gui.draw_gui()  # вызываем модуль gui, в котором обращаемся к функции draw_gui, она возвращает номер канала
i: int = 0
filenames: typing.List[str] = []

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

names, df = df_fill.df_fill(filenames)

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
    except KeyError:  # В случае появления номера канала, который отсутствует в таблице, обрабатываем возможную ошибку
        continue  # Делаем нихера, просто пропуская эту итерацию и ждём следующей.
    except NameError:
        break
        #  В случае, если нет ни одного канала в данных, получаем пустой плот
show(p)
