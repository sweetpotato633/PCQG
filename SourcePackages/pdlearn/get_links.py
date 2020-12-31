import requests
import re
import pdlearn.para_config as para

def get_article_links():
    try:
        #article = requests.get(
        #    "https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/data9a3668c13f6e303932b5e0e100fc248b.js").content.decode(
        #    "utf8")
        #artic = requests.get("https://source.xuexi.cn/AWSC/AWSC/awsc.v2.js").content.decode("utf8")

        #https://www.xuexi.cn/lgdata/35il6fpn0ohq.json?_st=26820188
        res = requests.get(r'https://www.xuexi.cn/lgdata/35il6fpn0ohq.json?_st=26820188')
        article = res.json()
        g_list = para.LoadListFromFile('article.txt')
        titles = [t1['publishTime'] + t1['title'] for t1 in article]
        links = [t1['url'] for t1 in article]
        t_list = []
        l_list = []
        count = 0
        for i in range(len(titles)):
            if count > 20:
                break
            if titles[i] not in g_list:
                t_list.append(titles[i])
                l_list.append(links[i])
                count += 1
        '''
        pattern = r"list\"\:(.+),\"count\"\:"
        links = []
        list = eval(re.search(pattern, article).group(1))[:20000]
        list.reverse()
        news_time =[]
        for i in range(len(list)):
            links.append(list[i]["static_page_url"])
            news_time.append(list[i]['original_time'])
        print(news_time)
        '''
        return l_list,t_list
    except:
        print("=" * 120)
        print("get_article_links获取失败")
        print("=" * 120)
        raise


def get_video_links():
    try:
        '''
        video = requests.get(
            "https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js").content.decode(
            "utf8")
        pattern = r'https://www.xuexi.cn/[^,"]*html'
        
        #https://www.xuexi.cn/lgdata/1novbsbi47k.json?_st=26820259
        link = re.findall(pattern, video, re.I)
        link.reverse()
        '''
        res = requests.get(r'https://www.xuexi.cn/lgdata/1novbsbi47k.json?_st=26820259')
        video = res.json()
        titles = [t1['publishTime'] + t1['title'] for t1 in video]
        links = [t1['url'] for t1 in video]
        t_list = []
        l_list = []
        count = 0
        g_list = para.LoadListFromFile('vedio.txt')
        for i in range(len(titles)):
            if count > 20:
                break
            if titles[i] not in g_list:
                t_list.append(titles[i])
                l_list.append(links[i])
                count += 1
        return l_list,t_list
    except:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise


def test():
    get_article_links()


if __name__ == "__main__":
    test()
    print("finished\n")