

#coding=utf-8       #代码中有中文时输入此项   环境 ubuntu  待改进：下载速度慢

import
 scrapy       #使用scrapy

import
 re           #使用正则表达式匹配内容

import
 requests
     # requests 用来进行内容下载


class
 
UiiconSpider
(
scrapy
.
Spider
):

	name 
=
 
"car"                                                 #每个爬虫必须有单独的名称

	allowed_domains 
=
 
[
"http://www.27270.com"
]                   # 允许爬取的域名

	start_urls 
=
 
[
"http://www.27270.com/beautiful/qichetuku/"
]   #开始爬取的地址


	
def
 parse
(
self
,
response
):                                    #自动调用的解析函数

		
for
 sel 
in
 response
.
xpath
(
'//div[@class = "w1200"]'
):    # 解析开始，div下所有w1200标签内容,返回selectorlist

			src 
=
 sel
.
xpath
(
'ul/li/a'
).
extract
()
                 #提取该路径下的内容，返回list

			
for
 text 
in
 src
:                                     #文本中查找想要内容

				url 
=
 re
.
findall
(
'src="(.*?)"'
,
text
)             

				title 
=
 re
.
findall
(
'alt="(.*?)"'
,
text
)

				name 
=
 title
[
0
]

				suffix 
=
 
'.'
 
+
 url
[
0
].
split
(
'.'
)[-
1
]             #分割出文件后缀

#				print(title[0].encode('utf-8'))

#				print(url)

				saveFileName 
=
 name 
+
 suffix                     #拼接保存的文件名

				
print
(
'downloading..'
 
+
 saveFileName
)            #以下内容为下载保存图片

				responseFile 
=
 requests
.
get
(
url
[
0
].
strip
(),
 stream
=
True
)

				image 
=
 responseFile
.
content

				
with
 open
(
saveFileName
,
"wb"
)
 
as
 jpg
:

					jpg
.
write
(
image
)
     


		
for
 nxtpgsel 
in
 response
.
xpath
(
'//div[@class = "NewPages"]'
):#页面内查找下一页链接

			src 
=
 nxtpgsel
.
xpath
(
'ul/li'
).
extract
()                  #返回li标签内容

			
for
 text 
in
 src
:

				
if
 
"下一页"
.
decode
(
'utf-8'
)
 
in
 text
:                  #查找包含下一页的li

					nxtlnk 
=
 
''
.
join
(
re
.
findall
(
'href="(.*?)"'
,
text
)) #找到下一页连接，并转换为字符串

					nxtlnk 
=
 self
.
allowed_domains
[
0
]
 
+
 nxtlnk         #拼接URL

					
yield
 scrapy
.
Request
(
nxtlnk
,
callback 
=
 self
.
parse
,
dont_filter 
=
 
True
)                                  #利用yield请求下一页，并传递给回调函数，由于允许域名和该连接的域名不相同，设置不过滤，否则会导致response不能传递给parse，导致爬取失败，是否过滤仍有待研究


