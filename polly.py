# -*- coding: utf-8 -*-
# @Time    : 2024/2/27 0:05
# @Author  : jensentsts
# @File    : polly.py
# @Description : 文本阅读相关
# 真宵：是不是忘记了什么事？
# 小百合：别忘了DL-6号事件！


import easyocr
import win32com.client
from PIL.Image import Image

RATE = 4

tongue = win32com.client.Dispatch('SAPI.SpVoice')  # 相当于 speaker
tongue.Rate = RATE
tongue_buffer: str = ''
reader = easyocr.Reader(['ch_sim', 'en'], gpu=True, download_enabled=True)


def say_hello():
    tongue.Speak('小百合说：不可以忘记DL6号事件！')


def read(text_img: Image) -> str:
    text_img.save('./polly.png')
    try:
        return reader.readtext('./polly.png', paragraph=True, detail=False)[0]
    except Exception:
        return ''


def learn(text_data: Image | str, print_text: bool = True) -> str:
    """
    写入对话，内容为识别 dialogue_image 的结果；或者为一段纯文本。
    :param text_data: 含对话文本的 Image 图像对象。
    :param print_text: 是否打印识别结果
    :return: 返回识别的内容。如果 text_data 为 str ，则返回 text_data 中的内容。
    """
    global tongue_buffer
    text: str = ''
    if type(text_data) is Image:
        text = read(text_data)
    elif type(text_data) is str:
        text = text_data.replace(' ', '')

    if len(text) > 0:
        tongue_buffer += text
        if print_text:
            print('小百合：', text)

    return text


def say() -> None:
    """
    说出内容。
    ** Warning **: 使用前请调用 learn。
    :return: 无
    """
    global tongue_buffer
    tongue.Speak(tongue_buffer)
    tongue_buffer = ''


def forget():
    global tongue, tongue_buffer
    tongue = win32com.client.Dispatch('SAPI.SpVoice')
    tongue_buffer = ''
