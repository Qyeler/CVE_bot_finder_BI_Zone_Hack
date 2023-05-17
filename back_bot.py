
import telebot
from telebot import types
import requests
def webAppKeyboard(str): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   if tryFind(str):
      webAppTest = types.WebAppInfo(f"https://nvd.nist.gov/vuln/detail/{str}") #создаем webappinfo - формат хранения url
      webAppTest2 = types.WebAppInfo(f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={str}") #создаем webappinfo - формат хранения url
      webAppTest3 = types.WebAppInfo(f"https://www.opencve.io/cve/{str}")  # создаем webappinfo - формат хранения url
      one_butt = types.KeyboardButton(text="Мы смогли найти на nist  информацию о CVE", web_app=webAppTest) #создаем кнопку типа webapp
      two_butt = types.KeyboardButton(text="Мы смогли найти на cve.mitre.org о CVE", web_app=webAppTest2)
      treebutt = types.KeyboardButton(text="Мы смогли найти на opencve.io о CVE", web_app=webAppTest3)
      exit = types.KeyboardButton("/exit")
      keyboard.add(one_butt,two_butt,treebutt,exit) #добавляем кнопки в клавиатуру
      return [1,keyboard] #возвращаем клавиатуру
   else:
      return [0,0]

def tryFind(str):
   url=f"https://www.opencve.io/cve?cvss=&search={str}"
   req=requests.request("get",url)
   if "No CVE found" in req.text:
      return 0
   else:
      return 1

def CVE_profuct_find(str,param):
   url=f"https://www.opencve.io/cve?cvss=&search={str}"
   if url[-1]=="-":
      url=url[0:-1]
   req = requests.request("get", url)
   if "No CVE found" in req.text:
      return []
   else:
      ls=0
      ans=[]
      for i in range(20):
         ls = req.text.find('"><strong>CVE-',ls)
         name=req.text[ls+len('"><strong>CVE-'):ls+len('"><strong>CVE-')+9]
         if req.text[ls+len('"><strong>CVE-')+9].isdigit():
            name+= req.text[ls+len('"><strong>CVE-')+9]
         ls=req.text.find('colspan="5">',ls)
         bs=req.text.find('</td>',ls)
         info=req.text[ls+len('colspan="5">'):bs]
         ans.append([name,info])
      print(ans)
      return ans

def Get_inline_marrkup(str):  # создание клавиатуры с webapp кнопкой
   if str[-1]=="-":
      str=str[0:-1]
   keyboard = types.InlineKeyboardMarkup(row_width= 2)  # создаем клавиатуру
   if tryFind(str):
      webAppTest = types.WebAppInfo(
         f"https://nvd.nist.gov/vuln/detail/{str}")  # создаем webappinfo - формат хранения url
      webAppTest2 = types.WebAppInfo(
         f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={str}")  # создаем webappinfo - формат хранения url
      webAppTest3 = types.WebAppInfo(f"https://www.opencve.io/cve/{str}")  # создаем webappinfo - формат хранения url

      one_butt =  types.InlineKeyboardButton(text="Мы смогли найти на nist  информацию о CVE",
                                      web_app=webAppTest)  # создаем кнопку типа webapp
      two_butt =  types.InlineKeyboardButton(text="Мы смогли найти на cve.mitre.org о CVE", web_app=webAppTest2)
      treebutt =  types.InlineKeyboardButton(text="Мы смогли найти на opencve.io о CVE", web_app=webAppTest3)

      keyboard.add(one_butt, two_butt, treebutt)  # добавляем кнопки в клавиатуру
      return [1, keyboard]  # возвращаем клавиатуру
   else:
      return [0, 0]


def translate(text):
   url = "https://microsoft-translator-text.p.rapidapi.com/translate"
   querystring = {"to[0]": "ru", "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}
   headers = {
      "content-type": "application/json",
      "X-RapidAPI-Key": "1a3b303d7amsh7a36f4fc816e8c5p1c21f3jsn46227ab75276",
      "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
   }
   payload = [{"Text": f"{text}"}]
   response = requests.post(url, json=payload, headers=headers, params=querystring)
   return response.json()[0]["translations"][0]["text"]