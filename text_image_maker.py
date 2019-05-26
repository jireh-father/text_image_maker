# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import sys
import random
import time
import copy
import os

reload(sys)
sys.setdefaultencoding('utf-8')

im_cache = Image.new("RGB", (1, 1))
draw_cache = ImageDraw.Draw(im_cache)


def get_text_size(text, font):
    return draw_cache.textsize(text, font=font)


def random_make_synthetic_images_with_texts(text_list, font_list, font_size_list, output_dir,
                                            text_xy_range=[0.0, 0.5, 0.0, 0.7], text_color_list=["white"],
                                            bg_color_list=["black"], bg_list=None, padding_list=[10],
                                            nums_gen_iterate=100, use_multi_fonts_per_text=True, use_binarize=False,
                                            image_size=None, random_seed=None, use_cache=True, is_print=True,
                                            back_fore_color_l1dist_limit=30, crop_and_padding=(224, 224)):
    random.seed(random_seed)
    print("start")
    dir_names = []
    dir_paths = []
    for tmp_font_path in font_list:
        dir_path = os.path.join(output_dir, os.path.splitext(os.path.basename(tmp_font_path))[0])
        dir_name = os.path.splitext(os.path.basename(tmp_font_path))[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        dir_names.append(dir_name)
        dir_paths.append(dir_path)

    if use_cache and bg_list is not None:
        bg_list_cache = []
        for bg in bg_list:
            try:
                bg_list_cache.append(Image.open(bg).convert("RGB"))
            except:
                print("image open error", bg)
                continue
        bg_list = bg_list_cache

    x_range = list(range(int(text_xy_range[0] * 10), int(text_xy_range[1] * 10) + 1))
    y_range = list(range(int(text_xy_range[2] * 10), int(text_xy_range[3] * 10) + 1))

    if use_multi_fonts_per_text:
        for i in range(nums_gen_iterate):
            text = random.sample(text_list, 1)[0]

            if text == "":
                print("empty text. skip.")
                continue

            for j, font_path in enumerate(font_list):
                if is_print:
                    print("create image - font: %s, text: %s, iter: %d/%d" % (dir_names[j], text, i, nums_gen_iterate))
                output_path = os.path.join(dir_paths[j], "%s_%d.jpg" % (dir_names[j], i))
                font_size, text_color, bg_color, bg_path, text_xy, padding = _random_sample(font_size_list,
                                                                                            text_color_list,
                                                                                            bg_list, bg_color_list,
                                                                                            text_xy_range, x_range,
                                                                                            y_range, padding_list)
                make_synthetic_image_with_text(text, font_path, font_size, text_xy=text_xy, text_color=text_color,
                                               bg_color=bg_color, padding=padding, image_size=image_size,
                                               output_path=output_path, bg_path=bg_path, use_binarize=use_binarize,
                                               use_cache=use_cache,
                                               back_fore_color_l1dist_limit=back_fore_color_l1dist_limit,
                                               crop_and_padding=crop_and_padding)
    else:
        for i in range(nums_gen_iterate):
            text = random.sample(text_list, 1)[0]
            if text == "":
                print("empty text. skip.")
                continue
            font_idx = random.randint(0, len(font_list) - 1)
            font_path = font_list[font_idx]
            if is_print:
                print("create image - font: %s, text: %s, iter: %d/%d" % (
                    dir_names[font_idx], text, i, nums_gen_iterate))
            output_path = os.path.join(dir_paths[font_idx], "%s_%d.jpg" % (dir_names[font_idx], i))
            font_size, text_color, bg_color, bg_path, text_xy, padding = _random_sample(font_size_list, text_color_list,
                                                                                        bg_list, bg_color_list,
                                                                                        text_xy_range, x_range, y_range,
                                                                                        padding_list)
            make_synthetic_image_with_text(text, font_path, font_size, text_xy=text_xy, text_color=text_color,
                                           bg_color=bg_color, padding=padding, image_size=image_size,
                                           output_path=output_path, bg_path=bg_path, use_binarize=use_binarize,
                                           use_cache=use_cache,
                                           back_fore_color_l1dist_limit=back_fore_color_l1dist_limit,
                                           crop_and_padding=crop_and_padding)
    print("end")
    random.seed(None)


def _random_sample(font_size_list, text_color_list, bg_list, bg_color_list, text_xy_range,
                   x_range, y_range, padding_list):
    font_size = random.sample(font_size_list, 1)[0]
    if isinstance(text_color_list, str):
        text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        text_color = random.sample(text_color_list, 1)[0]

    if bg_list is not None:
        if random.randint(0, 1) == 0:
            if isinstance(bg_color_list, str):
                bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            else:
                bg_color = random.sample(bg_color_list, 1)[0]
            bg_path = None
        else:
            bg_color = None
            bg_path = random.sample(bg_list, 1)[0]
    else:
        bg_color = None
        bg_path = random.sample(bg_list, 1)[0]

    if text_xy_range is None:
        text_xy = None
    else:
        x = random.sample(x_range, 1)[0] * 0.1
        y = random.sample(y_range, 1)[0] * 0.1
        text_xy = [x, y]

    padding = random.sample(padding_list, 1)[0]
    rand_padding = {}
    padding_margin = 10
    rand_padding["left"] = random.randint(padding - padding_margin, padding + padding_margin)
    rand_padding["top"] = random.randint(padding - padding_margin, padding + padding_margin)
    rand_padding["right"] = random.randint(padding - padding_margin, padding + padding_margin)
    rand_padding["bottom"] = random.randint(padding - padding_margin, padding + padding_margin * 2)

    return font_size, text_color, bg_color, bg_path, text_xy, rand_padding


def make_synthetic_image_with_text(text, font_path, font_size, text_xy=None, text_color="white", bg_color="black",
                                   padding={"left": 5, "top": 5, "right": 5, "bottom": 5}, image_size=None,
                                   output_path=None, bg_path=None, use_binarize=False,
                                   use_cache=True, back_fore_color_l1dist_limit=30, crop_and_padding=(224, 224)):
    mode = "RGB"
    if bg_path is None and isinstance(bg_color, str) and isinstance(text_color, str) and text_color == bg_color:
        print("skip same string color", bg_color)
        return False

    if bg_path is None and not isinstance(bg_color, str) and not isinstance(text_color, str):
        color_d = abs(bg_color[0] - text_color[0]) + abs(bg_color[1] - text_color[1]) + abs(bg_color[2] - text_color[2])
        if color_d < back_fore_color_l1dist_limit:
            print("skip same color", bg_color, text_color)
            return False

    text = unicode(text)

    font = ImageFont.truetype(font_path, font_size)
    try:
        w, h = get_text_size(text, font)
    except:
        print("failed to get text size", font_path)
        return False
    if bg_path is None:
        if image_size is None:
            im = Image.new(mode, (w + padding["left"] + padding["right"], h + padding["top"] + padding["bottom"]),
                           bg_color)
        else:
            im = Image.new(mode, image_size, bg_color)
    else:
        if use_cache:
            im = copy.deepcopy(bg_path)
        else:
            try:
                im = Image.open(bg_path).convert(mode)
            except:
                print("image open error",)
                return False

    W, H = im.size
    if bg_path is None:
        if image_size is None:
            w_pad = (padding["left"] + padding["right"]) // 2
            h_pad = (padding["top"] + padding["bottom"]) // 2
            text_xy = (int(0 + w_pad), int(0 + h_pad))
        else:
            text_xy = (int((W - w) // 2), int((H - h) // 2))
    else:
        if text_xy is None:
            text_xy = (int((W - w) // 2), int((H - h) // 2))
        else:
            text_xy = (int(text_xy[0] * W), int(text_xy[1] * H))

        if image_size is not None:
            if image_size[0] > W or image_size[1] > H:
                return False
            x_center = text_xy[0] + w // 2
            y_center = text_xy[1] + h // 2
            left = x_center - image_size[0] // 2
            top = y_center - image_size[1] // 2
            right = x_center + image_size[0] // 2
            bottom = y_center + image_size[1] // 2
            if right > W:
                left -= (right - W)
                right = W
            if left < 0:
                right += abs(left)
                left = 0
            if bottom > H:
                top -= (bottom - H)
                bottom = H
            if top < 0:
                bottom += abs(top)
                top = 0
            if left < 0:
                left = 0
            if right > W:
                right = W
            if top < 0:
                top = 0
            if bottom > H:
                bottom = H
        else:
            left = text_xy[0] - padding["left"]
            top = text_xy[1] - padding["top"]
            right = text_xy[0] + w + padding["right"]
            bottom = text_xy[1] + h + padding["bottom"]

    draw = ImageDraw.Draw(im)
    draw.text(text_xy, text, font=font, fill=text_color)

    if bg_path is not None:
        im = im.crop((left, top, right, bottom))

    if crop_and_padding is not None:
        bg_im = Image.new(mode, crop_and_padding, "black")
        x = crop_and_padding[0] // 2 - (w + padding["left"] + padding["right"]) // 2
        y = crop_and_padding[1] // 2 - (h + padding["top"] + padding["bottom"]) // 2
        bg_im.paste(im, (x, y))
        im = bg_im

    if use_binarize:
        img = np.array(im)
        img = img[:, :, ::-1].copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret2, img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if output_path is None:
            return img
        else:
            cv2.imwrite(output_path, img)
    else:
        if output_path is None:
            img = np.array(im)
            img = img[:, :, ::-1].copy()
            return img
        else:
            im.save(output_path, format="JPEG", subsampling=0, quality=100)
