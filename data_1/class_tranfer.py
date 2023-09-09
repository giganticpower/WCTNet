import os

import numpy as np
from PIL import Image

import matplotlib.pyplot as plt


# 定义每个类别所对应的RGB颜色值
colors1 = {
    'urban_land': (0, 255, 255),   # 红色
    'agriculture_land': (255, 255, 0),   #
    'rangeland': (255, 0, 255),  #
    'forest_land': (0, 255, 0),   # 绿色
    'water': (0, 0, 255),    # 蓝色
    'barren_land': (255, 255, 255),    # black
    'unknown': (0, 0, 0)   # white色
}

colors2 = {
    'background': (0, 0, 0),   # white色
    'house': (255, 255, 255)    # black
}

def Label_generation(path, colors, save_dir):
    for ori_image in os.listdir(path):
        # 读取原始图片
        image = Image.open(os.path.join(path, ori_image))
        # 将原始图片转换为numpy数组
        image_array = np.array(image)

        # 新建一个与原始图片大小相同的numpy数组，用于保存类别标签
        label_array = np.zeros((image.height, image.width), dtype=np.uint8)

        # 遍历每个像素点并标记为对应的类别标签
        for i in range(image.height):
            for j in range(image.width):
                pixel = tuple(image_array[i, j])
                if colors == colors1:
                    if pixel == colors['urban_land']:
                        label_array[i, j] = 0
                    elif pixel == colors['agriculture_land']:
                        label_array[i, j] = 1
                    elif pixel == colors['rangeland']:
                        label_array[i, j] = 2
                    elif pixel == colors['forest_land']:
                        label_array[i, j] = 3
                    elif pixel == colors['water']:
                        label_array[i, j] = 4
                    elif pixel == colors['barren_land']:
                        label_array[i, j] = 5
                    elif pixel == colors['unknown']:
                        label_array[i, j] = 6
                elif colors == colors2:
                    if pixel == colors['background']:
                        label_array[i, j] = 0
                    elif pixel == colors['house']:
                        label_array[i, j] = 1
        # 将类别标签数组转换为PIL图片并保存
        label_image = Image.fromarray(label_array)
        label_image.save(save_dir + ori_image.split('.')[0] + '.png')
        print(ori_image.split('.')[0] + '.png')


def convert_images(input_folder, output_folder, colors):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            img = Image.open(input_path)
            img = img.convert("RGB")

            pixels = img.load()
            width, height = img.size

            for x in range(width):
                for y in range(height):
                    pixel = pixels[x, y]
                    value = pixel[0]  # Assuming pixel values are in the red channel

                    if value == 0:
                        pixels[x, y] = colors['urban_land']
                    elif value == 1:
                        pixels[x, y] = colors['agriculture_land']
                    elif value == 2:
                        pixels[x, y] = colors['rangeland']
                    elif value == 3:
                        pixels[x, y] = colors['forest_land']
                    elif value == 4:
                        pixels[x, y] = colors['water']
                    elif value == 5:
                        pixels[x, y] = colors['barren_land']
                    elif value == 6:
                        pixels[x, y] = colors['unknown']

            img.save(output_path)
            img.close()


def plot_pixel_distribution(image_path):
    img = Image.open(image_path)
    img = img.convert("L")  # Convert to grayscale for simplicity

    pixel_values = list(img.getdata())

    plt.hist(pixel_values, bins=7, range=(0, 7), density=True, color='blue', alpha=0.7)
    plt.xlabel('Pixel Value')
    plt.ylabel('Normalized Frequency')
    plt.title('Pixel Value Distribution')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    datase1_path = '/train/Label_ori/'
    datase2_path = '/train/Label_ori/'
    save1_dir = '/DeepGlobe/train/Label/'
    save2_dir = '/data_1/train/Label/'

    pred_dg = "/prediction_dg/"
    pred_dg_save = "/prediction_dg_vis/"

    # Label_generation(datase1_path, colors1, save1_dir)
    # convert_images(pred_dg, pred_dg_save, colors1)

    # 调用函数并指定图片路径
    image_path = "/data_1/DeepGlobe/train/Label/24813_mask.png"
    plot_pixel_distribution(image_path)


