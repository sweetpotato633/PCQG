import jieba
import re
import os

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open("tool" + os.sep + 'baidu_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


def cut_text(input_str):
    cut_list = jieba.cut(input_str, cut_all=False)
    #res_list = [c1 for c1 in cut_list if c1 not in stop_words]
    return cut_list


def do_judge_type(question, hint):
    if len(hint) > len(question):
        if question in hint:
            return True
    else:
        if hint in question:
            return True
    return False

def do_normal_selection(selections,question_content,hint):
    sel_list = []
    for i in range(len(selections)):
        if selections[i] in hint:
            sel_list.append(i)
    return sel_list

def single_selection(selections, question_content, hint_text):
    ratio = [0]*len(selections)
    res_list = []
    for m in range(len(selections)):
        if len(selections[m]) > len(hint_text):
            short_str = hint_text
            long_str = selections[m]
        else:
            short_str = selections[m]
            long_str = hint_text
        match_length = 0
        for i in range(len(short_str)):
            if short_str[i] in long_str:
                match_length += 1
        ratio[m] = match_length
    max_value = 0
    max_index = 0
    for i in range(len(ratio)):
        if ratio[i] > max_value:
            max_value = ratio[i]
            max_index = i
    res_list.append(max_index)
    return res_list


def find_continue_blank_count(msg):
    pattern = r'（）'
    res = re.findall(pattern,msg)
    return len(res)

def test():
    str = "今天烟台很多地方下了雪，包括    、    、和    。haiyou   "
    find_continue_blank_count(str)

#stop_words = stopwordslist()

if __name__ == "__main__":
    test()
