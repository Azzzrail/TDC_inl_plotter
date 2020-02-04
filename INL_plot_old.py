# coding=utf-8
from typing import List
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import os
import sys
from matplotlib.font_manager import FontProperties
import plotly.graph_objects as go

def make_paus(mode, message=""):
    if mode == 0:
        message = message + " Press <Enter> to continue or q to quit:"
        print(message)
        ch = sys.stdin.readline()
        answer = sys.stdin.readline()

        answer = answer.strip("\n\t")
        if answer.lower() == "q":
            sys.exit(2)
        return ch


print("Enter channel number")

Channel = int(sys.stdin.readline())

i = 0
Data_arr: List[List[str]] = []
Channels: List[int] = []
line: str
filenames: List[str] = []

path = os.getcwd()
#print(path)
for filename in glob.iglob(path + '/**/TDC72VXS*.ini', recursive=True):
    i += 1
    #if filename not in filenames:
    filenames.insert(i, filename)

j = 0
i: int = 0
line_names = []
files = []
#print(filenames, "\n")
with open('filename.txt', "w") as g:
    for item in filenames:
        g.write("%s\n" % item)

while j < len(filenames):

    with open(filenames[j], "r") as f:

        data = f.readlines()
        for line in data:
            if ((line[0] + line[1]).isdigit() and int(line[0]+line[1]) == Channel) or \
                    (line[0].isdigit() and int(line[0]) == Channel and line[1] == "="):


                remove_equ = line.replace("=", ", ")

                remove_comma = remove_equ.replace(",", " ")
                lines = remove_comma.split()
                Data_arr.insert(i, lines)
                files = Data_arr[i].pop(0)
                line_names.insert(j, filenames[j])

                i += 1
    j += 1

t = 0
names = []
while t < len(line_names):
    name = os.path.basename(line_names[t])
    names.insert(t, name)
    t += 1

print(names)

x: List[int] = []
i = 0
j: int = 0

ax = plt.subplots()
Max_line = 0


fontP = FontProperties()
fontP.set_size('small')


fig = go.Figure()


while Max_line < len(names):
    fig.add_trace(go.Scatter(x=list(range(1024)), y=[float(i) for i in Data_arr[Max_line]], mode='lines',
                             name=names[Max_line]))

    mpl.rcParams['lines.linewidth'] = 0.1
    plot_line = plt.plot([float(i) for i in Data_arr[Max_line]], label=names[Max_line])
    Max_line += 1

lgd = plt.legend(names,  bbox_to_anchor=(0, 0, 0.5, 0.5), bbox_transform=plt.gcf().transFigure, prop=fontP)

plt.savefig("test" + str(Max_line) + ".pdf", dpi=6000, format="pdf")

plt.show()
fig.show()