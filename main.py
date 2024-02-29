# -*- coding: utf-8 -*-
# @Time    : 2024/2/26 20:45
# @Author  : jensentsts
# @File    : main.py
# @Description : 识别逆转裁判人物对话，并用默认语音朗读。

import time

import numpy as np
from PIL import Image
import torch

import get_phoenix_wright
from polly import Polly

# print('Cuda是否可用:', torch.cuda.is_available())
# print('Cuda支持的设备数量:', torch.cuda.device_count())

little_polly = Polly()


def decode_dialog_tuple(dialogs: tuple[np.ndarray, np.ndarray]) -> str:
    Image.fromarray(dialogs[0]).save('0.png')
    Image.fromarray(dialogs[1]).save('1.png')
    return little_polly.read(dialogs[0]) + little_polly.read(dialogs[1])


def get_stable_dialog() -> tuple[np.ndarray, np.ndarray]:
    dialogs: tuple[np.ndarray, np.ndarray] = get_phoenix_wright.get_dialog_tuple()
    for i in range(0, 50):  # 到50强制返回结果，防止光线枪、持续砸桌子……
        time.sleep(0.05)
        dialogs_cur: tuple[np.ndarray, np.ndarray] = get_phoenix_wright.get_dialog_tuple()
        if dialogs[0].all() == dialogs_cur[0].all() and dialogs[1].all() == dialogs_cur[1].all():
            for j in range(0, 5):
                time.sleep(0.05)
                dialogs_cur = get_phoenix_wright.get_dialog_tuple()
                if dialogs[0].all() == dialogs_cur[0].all() and dialogs[1].all() == dialogs_cur[1].all():
                    return dialogs_cur
                else:
                    break
        dialogs = dialogs_cur
    return dialogs


if __name__ == '__main__':
    spoken_text = ''
    spoken_name = ''
    little_polly.say_hello()
    while True:
        # time.sleep(0.1)
        """        
        name = little_polly.read(get_phoenix_wright.get_speaker_name())
        if spoken_name != name and len(name) != 0:
            little_polly.learn(name + '说')
        spoken_name = name
        """
        text = decode_dialog_tuple(get_stable_dialog())
        if spoken_text in text:
            little_polly.learn(text.replace(spoken_text, ''))
        elif len(text) > 0:
            little_polly.learn(text)
        spoken_text = text
        little_polly.say()
