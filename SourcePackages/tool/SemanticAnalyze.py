import jieba
import re
import os
import tool.expand_tool as expand_tool

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open("tool" + os.sep + 'baidu_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


def cut_text(input_str):
    cut_list = jieba.cut(input_str, cut_all=False)
    #res_list = [c1 for c1 in cut_list if c1 not in stop_words]
    return cut_list


def do_judge_type(question, hint):
    hint = ' '.join(hint)
    hint = expand_tool.remove_symbol(hint)
    question = expand_tool.remove_symbol(question)
    if len(hint) > len(question):
        if question in hint:
            return ['A']
    else:
        if hint in question:
            return ['A']
    return ['B']

def do_muti_selection(selections,question_content,hint):
    hint = ' '.join(hint)
    sel_list = []
    letters = ['A','B','C','D','E','F']
    count = find_continue_blank_count(question_content)
    if len(selections) == count:
        for i in range(count):
            sel_list.append(letters[i])
        return sel_list
    for i in range(len(selections)):
        if expand_tool.remove_symbol(selections[i]) in hint:
            sel_list.append(letters[i])
    if len(sel_list) < count:#判断出的选项不够，随机补一个
        n1 = count - len(sel_list)
        t1 = 0
        for let in letters:
            if let not in sel_list and t1 < n1:
                sel_list.append(let)
                t1 += 1

    return sel_list

def do_single_selection(selections, question_content, hint_text):
    hint_text = ''.join(hint_text)
    hint_text = expand_tool.remove_symbol(hint_text)
    ratio = [0]*len(selections)
    res_list = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F']

    #判断题
    if expand_tool.remove_symbol(selections[0]) == "正确" and expand_tool.remove_symbol(selections[1]) == "错误":
        res_list = do_judge_type(question_content,hint_text)
        return res_list

    #反选题
    in_count = 0
    out_index = 0
    for i in range(len(selections)):
        if selections[i] in hint_text:
            ratio[i] = 1
            in_count += 1
        else:
            out_index = i
    if in_count == len(selections)-1:#单选题有三个选项在提示里面，说明是反选，选择不在提示中的那个
        res_list = [letters[i]]
        return res_list



    for m in range(len(selections)):
        if len(selections[m]) > len(hint_text):
            short_str = hint_text
            long_str = selections[m]
        else:
            short_str = selections[m]
            long_str = hint_text
        short_str = expand_tool.remove_symbol(short_str)
        long_str = expand_tool.remove_symbol(long_str)
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
    res_list.append(letters[max_index])
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
