# В файле dataset.txt содержатся пары чисел,
# соответствующие кадрам:
# первое число - количество людей, найденное алгоритмом
# второе число - истинное количество людей.
# Используя эти данные определим точность алгоритма

dataset_file = open('dataset.txt', 'r')
dataset_yolo = []
dataset_true = []
for line in dataset_file:
    yolo, ground_truth = map(int, line.split())
    dataset_yolo.append(yolo)
    dataset_true.append(ground_truth)
    
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print("Mean Squared Error:", mean_squared_error(dataset_true, dataset_yolo))
print("Root Mean Squared Error:", mean_squared_error(dataset_true, dataset_yolo)**0.5)
print("Mean Absolute Error:", mean_absolute_error(dataset_true, dataset_yolo))
