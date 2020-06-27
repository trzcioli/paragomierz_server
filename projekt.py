from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import regex as re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Elem:
    name: str
    price: Optional[float]


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def find_first_digit(s):
    m = re.search(r"\d", s)
    if m:
        return m.start()


def take_price(s):
    m = re.findall(r"[^0-9][0-9]+,[0-9]+[^0-9]", s, overlapped=True)
    if m:
        comp = re.compile('[0-9]+,[0-9]+')
        res = comp.search(m[-1])
        return res.group()


def remove_empty_lines(text):
    res = []
    for t in text.split('\n'):
        if t != '':
            res.append(t)
    return res


def join_text_lines_with_prices(text):
    res = []
    idx = 0
    while idx < len(text):
        t = text[idx]
        if not has_numbers(t):
            line = t.rstrip()
            while not has_numbers(line):
                if text[idx + 1]:
                    line += text[idx + 1]
                    idx += 1
            res.append(line)
        else:
            res.append(t)
        idx += 1
    return res


def extract_names_and_prices(new_text):
    all_elems = []
    for x in new_text:
        first = find_first_digit(x)
        if first:
            name = x[0:first]
            price = take_price(x[first:])
            if price:
                elem = Elem(name, float(price.replace(',', '.')))
                all_elems.append(elem)
            else:
                elem = Elem(name, None)
                all_elems.append(elem)
        else:
            elem = Elem(x, None)
            all_elems.append(elem)
    return all_elems


def main(image):
    print(image)
    # co musze wziac pod uwage:  co jesli name lub price jest puste; co jesli price ma separator .
    gray = image
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(
        Image.open(filename), lang='pol', config='--psm 6')
    os.remove(filename)

    text_without_empty_lines = remove_empty_lines(text)

    text_join_lines = join_text_lines_with_prices(text_without_empty_lines)

    print(text_join_lines)

    all_elems = extract_names_and_prices(text_join_lines)

    return all_elems
