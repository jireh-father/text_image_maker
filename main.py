# -*- coding:utf-8 -*-
import text_image_maker
import json
import os
import glob
import re

image_size = None#(224, 224)
text_color = "black"
bg_color = "white"
font_size_list = list(range(12, 80))  # [font_size]
output_dir = "gen"
font_dir = "fonts"
bg_dir = "D:\\bgs"
text_dir = "text"

bg_list = glob.glob(os.path.join(bg_dir, "*.jpg"))
font_list = glob.glob(os.path.join(font_dir, "*.ttf"))
text_file_list = glob.glob(os.path.join(text_dir, "*.txt"))
text_list = []
text_dict = {}
for text_file in text_file_list:
    with open(text_file) as f:
        f.readline()
        for line in f:
            text_list += re.compile("\s+").split(line)[1:-2]

text_image_maker.random_make_synthetic_images_with_texts(text_list, font_list, font_size_list, output_dir,
                                                         text_xy_range=[0.3, 0.5, 0.3, 0.7],
                                                         text_color_list="random",
                                                         # [text_color, (222, 222, 222), (123, 223, 211)],
                                                         bg_color_list="random",
                                                         # [bg_color, (222, 222, 231), (123, 223, 213)],
                                                         bg_list=bg_list,
                                                         padding_list=[10, 15, 20],
                                                         nums_gen_iterate=1000, use_multi_fonts_per_text=True,
                                                         use_binarize=False,
                                                         image_size=image_size, random_seed=None, use_cache=True,
                                                         back_fore_color_l1dist_limit=60, is_print=True,
                                                         crop_and_padding=(224,224))
