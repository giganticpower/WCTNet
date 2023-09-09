import os
import random

# 设置数据集所在路径和保存txt文件的路径
data_dir = './train/Sat'
save_dir = '/data_1'

# 读取所有图片名称并打乱顺序
image_names = os.listdir(data_dir)
random.shuffle(image_names)

# 计算训练集、评估集和测试集的大小
num_images = len(image_names)
train_size = int(0.8 * num_images)
val_size = int(0.1 * num_images)

# 将图片名称分别写入训练集、评估集和测试集的txt文件中
with open(os.path.join(save_dir, 'train.txt'), 'w') as f:
    for image_name in image_names[:train_size]:
        f.write('{}\n'.format(image_name))

with open(os.path.join(save_dir, 'val.txt'), 'w') as f:
    for image_name in image_names[train_size:train_size+val_size]:
        f.write('{}\n'.format(image_name))

with open(os.path.join(save_dir, 'test.txt'), 'w') as f:
    for image_name in image_names[train_size+val_size:]:
        f.write('{}\n'.format(image_name))
