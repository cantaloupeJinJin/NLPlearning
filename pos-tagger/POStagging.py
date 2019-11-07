# encoding: utf-8
'''
@author: jinjin
@contact: cantaloupejinjin@gmail.com
@file: POStagging.py
@time: 2019/11/3 14:29
'''

tag2id, id2tag = {}, {}#maps tag to id. tag2id:{"VB":0,..} id2tag:{0:"VB",1:"NNP"}
word2id, id2word = {}, {} #maps word to id
for line in open('traindata.txt'):
    items = line.split('/')#抽取每一行里的单词和词性
    word, tag = items[0], items[1].rstrip()#rstrip()去掉换行符
    if word not in word2id:
        word2id[word] = len(word2id)#给定下标
        id2word[len(id2word)] = word
    if tag not in tag2id:
        tag2id[tag] = len(tag2id)
        id2tag[len(id2tag)] = tag
M = len(word2id)#M：词典的大小、# of words
N = len(tag2id) #:词性的种类个数、# of tags
#构建 Π，A,B，参见有道笔记-词性标注
import numpy as np
pi = np.zeros(N)#每个词性出现在句子中第一个位置的概率
A = np.zeros((N, M))#A[i][j]:给定tag i,出现单词j的概率
B = np.zeros((N, N))#B[i][j]:之前的状态是i，之后转换成j的概率

prev_tag = ""
for line in open('traindata.txt'):
    items = line.split('/')
    wordId, tagId = word2id[items[0]], tag2id[items[1].rstrip()]
    if prev_tag == "":#意味着句子开始
        pi[tagId] += 1#此处的tagId相当于列表中的索引
        A[tagId][wordId] += 1
    else:#如果不是句子的开头
        A[tagId][wordId] += 1
        B[tag2id[prev_tag]][tagId] += 1
    if items[0] == ".":
        prev_tag = ""
    else:
        prev_tag = items[1].rstrip()
#normalize  从次数转为概率
pi = pi/sum(pi)
for i in range(N):
    A[i] /= sum(A[i])
    B[i] /= sum(B[i])
def log(v):
    if v == 0:
       return np.log(v+0.000001)
    return np.log(v)

def viterbi(x, pi, A, B):
    """
    :param x: user input string/sentence用户输入的句子,"I like playing soccer"
    :param pi: initial probability of tags第一个tag的概率
    :param A: 给定tag,每个单词出现的概率
    :param B: tag之间的转移概率
    :return:
    """
    x = [word2id[word] for word in x.split(" ")]
    T = len(x)

    dp = np.zeros((T, N))#dp[i][j]:w1...wi,假设wi的tag是第j个tag
    ptr = np.array([[0 for x in range(N)] for y in range(T)])#T*N
    for j in range(N):#basecase for DP 算法
        dp[0][j] = log(pi[j]) + log(A[j][x[0]])
    for i in range(1,T):#每个单词
        for j in range(N):#每个词性
            dp[i][j] = -9999
            for k in range(N):#从每一个K可以到达j
                score = dp[i-1][k] + log(B[k][j]) + log(A[j][x[i]])
                if score > dp[i][j]:
                    dp[i][j] = score
                    ptr[i][j] = k
    #decoding:把最好的tag sequence 打印出来
    best_seq = [0] * T
    #step1:找出对应于最后一个单词的词性
    best_seq[T-1] = np.argmax(dp[T-1])

    #step2:通过从后到前的循环来依次求出每个单词的词性
    for i in range(T-2, -1, -1):
        best_seq[i] = ptr[i+1][best_seq[i+1]]
    #到目前为止，best_seq存放了对应的x的词性序列
    for i in range(len(best_seq)):
        print(id2tag[best_seq[i]])
x = "Social Security number , passport number and details"
viterbi(x, pi, A, B)
















