import  requests
from lxml import etree
import os



if not os.path.exists(os.getcwd()+"/xiaoshuo"):
    print("小说文件夹不存在，自动创建一个")
    os.mkdir("xiaoshuo")
    # 把当前路径改为到xiaoshuo文件夹
    os.chdir(os.getcwd()+"/xiaoshuo")
else:
    print("小说文件夹存在")
    os.chdir(os.getcwd()+"/xiaoshuo")



#设置请求头（网络，第一个，拉到底找user-agent）
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34'}
#设置想要爬取小说的目录页链接
url='https://www.cascoo.net/137_137811/'



#爬取函数
#设置爬取小说的函数功能
def get_text(url):
    response = requests.get(url, headers=headers)

    #最常用的编码方式是utf-8以及gbk，出现乱码可以先尝试这两种
    geshi='utf-8'
    #geshi='gbk'
    response.encoding = geshi
    selector = etree.HTML(response.text)

    #获取到所有章节的标题和章节链接
    #注意：xpath选用p标签下的所有值，写成/p/text(),而不是/p[]/text()
    title=selector.xpath('//*[@id="list"]/dl[2]/dd/a/text()')
    hrefs=selector.xpath('//*[@id="list"]/dl[2]/dd/a/@href')
    print(hrefs)
    print(title)

    # #不是从第一章开始的，修改列表为
    # title=title[9:]
    # hrefs=hrefs[9:]
    # print(title)
    # print(hrefs)
    #
    # # 需要翻页的，在链接后面添加-1，-2
    # hre=[]
    # hre2=[]
    # for i in range(0, len(hrefs)):
    #     hre.append(str(hrefs[i]))
    #     hre2.append(hre[i].replace('.html',''))
    # print(hre2)
    # hrefss=[]
    # for i in hre2:
    #     # 把url和href拼接得到每一章具体内容的url并存在urls列表里
    #     hrefss.append(i + '-1.html')
    #     hrefss.append(i + '-2.html')
    # print(hrefss)

    # 制作一个总urls列表用于爬取
    urls = []
    for i in hrefs:
         # 把url和href拼接得到每一章具体内容的url并存在urls列表里
         urls.append('https://www.cascoo.net'+ i)
    print(urls)
#下载所有章节到一个文件里
    for i in range(0,len(urls)):
        response = requests.get(urls[i], headers=headers)
        response.encoding = geshi
        selector = etree.HTML(response.text)

        # 获取每一章具体的内容//*[@id="content"]/text()[2]
        contents = selector.xpath('//*[@id="content"]/text()')
        print("获取第"+str(i+1)+"页内容")
        print(contents)

        #开始下载
        f = open("蚕枝.txt", "a", encoding='utf-8')
        #格式化设定
        huanhang = '\n'
        xian = '——' * 14


        f.write('\n')
        f.write(xian)
        f.write('\n')
        f.write("第"+str(i+1)+"章")
        #f.write('\n')
        # f.write(str(titlen[i]))
        f.write('\n')
        print("导出第"+str(i+1)+"章中，请稍后")

        # 写入标题和章节分割（if判断值由页数而定）
        # if i%2==0:
        #     f.write('\n')
        #     f.write(xian)
        #     f.write('\n')
        #     f.write("第"+str(int(i/2+1))+"章")
        #     f.write('\n')
        #     f.write(str(title[int(i/2)]))
        #     f.write('\n')
        #     print("正在下载"+str(i/2+1)+"章")

        f.write(huanhang.join(contents))
        f.close()
        print("uls["+str(i)+"]"+"对应内容已成功写入文档")
    print("全文下载完成！")

    ##分开保存小说章节名称及章节内容
    ##要合并为一个txt，就cmd,并d:,cd到文件夹下，然后：Copy *.txt  book.txt
    #     with open(title[i] + ".txt", "w", encoding='utf-8') as f:
    #         for content in contents:
    #             content = content+"\n"
    #             # 将每一章的内容写入对应章节的txt文件里
    #             f.write(content)
    #         print(str(title[i]) + "下载成功！")
get_text(url)

