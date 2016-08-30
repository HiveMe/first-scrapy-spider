#coding=utf-8
import scrapy
import re
import requests

class UiiconSpider(scrapy.Spider):
	name = "car"
	allowed_domains = ["http://www.27270.com"]
	start_urls = ["http://www.27270.com/beautiful/qichetuku/"]

	def parse(self,response):
		print('in parse')
		for sel in response.xpath('//div[@class = "w1200"]'):
			src = sel.xpath('ul/li/a').extract()
			for text in src:
				url = re.findall('src="(.*?)"',text)
				title = re.findall('alt="(.*?)"',text)
				name = title[0]
				suffix = '.' + url[0].split('.')[-1]
#				print(title[0].encode('utf-8'))
#				print(url)
				saveFileName = name + suffix 
				print('downloading..' + saveFileName)
				responseFile = requests.get(url[0].strip(), stream=True)
				image = responseFile.content
				with open(saveFileName,"wb") as jpg:
					jpg.write(image)     

		for nxtpgsel in response.xpath('//div[@class = "NewPages"]'):
			src = nxtpgsel.xpath('ul/li').extract()
			for text in src:
				if "下一页".decode('utf-8') in text:
					nxtlnk = ''.join(re.findall('href="(.*?)"',text))
					nxtlnk = self.allowed_domains[0] + nxtlnk
					yield scrapy.Request(nxtlnk,callback = self.parse,dont_filter = True)


