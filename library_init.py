#coding=utf-8
import cv2
import numpy as np
import pyshine as ps
import time
import random
import os

from gensim.models import word2vec
from matplotlib import pyplot as plt
from PIL import ImageFont, ImageDraw, Image
from ArticutAPI import Articut
from pprint import pprint
from random import choice
import pandas as pd






##取出要的詞性（POS.txt）
def load_POS():
    fp = open('POS.txt', "r")
    line = fp.readline()
    n=0 
    ## 用 while 逐行讀取檔案內容，直至檔案結尾
    POS = []
    while line:

        n+=1
        # print(n)
        # print(line)
        line = line.replace("\n", "")
        POS.append(line)

        line = fp.readline()
    print(POS)


    fp.close()
    
    return POS

    ##取不能換的詞（DoNotChange.txt）
def load_DoNotChange():
    fp = open('DoNotChange.txt', "r")
    line = fp.readline()
    n=0 
    ## 用 while 逐行讀取檔案內容，直至檔案結尾
    DoNotChange = []
    while line:

        n+=1
        # print(n)
        # print(line)
        line = line.replace("\n", "")
        DoNotChange.append(line)

        line = fp.readline()
    print(DoNotChange)


    fp.close()
    return DoNotChange

    ##取不好的詞（badword.txt）
def load_badword(): 
    fp = open('badword.txt', "r")
    line = fp.readline()
    n=0 
    ## 用 while 逐行讀取檔案內容，直至檔案結尾
    badword = []
    while line:

        n+=1
        # print(n)
        # print(line)
        line = line.replace("\n", "")
        badword.append(line)

        line = fp.readline()
    print(badword)


    fp.close()
    return badword

    ##取dataset（dataset.txt）
def load_dataset(): 
    fp = open('dataset.txt', "r")
    line = fp.readline()
    n=0 
    ## 用 while 逐行讀取檔案內容，直至檔案結尾
    dataset = []
    while line:

        n+=1
        # print(n)
        # print(line)
        line = line.replace("\n", "")
        dataset.append(line)

        line = fp.readline()
    # print(dataset)


    fp.close()
    return dataset

    ##取dataset（dataset.csv）
def load_dataset_csv(): 
    df = pd.read_csv('dataset.csv')
    return df
