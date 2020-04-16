# Объединить все .txt с количествами людей в один файл


import os

# Директория со всеми .txt файлами
dir_ = '...\\united_dataset\\'

# Список всех файлов в директории
file_list = os.listdir(dir_)

# Выходной файл с объединенными количествами
output_file = open('dataset.txt', 'w')

# Идем по всем файлам в директории
for file_ in file_list:
    with open(dir_ + file_, 'r') as fr:
        for k in fr:
            output_file.write(k)
output_file.close()
