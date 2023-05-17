
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


def pars_info(str):
   s = f"https://www.opencve.io/cve/{str}"
   s= requests.request("get",s).text
   s = s[s.find("reference_data"):]
   i = s.find("http")
   ans = {"links": []}
   if 'url&#34;:34;' in s:
      while i < s.find("impactScore") and i != -1:
         ans["links"].append(s[i:s.find(";", i)].replace("&#34", ""))
         s = s[s.find(";", i):]
         if i < s.find("impactScore") and i != -1:
            i = s.find("http")
         else:
            break
   else:
      ans["links"].append("None")
   if "impactScore" in s:
      ans["impactScore"] = s[s.find(":", s.find("impactScore")) + 1:s.find(",", s.find("impactScore"))].replace("\n",
                                                                                                                "").replace(
         "\t", "")
   else:
      ans["impactScore"]="None"
   if "exploitabilityScore" in s:
      ans["exploitabilityScore"] = s[
                                   s.find(":", s.find("exploitabilityScore")) + 1:s.find("}",
                                                                                         s.find("exploitabilityScore"))]
   else:
      ans["exploitabilityScore"]="None"
   if "publishedDate" in s:
      ans["publishedDate"] = s[s.find(":", s.find("publishedDate")) + 1:s.find(",", s.find("publishedDate"))].replace("\n",
                                                                                                                      "").replace(
         "\t", "")
      ans["publishedDate"] = ans["publishedDate"].replace("&#34;", "")
   else:
      ans["publishedDate"]="None"
   if "CVSS" in s:
      ans["CVSS"] = s[s.find("CVSS") + 5:s.find("/", s.find("CVSS"))]
   else:
      ans["CVSS"]="None"
   if "ID" in s:
      ans["ID"] = s[s.find(":", s.find("ID")) + 2:s.find(",", s.find("ID"))]
      ans["ID"] = ans["ID"].replace("&#34;", "")
   else:
      ans["ID"]="None"
   return ans