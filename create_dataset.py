import os
import glob
import pickle
import random

def get_subfolders(folder_path):
    subfolders = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            subfolders.append(subfolder_path)
    return subfolders


# アノテーションのラベルのリストを6:2:2に分割 (train, val, testに分割するため)
def split_list(input_list, ratio= [6, 2, 2]):
    random.shuffle(input_list)
    total_len = len(input_list)
    
    len_1 = total_len * ratio[0] // sum(ratio)
    len_2 = total_len * ratio[1] // sum(ratio)
   
    part_1 = input_list[:len_1]
    part_2 = input_list[len_1:len_1+len_2]
    part_3 = input_list[len_1+len_2:]    
    return part_1, part_2, part_3


train_X = []
val_X = []
test_X = []
train_y = []
val_y = []
test_y = []
folder_path = "./sample"  
subfolders_list = get_subfolders(folder_path)

for subfolder in subfolders_list:
    with open(f"{subfolder}/labels.txt", "r", encoding="utf-8") as file:
        labels = file.read().split("\n")
        num_labels = len(labels)
        train_labels, val_labels, test_labels = split_list(labels)
        train_y.extend(train_labels)
        val_y.extend(val_labels)
        test_y.extend(test_labels)
    
    cleaned_txt_path = glob.glob(os.path.join(subfolder, "cleaned_transcription.txt"))
    if len(cleaned_txt_path) != 1:
        assert False, "txt_path must be one"
    with open(cleaned_txt_path[0], "r", encoding="utf-8") as file:
        cleaned_content = file.read()
    train_X.extend([cleaned_content] * len(train_labels))
    val_X.extend([cleaned_content] * len(val_labels))
    test_X.extend([cleaned_content]* len(test_labels))
    
# pickleで保存
with open("./pickle/train_X.pkl", "wb") as file:
    pickle.dump(train_X, file)
with open("./pickle/val_X.pkl", "wb") as file:
    pickle.dump(val_X, file)
with open("./pickle/test_X.pkl", "wb") as file:
    pickle.dump(test_X, file)
with open("./pickle/train_y.pkl", "wb") as file:
    pickle.dump(train_y, file)
with open("./pickle/val_y.pkl", "wb") as file:
    pickle.dump(val_y, file)
with open("./pickle/test_y.pkl", "wb") as file:
    pickle.dump(test_y, file)
   