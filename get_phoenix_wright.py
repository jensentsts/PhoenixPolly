# -*- coding: utf-8 -*-
# @Time    : 2024/2/26 21:05
# @Author  : jensentsts
# @File    : get_phoenix_wright.py
# @Description :
import cv2
import numpy as np
import pygetwindow
import pyautogui
from PIL import Image

PHOENIX_TITLE = 'Phoenix Wright'

DIALOG_TOP = 684
DIALOG_LEFT = 270
DIALOG_WIDTH = 920
DIALOG_HEIGHT = 188

SPEAKER_TOP = 645
SPEAKER_LEFT = 165
SPEAKER_WIDTH = 220
SPEAKER_HEIGHT = 46


def find_phoenix_wright() -> pygetwindow.Win32Window:
    """
    获取逆转裁判的窗口对象
    :return: 窗口对象
    """
    phoenix_windows = pygetwindow.getWindowsWithTitle(PHOENIX_TITLE)
    if len(phoenix_windows) == 0:
        raise WindowsError('未找到逆转裁判窗口。')
    return phoenix_windows[0]


def get_region_shot(rela_left: int, rela_top: int, rela_width: int, rela_height: int) -> Image.Image:
    """
    获取逆转裁判实时图像
    :return:
    """
    window = find_phoenix_wright()
    left, top, width, height = window.left, window.top, window.width, window.height
    return pyautogui.screenshot(region=(left + rela_left, top + rela_top, rela_width, rela_height))


def get_dialog_tuple() -> tuple[Image.Image, Image.Image]:
    """
    获取对话框中包含文字部分的截图
    :return: Image对象的对话框截图
    """

    def proces(img: Image.Image) -> Image.Image:
        img = np.array(img)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_hsv = cv2.GaussianBlur(img_hsv, (3, 3), 0)
        img_bin = cv2.inRange(img_hsv, np.array([0, 0, 200]), np.array([255, 255, 255]))
        img_can_medium = cv2.Canny(img_gray, 140, 240)
        # img_can_high = cv2.Canny(img_bin, 140, 220)
        res = img_bin
        res = cv2.addWeighted(res, 0.7, img_can_medium, 0.7, 0)
        # res = cv2.addWeighted(res, 1, img_can_high, 0.7, 0)
        res[0:20, 0:160] = 0  # 消除左上角的边框区域
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        counter = np.where(res > 160, 1, 0)
        from scipy import signal
        counter = signal.convolve2d(counter, kernel)
        res = np.where(counter >= 5, 255, 0)

        return Image.fromarray(res).convert('RGB')

    return (proces(get_region_shot(DIALOG_LEFT, DIALOG_TOP, DIALOG_WIDTH, int(DIALOG_HEIGHT / 2) + 8)),
            proces(get_region_shot(DIALOG_LEFT, DIALOG_TOP + int(DIALOG_HEIGHT / 2) - 12, DIALOG_WIDTH, int(DIALOG_HEIGHT / 2))))


def get_speaker_name() -> Image.Image:
    speaker_name = np.array(get_region_shot(SPEAKER_LEFT, SPEAKER_TOP, SPEAKER_WIDTH, SPEAKER_HEIGHT))
    speaker_grey = cv2.cvtColor(speaker_name, cv2.COLOR_BGR2HSV)
    speaker_binary = cv2.inRange(speaker_grey, np.array([0, 0, 224]), np.array([255, 255, 255]))
    return Image.fromarray(speaker_binary).convert('RGB')  # 转换为Image对象，并转换为RGB以便于调试和避免其它错误