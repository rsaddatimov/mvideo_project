# Объединить все .txt с количествами людей в один файл
import os

# Директория со всеми .txt файлами
dir_ = '...\\united_dataset\\'

fw = open('dataset.txt', 'w')
l = os.listdir(dir_)

# Идем по всем файлам в директории
for i in l:
    with open(dir_ + i, 'r') as fr:
        for k in fr:
            fw.write(k)
fw.close()
