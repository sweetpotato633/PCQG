import time
from sys import argv
import random
from pdlearn import version
from pdlearn import user
from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import threads
from pdlearn import get_links
from pdlearn.mydriver import Mydriver
import pdlearn.para_config as para
import tool.SemanticAnalyze as SemanticAnalyze


def user_flag(dd_status, uname):
    if False and dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        # if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
        if True:
            driver_login = mydriver.Mydriver(nohead=False)
            cookies = driver_login.login()
        else:
            cookies = dingding.dd_login_status(uname)
    a_log = user.get_a_log(uname)
    v_log = user.get_v_log(uname)
    d_log = user.get_d_log(uname)

    return cookies, a_log, v_log, d_log


def get_argv():
    nohead = True
    lock = False
    stime = False
    if len(argv) > 2:
        if argv[2] == "hidden":
            nohead = True
        elif argv[2] == "show":
            nohead = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    return nohead, lock, stime


def show_score(cookies):
    total, each = score.get_score(cookies)
    print("当前学习总积分：" + str(total))
    print("阅读文章:{}/6,观看视频:{}/6,登陆:{}/1,文章时长:{}/6,视频时长:{}/6,每日答题:{}/6,每周答题:{}/5,专项答题:{}/10".format(*each))
    # print("阅读文章:",each[0],"/6,观看视频:",each[1],"/6,登陆:",each[2],"/1,文章时长:",each[3],"/6,视频时长:",each[4],"/6,每日答题:",each[5],"/6,每周答题:",each[6],"/5,专项答题:",each[7],"/10")
    return total, each


def article(cookies, a_log, each):
    if each[0] < 6 or each[3] < 8:
        driver_article = mydriver.Mydriver(nohead=nohead)
        driver_article.get_url("https://www.xuexi.cn")
        driver_article.set_cookies(cookies)
        links,titles = get_links.get_article_links()
        try_count = 0
        readarticle_time = 0
        while True:
            if each[0] < 6 and try_count < 10:
                a_num = 6 - each[0]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    para.SaveListToFile('article.txt',titles[i])
                    readarticle_time = 60 + random.randint(5, 15)
                    print("\n阅读文章：" + titles[i] + "\n")
                    for j in range(readarticle_time):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, readarticle_time - j), end="")
                        time.sleep(1)
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = show_score(cookies)
                    if each[0] >= 6:
                        print("检测到文章数量分数已满,退出学习")
                        break
                a_log += a_num
            else:
                with open("./user/{}/a_log".format(uname), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                break
        try_count = 0
        while True:
            if each[3] < 6 and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log - 1])
                para.SaveListToFile('article.txt', titles[a_log - 1])
                print("\n阅读文章：" + titles[a_log - 1] + "\n")
                remaining = (6 - each[3]) * 1 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (60) == 0 and i != remaining:
                        total, each = show_score(cookies)
                        if each[3] >= 6:
                            print("检测到文章时长分数已满,退出学习")
                            break
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("文章学习完成")
        else:
            print("文章学习出现异常，请检查用户名下a_log文件记录数")
        driver_article.quit()
    else:
        print("文章之前学完了")


def video(cookies, v_log, each):
    if each[1] < 6 or each[4] < 10:
        driver_video = mydriver.Mydriver(nohead=nohead)
        driver_video.get_url("https://www.xuexi.cn")
        driver_video.set_cookies(cookies)
        links,titles = get_links.get_video_links()
        try_count = 0
        watchvideo_time = 0
        while True:
            if each[1] < 6 and try_count < 10:
                v_num = 6 - each[1]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    para.SaveListToFile('vedio.txt', titles[i])
                    watchvideo_time = 60 + random.randint(5, 15)
                    print("\n观看视频：" + titles[i] + "\n")
                    for j in range(watchvideo_time):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, watchvideo_time - j), end="")
                        time.sleep(1)
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = show_score(cookies)
                    if each[1] >= 6:
                        print("检测到视频数量分数已满,退出学习")
                        break
                v_log += v_num
            else:
                with open("./user/{}/v_log".format(uname), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                break
        try_count = 0
        while True:
            if each[4] < 6 and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log - 1])
                para.SaveListToFile('vedio.txt', titles[v_log - 1])
                print("\n" + titles[v_log - 1] + "\n")
                remaining = (6 - each[4]) * 1 * num_time
                print("\n观看视频：" + titles[v_log - 1] + "\n")
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (60) == 0 and i != remaining:
                        total, each = show_score(cookies)
                        if each[4] >= 6:
                            print("检测到视频时长分数已满,退出学习")
                            break
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("视频学习完成")
        else:
            print("视频学习出现异常，请检查用户名下v_log文件记录数")
        driver_video.quit()
    else:
        print("视频之前学完了")


def check_delay(self, time_start=1, time_end=5):
    # delay_time = random.randint(time_start, time_end)
    seg = random.randint(1, 10)
    ratio = seg / 10
    delay = time_start + (time_end - time_start) * ratio
    #print('等待 ', delay, ' 秒')
    time.sleep(delay)


def save_cost_time(file_name,msg):
    with open(file_name,'a+',encoding='utf8') as fp:
        msg = msg + '\n'
        fp.write(msg)



def daily(cookies, d_log, each):
    start_time = time.time()
    last_time = time.time()
    time_list = []
    if each[5] < 6:
        # driver_daily = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_daily = mydriver.Mydriver(nohead=False)
        driver_daily.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_daily.get_url("https://www.xuexi.cn")
        driver_daily.set_cookies(cookies)
        try_count = 0

        if each[5] < 6:
            d_num = 6 - each[5]
            letters = list("ABCDEFGHIJKLMN")
            driver_daily.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_daily.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
            tips_err = 0
            while each[5] < 6:
                try:
                    category = driver_daily.xpath_getText(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]')  # get_attribute("name")
                except Exception as e:
                    print('查找元素失败！')
                    break
                print(category)
                tips = driver_daily._view_tips()
                driver_daily.check_delay()

                if not tips:
                    tips_err += 1
                    if "填空题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                    elif "多选题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                    elif "单选题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        cur_time = time.time()
                        t1 = cur_time - start_time
                        time_list.append(t1)
                        time_str = [str(temp) for temp in time_list]
                        save_cost_time('cost_time_daily.txt', ','.join(time_str))
                        break
                else:
                    tips_err = 0

                if driver_daily.click_next_when_error():
                    print("这个题答错了，进行下一题\n")
                    continue
                question_body = driver_daily.get_question_body()
                print(question_body)
                if "填空题" in category:
                    answer = tips
                    if not tips:
                        answer = "和谐社会和谐社会"
                        print("\n未找到提示，随便填了一个\n")
                    try:
                        driver_daily.fill_in_blank(answer)
                    except Exception as e:
                        print(e)
                        continue

                elif "多选题" in category:
                    options = driver_daily.radio_get_options()
                    selections = [op[2:] for op in options]
                    try:
                        radio_in_tips = SemanticAnalyze.do_muti_selection(selections, question_body, tips)
                    except:
                        continue
                    print('根据提示', radio_in_tips)
                    driver_daily.radio_check(radio_in_tips)

                elif "单选题" in category:
                    options = driver_daily.radio_get_options()
                    selections = [op[2:] for op in options]
                    try:
                        radio_in_tips = SemanticAnalyze.do_single_selection(selections, question_body, tips)
                    except:
                        continue
                    print('根据提示', radio_in_tips)
                    driver_daily.radio_check(radio_in_tips)
                else:
                    print("题目类型非法")
                    cur_time = time.time()
                    t1 = cur_time - start_time
                    time_list.append(t1)
                    time_str = [str(temp) for temp in time_list]
                    save_cost_time('cost_time_daily.txt', ','.join(time_str))
                    break
                # print("\r每日答题中，题目剩余{}题".format(d_log + d_num - i), end="")
                time.sleep(1)

                d_log += d_num
                cur_time = time.time()
                t1 = cur_time - last_time
                last_time = cur_time
                time_list.append(t1)

            total, each = show_score(cookies)
            if each[5] >= 6:
                print("检测到每日答题分数已满,退出学习")
                cur_time = time.time()
                t1 = cur_time - start_time
                time_list.append(t1)
                time_str = [str(temp) for temp in time_list]
                save_cost_time('cost_time_daily.txt',','.join(time_str))
                driver_daily.quit()
        else:
            with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(d_log))
            # break
        try:
            driver_daily.quit()
        except Exception as e:
            print('……')
    else:
        print("每日答题之前学完了")


def weekly(cookies, d_log, each):
    start_time = time.time()
    last_time = time.time()
    time_list = []
    if each[6] < 5:
        # driver_weekly = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_weekly = mydriver.Mydriver(nohead=False)
        driver_weekly.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_weekly.get_url("https://www.xuexi.cn")
        driver_weekly.set_cookies(cookies)
        try_count = 0

        if each[6] < 5:
            d_num = 6 - each[5]
            letters = list("ABCDEFGHIJKLMN")
            driver_weekly.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_weekly.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
            time.sleep(2)
            flag = 1
            for tem in range(0, 40):
                for tem2 in range(0, 5):
                    try:
                        temword = driver_weekly.driver.find_element_by_xpath(
                            '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                                tem2 + 1) + ']/button').text
                    except:
                        temword = ''
                    name_list = ["开始答题", "继续答题"]
                    if flag == 1 and (any(name in temword for name in name_list)):
                        driver_weekly.click_xpath(
                            '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                                tem2 + 1) + ']/button')
                        flag = 0
            tips_err = 0
            while each[6] < 5 and try_count < 10:
                try:
                    category = driver_weekly.xpath_getText(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]')  # get_attribute("name")
                except Exception as e:
                    print('查找元素失败！')
                    break
                print(category)
                tips = driver_weekly._view_tips()
                driver_weekly.check_delay()
                if not tips:
                    tips_err += 1
                    if "填空题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                    elif "多选题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                    elif "单选题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        cur_time = time.time()
                        t1 = cur_time - start_time
                        time_list.append(t1)
                        time_str = [str(temp) for temp in time_list]
                        save_cost_time('cost_time_weekly.txt', ','.join(time_str))
                        break
                else:
                    tips_err = 0

                if driver_weekly.click_next_when_error():
                    print("这个题答错了，进行下一题\n")
                    continue
                question_body = driver_weekly.get_question_body()
                print(question_body)
                if "填空题" in category:
                    answer = tips
                    if not tips:
                        answer = "和谐社会和谐社会"
                        print("\n未找到提示，随便填了一个\n")
                    try:
                        driver_weekly.fill_in_blank(answer)
                    except:
                        continue

                elif "多选题" in category:
                    options = driver_weekly.radio_get_options()
                    selections = [op[2:] for op in options]
                    try:
                        radio_in_tips = SemanticAnalyze.do_muti_selection(selections, question_body, tips)
                    except:
                        continue
                    print('根据提示', radio_in_tips)
                    driver_weekly.radio_check(radio_in_tips)

                elif "单选题" in category:
                    options = driver_weekly.radio_get_options()
                    selections = [op[2:] for op in options]
                    try:
                        radio_in_tips = SemanticAnalyze.do_single_selection(selections, question_body, tips)
                    except:
                        continue
                    print('根据提示', radio_in_tips)
                    driver_weekly.radio_check(radio_in_tips)
                else:
                    print("题目类型非法")
                    cur_time = time.time()
                    t1 = cur_time - start_time
                    time_list.append(t1)
                    time_str = [str(temp) for temp in time_list]
                    save_cost_time('cost_time_weekly.txt', ','.join(time_str))
                    break
                # print("\r每周答题中，题目剩余{}题".format(d_log + d_num - i), end="")
                time.sleep(1)

                d_log += d_num
                cur_time = time.time()
                t1 = cur_time - last_time
                last_time = cur_time
                time_list.append(t1)

            total, each = show_score(cookies)
            if each[6] >= 5:
                print("检测到每周答题分数已满,退出学习")
                cur_time = time.time()
                t1 = cur_time - start_time
                time_list.append(t1)
                time_str = [str(temp) for temp in time_list]
                save_cost_time('cost_time_weekly.txt', ','.join(time_str))
                driver_weekly.quit()
        else:
            with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(d_log))
            # break
        try:
            driver_weekly.quit()
        except Exception as e:
            print('……')
    else:
        print("每周答题之前学完了")


def zhuanxiang(cookies, d_log, each):
    start_time = time.time()
    last_time = time.time()
    time_list = []
    if each[7] < 10:
        # driver_zhuanxiang = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_zhuanxiang = mydriver.Mydriver(nohead=False)
        driver_zhuanxiang.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_zhuanxiang.get_url("https://www.xuexi.cn")
        driver_zhuanxiang.set_cookies(cookies)
        try_count = 0

        if each[7] < 10:
            d_num = 10 - each[5]
            letters = list("ABCDEFGHIJKLMN")
            driver_zhuanxiang.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_zhuanxiang.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div')
            time.sleep(2)
            for tem in range(0, 40):
                try:
                    temword = driver_zhuanxiang.driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div/div/div/div[' + str(tem + 1) + ']/div[2]/button').text
                except:
                    temword = ''
                name_list = ["开始答题", "继续答题"]  # , "重新答题"
                if (any(name in temword for name in name_list)):
                    driver_zhuanxiang.click_xpath(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div/div/div/div[' + str(tem + 1) + ']/div[2]/button')
                    break
            while each[7] < 10:
                try:
                    category = driver_zhuanxiang.xpath_getText(
                        '//*[@id="app"]/div/div[2]/div/div[6]/div[1]/div[1]')  # get_attribute("name")
                except Exception as e:
                    print('查找元素失败！')
                    break
                print(category)
                tips = driver_zhuanxiang._view_tips()
                driver_zhuanxiang.check_delay()
                if not tips:
                    tips_err += 1
                    if "填空题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                    elif "多选题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                    elif "单选题" in category:
                        print('没有找到提示，重试...')
                        if tips_err < 3:
                            continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        cur_time = time.time()
                        t1 = cur_time - start_time
                        time_list.append(t1)
                        time_str = [str(temp) for temp in time_list]
                        save_cost_time('cost_time_zhuan.txt', ','.join(time_str))
                        break
                else:
                    tips_err = 0

                if driver_zhuanxiang.click_next_when_error(test_type="专项"):
                    print("这个题答错了，进行下一题\n")
                    continue
                question_body = driver_zhuanxiang.get_question_body()
                print(question_body)
                if "填空题" in category:
                    answer = tips
                    if not tips:
                        answer = "和谐社会"
                        print("\n未找到提示，随便填了一个\n")
                    try:
                        driver_zhuanxiang.fill_in_blank(answer)
                    except:
                        continue

                elif "多选题" in category:
                    options = driver_zhuanxiang.radio_get_options()
                    selections = [op[2:] for op in options]
                    try:
                        radio_in_tips = SemanticAnalyze.do_muti_selection(selections, question_body, tips)
                    except:
                        continue
                    print('根据提示', radio_in_tips)
                    driver_zhuanxiang.radio_check(radio_in_tips)

                elif "单选题" in category:
                    options = driver_zhuanxiang.radio_get_options()
                    selections = [op[2:] for op in options]
                    try:
                        radio_in_tips = SemanticAnalyze.do_single_selection(selections, question_body, tips)
                    except:
                        continue
                    print('根据提示', radio_in_tips)
                    driver_zhuanxiang.radio_check(radio_in_tips)
                else:
                    print("题目类型非法")
                    cur_time = time.time()
                    t1 = cur_time - start_time
                    time_list.append(t1)
                    time_str = [str(temp) for temp in time_list]
                    save_cost_time('cost_time_zhuan.txt', ','.join(time_str))
                    break
                time.sleep(1)

                d_log += d_num
                cur_time = time.time()
                t1 = cur_time - last_time
                last_time = cur_time
                time_list.append(t1)

            total, each = show_score(cookies)
            if each[6] >= 5:
                print("检测到专项答题分数已满,退出学习")
                cur_time = time.time()
                t1 = cur_time - start_time
                time_list.append(t1)
                time_str = [str(temp) for temp in time_list]
                save_cost_time('cost_time_zhuan.txt', ','.join(time_str))

                driver_zhuanxiang.quit()
        else:
            with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(d_log))
            # break
        try:
            driver_zhuanxiang.quit()
        except Exception as e:
            print('……')
    else:
        print("专项答题之前学完了")




if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()

    print("=" * 120,'''
    V1.1 2021-01-27 优化了延时处理；优化了延时显示；修改答题默认页面为强国主页
    科技强国 现支持以下模式（答题时请值守电脑旁处理少部分不正常的题目）：
    1 文章+视频
    2 每日答题+每周答题+专项答题+文章+视频
      （可以根据当日已得做题积分，及是否有可得分套题，决定是否做题）
    3 每日答题+文章+视频
      （可以根据当日已得做题积分，决定是否做题）
    4 每日答题+每周答题+专项答题 仅答题
''',"=" * 120)
    TechXueXi_mode = input("请选择模式（输入对应数字）并回车： ")

    #info_shread = threads.MyThread("获取更新信息...", version.up_info)
    #info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies, a_log, v_log, d_log = user_flag(dd_status, uname)
    total, each = show_score(cookies)
    nohead, lock, stime = get_argv()

    if TechXueXi_mode in ["2", "3","4"]:
        print('开始每日答题……')
        daily(cookies, d_log, each)
    if TechXueXi_mode in ["2","4"]:
        print('开始每周答题……')
        weekly(cookies, d_log, each)
        print('开始专项答题……')
        zhuanxiang(cookies, d_log, each)
    question_time = int((time.time() - start_time) / 60)
    start_time = time.time()
    if TechXueXi_mode in ["1","2", "3"]:
        article_thread = threads.MyThread("文章学习", article, cookies, 0, each, lock=lock)
        article_thread.start()
        article_thread.join()
        #print("文章总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    article_time = int((time.time() - start_time) / 60)
    start_time = time.time()
    if TechXueXi_mode in ["1","2", "3"]:
        video_thread = threads.MyThread("视频学习", video, cookies, 0, each, lock=lock)
        video_thread.start()
        video_thread.join()
        #print("视频总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    vedio_time = int((time.time() - start_time) / 60)
    print("答题用时：{ques:2d} 分钟，阅读用时：{arti:2d} 分钟，视频用时：{ved:2d} 分钟\n".format(ques=question_time,arti=article_time,ved=vedio_time))
    user.shutdown(stime)
