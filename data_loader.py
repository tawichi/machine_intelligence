import torch
import numpy as np
import random
import pandas as pd
BATCH_SIZE = 4

# 乱数seedの固定
def fix_seed(seed):
    # random
    random.seed(seed)
    # numpy
    np.random.seed(seed)
    # pytorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


fix_seed(seed=42)

# データローダーのサブプロセスの乱数seedが固定
def worker_init_fn(worker_id):
    np.random.seed(np.random.get_state()[1][0] + worker_id)
# データセットの作成
class Mydataset(torch.utils.data.Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        cleaned_content = self.X[index]
        label = self.y[index]
        """
        前処理を書く
        現状はcleaned_contentには整形済みの文字列が入っている
        """
        return cleaned_content, label

train_X = pd.read_pickle("./pickle/train_X.pkl")
val_X = pd.read_pickle("./pickle/val_X.pkl")
test_X = pd.read_pickle("./pickle/test_X.pkl")
train_y = pd.read_pickle("./pickle/train_y.pkl")
val_y = pd.read_pickle("./pickle/val_y.pkl")
test_y = pd.read_pickle("./pickle/test_y.pkl")


train_dataset = Mydataset(train_X, train_y)
val_dataset = Mydataset(val_X, val_y)
test_dataset = Mydataset(test_X, test_y)


# データローダーの作成
train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=BATCH_SIZE, 
                                           shuffle=True,  # データシャッフル
                                           num_workers=2,  
                                           pin_memory=True,  
                                           worker_init_fn=worker_init_fn
                                           )
val_loader = torch.utils.data.DataLoader(val_dataset,
                                           batch_size=BATCH_SIZE,  
                                           shuffle=True,  
                                           num_workers=2, 
                                           pin_memory=True,
                                           worker_init_fn=worker_init_fn
                                           )
test_loader = torch.utils.data.DataLoader(test_dataset,
                                          batch_size=BATCH_SIZE,
                                          shuffle=False,
                                          num_workers=2,
                                          pin_memory=True,
                                          worker_init_fn=worker_init_fn
                                          )

# 動作確認
for data, label in train_loader:
    print(data, label)