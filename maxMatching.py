# encoding: utf-8
'''
@author: jinjin
@contact: cantaloupejinjin@gmail.com
@file: ForwardMatch.py
@time: 2019/10/19 21:16
'''
"""
中文分词：前向最大匹配+后向最大匹配
"""
dic = ["我们", "经常", "有", "有意见", "意见", "分歧", "意见分歧"]
sentence = "我们经常有意见分歧"
max_length = 5

def forwardMaxmatching(sentence):
    res = []
    sentence = sentence
    len_sentence = len(sentence)
    while len_sentence > 0:
        word = sentence[0:max_length]
        while word not in dic:
            if len(word) == 1:
                break
            word = word[0:len(word) - 1]
        res.append(word)
        sentence = sentence[len(word):]
        len_sentence = len(sentence)
    return res
print(forwardMaxmatching(sentence))

def backwordMaxmatching(sentence):
    res = []
    sentence = sentence
    len_sentence = len(sentence)
    while len_sentence > 0:
        word = sentence[-max_length:]
        while word not in dic:
            if len(word) == 1:
                break
            word = word[-(len(word) - 1):]
        res.append(word)
        sentence = sentence[:-len(word)]
        len_sentence = len(sentence)
    return res
print(backwordMaxmatching(sentence))
