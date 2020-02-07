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
#import warnings
#warnings.filterwarnings("ignore", 'This pattern has match groups')

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
line: str
filenames: List[str] = []
df = {}
new_cols = {}
path = os.getcwd()
for filename in glob.iglob(path + '/**/TDC72VXS*.*', recursive=True):
    i += 1
    #if filename not in filenames:
    filenames.insert(i, filename)

j: int = 0
i: int = 0

with open('filename.txt', "w") as g:
    for item in filenames:
        g.write("%s\n" % item)

while j < len(filenames):

    df[j] = pd.read_csv(filenames[j], skipinitialspace=True, skiprows=1,  header=None, sep='[_]|[=]|[,]|\s+]', engine='python')
    # get length of df's columns
    num_cols = len(list(df[j]))

    # generate range of ints for suffixes
    # with length exactly half that of num_cols;
    # if num_cols is even, truncate concatenated list later
    # to get to original list length
    new_cols = list(['Ch'] + [i for i in range(0, num_cols-1)])
    df[j].columns = new_cols

    df[j] = df[j][df[j].Ch != 'stat']

    df[j]['Ch'] = pd.to_numeric(df[j]['Ch'])
    df[j] = df[j].set_index('Ch')
    df[j].index.names = [None]

#        df[j].index.astype(int)
#        df[j] = df[j].astype(float)

    j += 1

#print(filenames[1])
#df[Channel].loc[[0]].plot(legend=True) #plot usa column

t = 0
names = []
while t < len(filenames):
    name = os.path.basename(filenames[t])
    names.insert(t, name)
    t += 1

#print("amount of names", names)

#x: List[int] = []
i = 0
j: int = 0
Max_line = int(0)

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

for Max_line, color in zip(range(0, len(names)), colors):

    try:
        p.line(x=range(1024), y=[i for i in df[Max_line].loc[(Channel)]],
               legend_label=names[Max_line], color=color)
    except KeyError:
        continue

show(p)



