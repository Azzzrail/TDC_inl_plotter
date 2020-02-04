# coding=utf-8
from typing import List
import glob
import os
import sys
import numpy as np


from bokeh.plotting import figure, output_file, show
import itertools  # Для перебора цветов в графиках
from bokeh.palettes import Dark2_5 as palette # Палитра цветов для линий


import pandas as pd
import os
import sys


def make_paus(mode, message=""):
    if mode == 0:
        message = message + " Press <Enter> to continue or q to quit:"
        print(message)
        answer = sys.stdin.readline()
        if answer.lower() == "q":
            sys.exit(2)
        return answer


Channel = int(make_paus(0, "enter channel number"))

print(Channel)

i = 0
Data_arr: List[List[str]] = []
Channels: List[int] = []
line: str
filenames: List[str] = []
df = {}
pure_data = {}
df_w_names = {}
new_cols = {}
path = os.getcwd()
for filename in glob.iglob(path + '/**/TDC72VXS*.*', recursive=True):
    i += 1
    #if filename not in filenames:
    filenames.insert(i, filename)

j = 0
i: int = 0
line_names = []
files = []
print(filenames, "\n")
with open('filename.txt', "w") as g:
    for item in filenames:
        g.write("%s\n" % item)

while j < len(filenames):

    with open(filenames[j], "r") as f:

        data = f.readlines()

        df[j] = pd.read_csv(filenames[j], skipinitialspace=True, skiprows=1,  header=None, sep='[_]|[=]|[,]|\s+]', engine='python')
        # get length of df's columns
        num_cols = 1025 #len(list(df[j]))

        # generate range of ints for suffixes
        # with length exactly half that of num_cols;
        # if num_cols is even, truncate concatenated list later
        # to get to original list length
        rng = range(0, num_cols-1)

        new_cols = list(['Chan'] + [i for i in rng])
        df[j].columns = new_cols

        df[j] = df[j][df[j].Chan != 'stat']


    j += 1

#print(df[Channel])
print(filenames[1])
#df[Channel].loc[[0]].plot(legend=True) #plot usa column

t = 0
names = []
while t < len(filenames):
    name = os.path.basename(filenames[t])
    names.insert(t, name)
    t += 1

print("amount of names", names)

x: List[int] = []
i = 0
j: int = 0
Max_line = 0

output_file("log_lines.html")
# набор инструментов для работы с нарисованным графиком
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"
# create a new plot
p = figure(
   tools=TOOLS, width=1500, height=1000,
   y_axis_type="linear",  title="TDC72_INL",
   x_axis_label='buf_place', y_axis_label='counts'
          )

colors = itertools.cycle(palette)
print(df[0].loc[[Channel]])

for Max_line, color in zip(range(0, len(names)), colors):
    # print(p)
    p.line(x=range(1023), y=[float(i) for i in df[Max_line].loc[[Channel]]], legend=names[1], color=color)

#show(p)



