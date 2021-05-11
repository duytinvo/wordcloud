#!/usr/bin/env python3
"""
Created on 5/5/2021
@Author: E977050
"""

import os
import sys
import argparse
import nltk
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


class WCBWC:
    stopword = set(STOPWORDS)
    @staticmethod
    def read_txt(txt_file, file_type="text"):
        with open(txt_file, "r") as f:
            if file_type == "text":
                text = f.read()
            else:
                text = {}
                for line in f:
                    k, v = line.strip().split("\t")
                    text[k] = float(v)
        return text

    @staticmethod
    def save_wc(text, filename='./data/wc_text.jpg'):
        stopword = set(STOPWORDS)
        wc = WordCloud(background_color="black", max_words=5000, stopwords=stopword)
        if type(text) == str:
            wc.generate(text)
        elif type(text) == dict:
            wc.generate_from_frequencies(text)
        else:
            raise Exception("Input type is incorrect")
        wc.to_file(filename)
        return wc

    @staticmethod
    def plot_wc(wc):
        plt.figure(figsize=(20, 10))
        plt.axis("off")
        plt.title("Word frequency", fontsize=20)
        plt.imshow(wc.recolor(colormap='viridis', random_state=17), alpha=0.98)
        plt.show()


if __name__ == '__main__':

    # text = WCBWC.read_txt("./data/freq.txt", file_type="freq")
    # wc = WCBWC.save_wc(text, './data/wc_freq.jpg')

    text = WCBWC.read_txt("./data/text.txt", file_type="text")
    wc = WCBWC.save_wc(text, './data/wc_text.jpg')
