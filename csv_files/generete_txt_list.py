import os

train_file = open('/home/chase/DataSets/steel_bar/ImageSets/Main/train.txt', 'w')
test_file = open('/home/chase/DataSets/steel_bar/ImageSets/Main/test.txt', 'w')
for _, _, train_files in os.walk('/home/chase/DataSets/steel_bar/train_dataset'):
    continue
for _, _, test_files in os.walk('/home/chase/DataSets/steel_bar/test_dataset'):
    continue
for file in train_files:
    train_file.write(file.split('.')[0] + '\n')

for file in test_files:
    test_file.write(file.split('.')[0] + '\n')