# coding=utf-8
from typing import List
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import os
import sys
from matplotlib.font_manager import FontProperties


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

Channel = 0##int(sys.stdin.readline())

i = 0
Data_arr: List[List[str]] = []
Channels: List[int] = []
line: str
filenames: List[str] = []

path = os.getcwd()
print(path)
for filename in glob.glob(path + '*.ini'):
    i += 1
    filenames.insert(i, filename)
print(filenames)
j = 0
i: int = 0
line_names = []
files = []

while Channel <= 15:

    with open("tqdc.ini", "r") as f:

        data = f.readlines()
        for line in data:
            if ((line[0] + line[1]).isdigit() and int(line[0]+line[1]) == Channel) or \
                    (line[0].isdigit() and int(line[0]) == Channel and line[1] == "="):

                print(line)
                remove_equ = line.replace("=", ", ")

                remove_comma = remove_equ.replace(",", " ")
                lines = remove_comma.split()
                Data_arr.insert(i, lines)
                files = Data_arr[i].pop(0)
                line_names.insert(j, str(Channel))
                print()
                i += 1
                Channel += 1
    j += 1

t = 0
names = []
while t < len(line_names):
    name = os.path.basename(line_names[t])
    names.insert(t, name)
    ##print(names)

    t += 1

x: List[int] = []
i = 0
j: int = 0

fig, ax = plt.subplots()
Max_line = 0


fontP = FontProperties()
fontP.set_size('small')

while Max_line < len(names):

    mpl.rcParams['lines.linewidth'] = 0.1
    plot_line = plt.plot([float(i) for i in Data_arr[Max_line]], label=names[Max_line])
    Max_line += 1

lgd = plt.legend(names,  bbox_to_anchor=(0, 0, 0.5, 0.7), bbox_transform=plt.gcf().transFigure, prop=fontP)

plt.savefig("TQDC" + str(Max_line) + ".pdf", dpi=6000, format="pdf")

plt.show()
