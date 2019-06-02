# -*- coding:utf-8 -*-
import text_image_maker
import glob
import re
import os


image_size = None#(224, 224)
crop_and_padding=None#(224,224)
font_size_list = list(range(12, 80))  # [font_size]
output_dir = "./gen"

#폰트경로
font_dir = "./fonts"#"/home/irelin/Downloads/korean_fonts_nodup"
#배경이미지 경로
bg_dir = "./bg"#"/home/irelin/Downloads/bgs"
#말뭉치 경로
text_dir = "./text"

#폰트별 이미지 갯수
nums_iter_per_font = 10

train_ratio = 0.9

bg_list = glob.glob(os.path.join(bg_dir, "*.jpg"))
font_list = glob.glob(os.path.join(font_dir, "*.ttf"))
text_file_list = glob.glob(os.path.join(text_dir, "*.txt"))
if os.name != 'nt':
    bg_list += glob.glob(os.path.join(bg_dir, "*.JPG"))
    font_list += glob.glob(os.path.join(font_dir, "*.TTF"))
    text_file_list += glob.glob(os.path.join(text_dir, "*.TXT"))

text_list = []
text_dict = {}
# 말뭉치에서 공백문자들로 split
for text_file in text_file_list:
    with open(text_file) as f:
        f.readline()
        for line in f:
            text_list += re.compile("\s+").split(line)[1:-2]

nums_iter_for_train = int(nums_iter_per_font * train_ratio)

text_image_maker.random_make_synthetic_images_with_texts(text_list, font_list, font_size_list, os.path.join(output_dir, "train"),
                                                         text_xy_range=[0.3, 0.5, 0.3, 0.7],
                                                         text_color_list="random",
                                                         # [text_color, (222, 222, 222), (123, 223, 211)],
                                                         bg_color_list="random",
                                                         # [bg_color, (222, 222, 231), (123, 223, 213)],
                                                         bg_list=bg_list,
                                                         padding_list=[-3],
                                                         # padding_list=[10, 15, 20],
                                                         nums_gen_iterate=nums_iter_for_train, use_multi_fonts_per_text=True,
                                                         use_binarize=False,
                                                         image_size=image_size, random_seed=None, use_cache=True,
                                                         back_fore_color_l1dist_limit=60, is_print=True,
                                                         crop_and_padding=crop_and_padding)

nums_iter_for_val = nums_iter_per_font - nums_iter_for_train

text_image_maker.random_make_synthetic_images_with_texts(text_list, font_list, font_size_list, os.path.join(output_dir, "val"),
                                                         text_xy_range=[0.3, 0.5, 0.3, 0.7],
                                                         text_color_list="random",
                                                         # [text_color, (222, 222, 222), (123, 223, 211)],
                                                         bg_color_list="random",
                                                         # [bg_color, (222, 222, 231), (123, 223, 213)],
                                                         bg_list=bg_list,
                                                         padding_list=[-3],
                                                         nums_gen_iterate=nums_iter_for_val, use_multi_fonts_per_text=True,
                                                         use_binarize=False,
                                                         image_size=image_size, random_seed=None, use_cache=True,
                                                         back_fore_color_l1dist_limit=60, is_print=True,
                                                         crop_and_padding=crop_and_padding)