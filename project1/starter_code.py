# encoding: utf-8
'''
@author: jinjin
@contact: cantaloupejinjin@gmail.com
@file: starter_code.py
@time: 2019/10/25 14:23
'''
import xlrd
from math import log
workbook  = xlrd.open_workbook("data/综合类中文词库.xlsx")

dic_words = []
booksheet = workbook.sheet_by_index(0)

rows = booksheet.get_rows()
for row in rows:
    dic_words.append(row[0].value)

print("len：" + str(len(dic_words)))

word_prob = {"北京":0.03,"的":0.08,"天":0.005,"气":0.005,"天气":0.06,"真":0.04,"好":0.05,"真好":0.04,"啊":0.01,"真好啊":0.02,
             "今":0.01,"今天":0.07,"课程":0.06,"内容":0.06,"有":0.05,"很":0.03,"很有":0.04,"意思":0.06,"有意思":0.005,"课":0.01,
             "程":0.005,"经常":0.08,"意见":0.08,"意":0.01,"见":0.005,"有意见":0.02,"分歧":0.04,"分":0.02, "歧":0.005}

print (sum(word_prob.values()))
def word_break(s, wordDict):
    memo= {len(s): ['']}
    def sentences(i):
        if i not in memo:
            memo[i] = [s[i:j] + (tail and ',' + tail)
                       for j in range(i+1, len(s)+1)
                       if s[i:j] in wordDict
                       for tail in sentences(j)]
        return memo[i]
    list_res = sentences(0)
    list_new = []
    for line in list_res:
        line = line.split(",")
        list_new.append(line)
    return list_new

def word_segment_naive(input_str):
    """
    1. 对于输入字符串做分词，并返回所有可行的分词之后的结果。
    2. 针对于每一个返回结果，计算句子的概率
    3. 返回概率最高的最作为最后结果

    input_str: 输入字符串   输入格式：“今天天气好”
    best_segment: 最好的分词结果  输出格式：["今天"，"天气"，"好"]
    """
    # TODO： 第一步： 计算所有可能的分词结果，要保证每个分完的词存在于词典里，这个结果有可能会非常多。

    segments = word_break(input_str, dic_words)  # 存储所有分词的结果。如果次字符串不可能被完全切分，则返回空列表(list)
    # 格式为：segments = [["今天"，“天气”，“好”],["今天"，“天“，”气”，“好”],["今“，”天"，“天气”，“好”],...]
    # TODO: 第二步：循环所有的分词结果，并计算出概率最高的分词结果，并返回
    best_segment = []
    best_score = 0
    for seg in segments:
    # TODO ...
        score = 0
        for i in range(len(seg)):
            if seg[i] in word_prob:
                score += - log(word_prob.get(seg[i]))
            else:
                score += - log(0.00001)
        if score > best_score:
            best_segment = seg
    return best_segment

#维特比算法优化
def word_segment_viterbi(input_str):
    """
    1. 基于输入字符串，词典，以及给定的unigram概率来创建DAG(有向图）。
    2. 编写维特比算法来寻找最优的PATH
    3. 返回分词结果

    input_str: 输入字符串   输入格式：“今天天气好”
    best_segment: 最好的分词结果  输出格式：["今天"，"天气"，"好"]
    """

    # TODO: 第一步：根据词典，输入的句子，以及给定的unigram概率来创建带权重的有向图（Directed Graph） 参考：课程内容
    #      有向图的每一条边是一个单词的概率（只要存在于词典里的都可以作为一个合法的单词），这些概率在 word_prob，如果不在word_prob里的单词但在
    #      词典里存在的，统一用概率值0.00001。
    #      注意：思考用什么方式来存储这种有向图比较合适？ 不一定有只有一种方式来存储这种结构。
    #      使用字典来存储
    graph = {}
    N = len(input_str)
    #     print(N)
    for k in range(N - 1, -1, -1):
        tmplist = []
        i = k
        # 位置k形成的片段
        frag = input_str[k]
        # 判断片段是否在前缀词典中
        # 如果片段不在前缀词典中，则跳出本循环
        # 也即该片段已经超出统计词典中该词的长度
        while i >= 0 and frag in dic_words:
            # 将该片段加入到有向无环图中
            # 片段末尾位置加1
            tmplist.append(i)
            i -= 1
            # 新的片段较旧的片段右边新增一个字
            #             frag = input_str[k:i + 1]
            frag = input_str[i:k + 1]
        if not tmplist:
            tmplist.append(k)
        graph[k] = tmplist

    #     print(graph)

    # TODO： 第二步： 利用维特比算法来找出最好的PATH， 这个PATH是P(sentence)最大或者 -log P(sentence)最小的PATH。
    #              hint: 思考为什么不用相乘: p(w1)p(w2)...而是使用negative log sum:  -log(w1)-log(w2)-...
    list_f = []
    list_f.append(0.0)
    best_path = []
    for i in range(N):
        if i == 0:
            best_path.append(i)
            word = input_str[i]
            if word in word_prob:
                list_f.append(-log(word_prob.get(word)))
            else:
                list_f.append(-log(0.00001))
        else:
            min_word_p = 1000000.0
            min_index = 10000
            for j in graph.get(i):
                word = input_str[j:i + 1]
                word_p = 0.0
                if word in word_prob:
                    word_p = -log(word_prob.get(word))
                else:
                    word_p = -log(0.00001)

                word_p += list_f[j]
                if min_word_p > word_p:
                    min_word_p = word_p
                    if min_index > j:
                        min_index = j
                best_path.append(min_index)
                while best_path[-1] >= min_index:
                    best_path.pop()
                    if len(best_path) == 0:
                        break
                best_path.append(min_index)
            list_f.append(min_word_p)

    best_path.append(len(input_str))
    print(best_path)

    # TODO: 第三步： 根据最好的PATH, 返回最好的切分
    best_segment = []
    for i in range(len(best_path) - 1):
        best_segment.append(input_str[best_path[i]:best_path[i + 1]])

    return best_segment


# 测试
print(word_segment_naive("北京的天气真好啊"))
print(word_segment_naive("今天的课程内容很有意思"))
print(word_segment_naive("经常有意见分歧"))

#维特比算法测试
print(word_segment_viterbi("北京的天气真好啊"))
print(word_segment_viterbi("今天的课程内容很有意思"))
print(word_segment_viterbi("经常有意见分歧"))