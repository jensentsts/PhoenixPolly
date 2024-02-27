# -*- coding: utf-8 -*-
# @Time    : 2024/2/26 20:45
# @Author  : jensentsts
# @File    : main.py
# @Description : 识别逆转裁判人物对话，并用默认语音朗读。
# ** 使用tesseract **
import time

import numpy as np
import torch
from PIL.Image import Image

import get_phoenix_wright
from polly import Polly

print('Cuda是否可用:', torch.cuda.is_available())
print('Cuda支持的设备数量:', torch.cuda.device_count())

little_polly = Polly()


def decode_dialog_tuple(dialogs: tuple[np.ndarray, np.ndarray]) -> str:
    return little_polly.read(dialogs[0]) + little_polly.read(dialogs[1])


if __name__ == '__main__':
    spoken_text = ''
    spoken_name = ''
    little_polly.say_hello()
    while True:
        time.sleep(0.05)
        name = little_polly.read(get_phoenix_wright.get_speaker_name())
        if spoken_name != name and len(name) != 0:
            little_polly.learn(name + '说')
        spoken_name = name

        text = decode_dialog_tuple(get_phoenix_wright.get_dialog_tuple())
        if spoken_text in text:
            little_polly.learn(text[len(spoken_text):])
        elif len(text) > 0:
            little_polly.learn(text)
        spoken_text = text
        little_polly.say()
