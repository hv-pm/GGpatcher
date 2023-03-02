# This is a sample Python script.
import os
from os import walk

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def generate(path, name : str):
    dir_path = rf'{path}'
    name = name
    if name == '':
        name = 'filelist'
    res = []
    for (dir_path, dir_names, file_names) in walk(dir_path):
        for x in file_names:
            size = os.stat(os.path.join(dir_path, x)).st_size
            tup = (x, size)
            res.append(tup)
    with open(f'{name}.txt', "w+", encoding="utf-8") as file:
        for i in range(len(res)):
            file.write(f'{res[i][0]},{res[i][1]}\n')


if __name__ == '__main__':
    folder_path = input('Path to update folder: ')
    if os.path.exists(folder_path) == True:
        name = input("Filelist name (leave blank for 'filelist.txt'):")
        generate(folder_path, name)
        input('Done, press [ENTER] to exit.')
    else:
        input('Path could not be found, press [ENTER] to exit.')
