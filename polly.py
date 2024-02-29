# -*- coding: utf-8 -*-
# @Time    : 2024/2/27 0:05
# @Author  : jensentsts
# @File    : polly.py
# @Description : 文本阅读相关
# 真宵：是不是忘记了什么事？
# 小百合：别忘了DL-6号事件！

import easyocr
import win32com.client
import numpy as np
from PIL.Image import Image


RATE = 5


class Polly:

    tongue = win32com.client.Dispatch('SAPI.SpVoice')  # 相当于 speaker
    tongue.Rate = RATE
    tongue_buffer: str = ''
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, download_enabled=True)

    def say_hello(self):
        self.tongue.Speak('小百合说：不可以忘记DL6号事件！')

    def read(self, text_img: np.ndarray) -> str:
        try:
            return self.reader.readtext(text_img, paragraph=True, detail=False)[0]
        except Exception:
            return ''

    def learn(self, text_data: Image | str, print_text: bool = True) -> str:
        """
        写入对话，内容为识别 dialogue_image 的结果；或者为一段纯文本。
        :param text_data: 含对话文本的 Image 图像对象。
        :param print_text: 是否打印识别结果
        :return: 返回识别的内容。如果 text_data 为 str ，则返回 text_data 中的内容。
        """
        text: str = ''
        if type(text_data) is Image:
            text = self.read(text_data)
        elif type(text_data) is str:
            text = text_data.replace(' ', '')

        if len(text) > 0:
            self.tongue_buffer += text
            if print_text:
                print('小百合：', text)

        return text

    def say(self) -> None:
        """
        说出内容。
        ** Warning **: 使用前请调用 learn。
        :return: 无
        """
        self.tongue.Speak(self.tongue_buffer)
        self.tongue_buffer = ''

    def forget(self) -> None:
        """
        初始化
        :return:
        """
        self.tongue = win32com.client.Dispatch('SAPI.SpVoice')
        self.tongue.Rate = RATE
        self.tongue_buffer = ''
        self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=True, download_enabled=True)
