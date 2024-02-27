# -*- coding: utf-8 -*-
# @Time    : 2024/2/26 20:45
# @Author  : jensentsts
# @File    : main.py
# @Description : 识别逆转裁判人物对话，并用默认语音朗读。
# ** 使用tesseract **
import time

import torch

print(torch.cuda.device_count())
print(torch.cuda.is_available())

from PIL.Image import Image

import get_phoenix_wright
import polly


def decode_dialog_tuple(dialogs: tuple[Image, Image]) -> str:
    return polly.read(dialogs[0]) + polly.read(dialogs[1])


if __name__ == '__main__':
    spoken_text = ''
    spoken_name = ''
    polly.say_hello()
    while True:
        time.sleep(0.02)
        name = polly.read(get_phoenix_wright.get_speaker_name())
        if spoken_name != name and len(name) != 0:
            polly.learn(name + '说')
        spoken_name = name

        text = decode_dialog_tuple(get_phoenix_wright.get_dialog_tuple())
        if spoken_text in text:
            polly.learn(text[len(spoken_text):])
        elif len(text) > 0:
            polly.learn(text)
        spoken_text = text
        polly.say()
