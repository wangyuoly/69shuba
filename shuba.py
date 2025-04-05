import requests
from bs4 import BeautifulSoup
import json
import os

class Shuba():
    def __init__(self,目录链接):
        self.目录链接 = 目录链接
        self.书名 = ""
        self.章节JSON = []
        self.目录列表 = []
        self.爬取书名()
        

    def 爬取书名(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.4472.124 Safari/537.36'
        }
        响应 = requests.get(self.目录链接,headers=headers)
        响应.encoding = 'gbk'  # 设置响应的编码为GBK
        if 响应.status_code != 200:
            print(f"爬取失败，状态码：{响应.status_code}")
            return

        soup = BeautifulSoup(响应.text, 'html.parser')
        div = soup.find('div', class_='bread')
        div_a = div.find_all('a')[-1]
        self.书名 = div_a.text

    

    def 爬取目录(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.4472.124 Safari/537.36'
        }
        响应 = requests.get(self.目录链接,headers=headers)
        响应.encoding = 'gbk'  # 设置响应的编码为GBK
        if 响应.status_code != 200:
            print(f"爬取失败，状态码：{响应.status_code}")
            return

        soup = BeautifulSoup(响应.text, 'html.parser')

        all_ul = soup.find_all('ul')
        ul = all_ul[4]
        all_a = ul.find_all('a')

        for a in all_a:
            章节链接 = a["href"]
            self.目录列表.append(章节链接)

        self.目录列表.reverse()

    def 处理章节(self,文本内容):

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
    
    def 爬取章节(self,链接):
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

    def 生成json(self):
        序号 = 1
        for 章节链接 in self.目录列表:
            章节 = {
                "序号":序号,
                "章节链接":章节链接,
                "是否成功":False,
                "正文":""
            }
            self.章节JSON.append(章节)
            序号 = 序号 + 1
        
        data = {
            "小说名字":self.书名,
            "章节":self.章节JSON
        }

        with open(f"{self.书名}.json",'w',encoding='utf-8') as 文件:
            json.dump(data,文件,ensure_ascii=False,indent=4)

    def 爬取所有章节(self):
        with open(f"{self.书名}.json",'r',encoding='utf-8') as 文件:
            data = json.load(文件)

        章节JSON = data["章节"]

        for 章节 in 章节JSON:
            print(章节["序号"])
            if 章节["是否成功"] == False:
                # print(
                #     '章节["章节链接"]',
                #    章节["章节链接"] 
                # )
                未处理内容 = self.爬取章节(章节["章节链接"])
                处理后内容 = self.处理章节(未处理内容)

                章节["正文"]= 处理后内容
                章节["是否成功"] = True

                with open(f"{self.书名}.json",'w',encoding='utf-8') as 文件:
                    json.dump(data,文件,ensure_ascii=False,indent=4)

    def 合并章节(self):
        with open(f"{self.书名}.json",'r',encoding='utf-8') as 文件:
            真章节json=json.load(文件)["章节"]
            完整章节=""
            for 章节 in 真章节json:
                完整章节内容=章节["正文"]+"\n\n"

                with open(f"{self.书名}.txt","a",encoding='utf-8') as 文件:
                    文件.write(完整章节内容)

    def 一键爬取(self):
        if not os.path.exists(f"{self.书名}.json"):
            self.爬取目录()
            self.生成json()

        self.爬取所有章节()
        self.合并章节()

shuba = Shuba("https://69shuba.cx/book/44468/")
shuba.一键爬取()

