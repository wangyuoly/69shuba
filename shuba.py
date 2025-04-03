import requests
from bs4 import BeautifulSoup
import json

def 爬取目录(目录链接):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.4472.124 Safari/537.36'
    }
    响应 = requests.get(目录链接,headers=headers)
    响应.encoding = 'gbk'  # 设置响应的编码为GBK
    if 响应.status_code != 200:
        print(f"爬取失败，状态码：{响应.status_code}")
        return

    soup = BeautifulSoup(响应.text, 'html.parser')
    all_ul = soup.find_all('ul')
    ul = all_ul[4]
    all_a = ul.find_all('a')
    目录列表 = []

    for a in all_a:
        章节链接 = a["href"]
        目录列表.append(章节链接)

    目录列表.reverse()

    return 目录列表

def 爬取章节(链接):
    print(链接)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    响应 = requests.get(链接,headers=headers)
    响应.encoding = 'gbk'  # 设置响应的编码为GBK
    if 响应.status_code != 200:
        print(f"爬取失败，状态码：{响应.status_code}")
        return
    return 响应.text

def 处理章节(文本内容):

    文本内容列表 = 文本内容.split('\n')

    for 文本 in 文本内容列表:

        if '<script>loadAdv(2, 0);</script>' in 文本:
            开始行号 = 文本内容列表.index(文本)+2
        
        if "<script>loadAdv(3, 0);</script>" in 文本:
            结尾行号 = 文本内容列表.index(文本)-1

    处理后文本 = 文本内容列表[开始行号:结尾行号]

    返回文本 = ""
    for 文本 in 处理后文本:
        返回文本 += 文本 + '\n'

    返回文本 = 返回文本.replace('<br />','\n')
    返回文本 = 返回文本.replace('<p>','')
    返回文本 = 返回文本.replace('</p>','\n')
    返回文本 = 返回文本.replace('最⊥新⊥小⊥说⊥在⊥六⊥9⊥⊥书⊥⊥吧⊥⊥首⊥发！','')
    返回文本 = 返回文本.replace('<div class="contentadv"><script>loadAdv(7,3);</script></div>','')

    return 返回文本

def 生成json(小说名字,目录链接):
    目录列表 = 爬取目录(目录链接)

    章节JSON = []
    序号 = 1
    for 章节链接 in 目录列表:
        章节 = {
            "序号":序号,
            "章节链接":章节链接,
            "是否成功":False,
            "正文":""
        }
        章节JSON.append(章节)
        序号 = 序号 + 1

    with open(f"{小说名字}.json",'w',encoding='utf-8') as 文件:
        json.dump(章节JSON,文件,ensure_ascii=False,indent=4)

def 爬取所有章节(书名):
    with open(f"{书名}.json",'r',encoding='utf-8') as 文件:
        章节JSON = json.load(文件)

    for 章节 in 章节JSON:
        print(章节["序号"])
        if 章节["是否成功"] == False:
            未处理内容 = 爬取章节(章节["章节链接"])
            处理后内容 = 处理章节(未处理内容)
            章节["正文"]= 处理后内容
            章节["是否成功"] = True

            with open("我在精灵世界浪到失联.json",'w',encoding='utf-8') as 文件:
                json.dump(章节JSON,文件,ensure_ascii=False,indent=4)

def 合并章节(书名):
    pass

# 生成json("我在精灵世界浪到失联","https://69shuba.cx/book/44468/")
爬取所有章节("我在精灵世界浪到失联")
合并章节("我在精灵世界浪到失联")