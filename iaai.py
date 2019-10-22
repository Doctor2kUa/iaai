#!/usr/local/bin/python3
from lxml import html
from lxml import etree
import requests
import redis

def telegram_bot_sendtext(bot_message):
    bot_token = '658981372:AAE9BlNCANSZUwqg_ZUeiZOgADIcFt5OJis'
#    bot_chatID = '443557038'
    bot_chatID = '-322090519'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


#url='https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=audi%20q5'
#url='https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=LINCOLN%20MKS'
#url='https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=HYUNDAI+SANTA+FE'
#url='https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=kia+sportage'

urls=['https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=LINCOLN%20MKS', 
'https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=HYUNDAI+SANTA+FE',
'https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=kia+sportage',
'https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=jeep+cherokee',
'https://www.iaai.com/Search?&crefiners=|yearfilter:2015-|quicklinks:I-BUY%20FAST&keyword=jeep+renegade',
'https://www.iaai.com/Search?&crefiners=|yearfilter:2004-2019|quicklinks:I-BUY FAST&keyword=Honda Gl1800'
]


scrap_list=[]

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
######
r = redis.Redis(host='10.128.0.2', port=7001, db=0, decode_responses=True)
#r.flushdb()

for i in range(0, r.llen("iaai1")):
#    print(r.lindex("iaai1", i))
    scrap_list.append(r.lindex("iaai1", i))

######


try:
	with open ("show.list", 'rb') as fp:
          print ("not from file")
except FileNotFoundError:
	pass

for url in urls:

  page = requests.get(url, headers = headers)
  search=html.fromstring(page.content)
  ahref=search.xpath('//div[@class="shadow"]/table[@class="table"]/tbody/tr/td[2]/a/@href')


  for link in ahref:
    file=[]
    file_tmp=link.rsplit("=", -1)[1]
    file_str=file_tmp.split('&', -1)[0]
    file.append(file_str)
#    print (file)
#    r.delete("iaai1", file_str)


    if (file_str not in scrap_list):
      print ("show")
      uri=link.replace("../","")
      detail="https://www.iaai.com/" + uri
      detail_page=requests.get(detail, headers = headers)
      detail_html=html.fromstring(detail_page.content)
#      buy_price=detail_html.xpath('//div[@class="pd-btn-wrapper flex-btn btn-buy-wrapper"]/p/span/text()')
      buy_price=detail_html.xpath('/html/body/section/main/section[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/ul/li[1]/span[2]/text()')
      name=detail_html.xpath('/html/body/section/main/section[2]/div/div/h1/text()')
#           name.append("ALREADY SOLD!!!!")
#      name=detail_html.xpath('/html/body/section/main/section[2]/div/div/h1/text()')
#      print (name)
      try:
           str_price=(buy_price[0].rsplit('$',-1))

      except IndexError:
           pass
      print ("----")
      try:
           r.rpush ("iaai1", file_str)
      except IndexError:
          pass
      if len(name) == 0:
          name.append("ALREADY SOLD!!!!")
      mesage= (str(name[0]) + "\n" +str(str_price[1])+ "\n" +str(detail))
#      mesage= (str(str_price[1])+ "\n" +str(detail))
      test = telegram_bot_sendtext(mesage)
      print(test)
