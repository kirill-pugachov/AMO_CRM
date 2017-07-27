# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 14:14:30 2017

@author: Kirill
"""

import requests, datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


#Запись выполненных заказов
#Куда писать
save_path='C:/Python/Service/AMO/'
#Все полученные заказы
orders_file='all_orders_income.log'
#Все отправленные на почту
send_mail_file='send_mail_orders.log'
#Все добавленные в АМО ЦРМ
amo_add_file='amo_add_orders.log'

#Задаем переменные для отправки в АМО заказов
user_login='v.shulha@proximaresearch.com'
user_hash='c62705082bcff19796c55ef5a105054d'
domen='https://geoapteka.amocrm.ru'
auth='/private/api/auth.php'
deal_list='/private/api/v2/json/leads/list?limit_offset=3200&limit_rows=50'
account_info='m/private/api/v2/json/accounts/current'
add_deal='/private/api/v2/json/leads/set'
contact_list_url='/private/api/v2/json/contacts/list'
contact_set_url='/private/api/v2/json/contacts/set'

#отправка почты - общий раздел
#отправитель
user='order@geoapteka.ua'#'geoapteka.com.ua@gmail.com'
#пароль
pwd='NgrQdtBx5Yox'#utjfgntrf'
#получатель
recipient=['shadow199@bigmir.net','pugachovk@gmail.com']
#Тема письма
subject='Ordrers from Geoapteka'
#Тело сообщения
body='Заказы с сайта Geoapteka'+'\n'+'\n'

#список рассылки
send_list = {
	'444838': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.406@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'469135': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.117@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'564162': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.176@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'4151015': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','lv.678@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1944369': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','zt.445@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'628986': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','lv.223@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'922073': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.254@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'937765': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.271@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'564038': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.145@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2507531': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.558@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'943931': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.279@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1546078': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.426@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'446909': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.197@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'447025': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','cn.203@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'446734': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.187@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'470073': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.192@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'446694': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.185@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'445045': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.109@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2133556': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','lv.463@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'446458': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.168@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'444840': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.331@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'947196': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.341@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'565537': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','cn.204@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2345323': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','lv.499@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2507565': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.559@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2507573': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.561@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'3066497': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','if.641@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'3079391': ['biloshicka.t@watsons.ua','kovernyak.s@watsons.ua','kv.632@watsons.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1254426': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'920448': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'972711': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'952328': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'953609': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1449607': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'970899': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1248138': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1545767': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1939671': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'921756': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'946777': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1449600': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1445521': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'947273': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2104943': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2717583': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'1606478': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2919514': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2975320': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2975312': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2963108': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
	'2961750': ['zakaz_site@apteka24.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '941969' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '954215' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '951580' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '996094' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1504960' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1018356' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1018357' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1123825' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1157372' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1260578' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '1260583' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'], 
      '2203177' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'], 
      '946997' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'], 
      '2423454' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'], 
      '2442047' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'], 
      '2436445' : ['reserv@aptekamirra.com.ua', 'a.melnichuk@aptekamirra.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'], 
      '448079':['rezerv5_7@e-apteka.com.ua','ogorodniychuk@e-apteka.com.ua','lytvynenko@e-apteka.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '469112':['rezerv5_7@e-apteka.com.ua','ogorodniychuk@e-apteka.com.ua','lytvynenko@e-apteka.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '471764':['rezerv5_7@e-apteka.com.ua','ogorodniychuk@e-apteka.com.ua','lytvynenko@e-apteka.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '446319':['rezerv5_7@e-apteka.com.ua','ogorodniychuk@e-apteka.com.ua','lytvynenko@e-apteka.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '446320':['rezerv5_7@e-apteka.com.ua','ogorodniychuk@e-apteka.com.ua','lytvynenko@e-apteka.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '469106':['rezerv5_7@e-apteka.com.ua','ogorodniychuk@e-apteka.com.ua','lytvynenko@e-apteka.com.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua'],
      '2469190':['apteka0961241590@yandex.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua','geoapteka.com.ua@gmail.com'],
      '1254757':['apteka0961241590@yandex.ua','natalya.karandasheva@geoapteka.ua','anna.stadnik@proximaresearch.com','geoapteka.com.ua@gmail.com','nadiia.honchar@proximaresearch.com.ua','geoapteka.com.ua@gmail.com']    
}

send_list_1 = {
      '444838': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'469135': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'564162': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'630507': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1944369': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'628986': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'922073': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'937765': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'564038': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2507531': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'943931': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1546078': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'446909': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'447025': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'446734': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'470073': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'446694': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'445045': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2133556': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'446458': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'444840': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'947196': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'565537': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2345323': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2507565': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2507573': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'3066497': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'3079391': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1254426': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'920448': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'972711': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'952328': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'953609': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1449607': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'970899': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1248138': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1545767': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1939671': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'921756': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'946777': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1449600': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1445521': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'947273': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2104943': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2717583': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'1606478': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2919514': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2975320': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2975312': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2963108': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com'],
	'2961750': ['viacheslav.bilous@gmail.com', 'pugachovk@gmail.com']
}


#Задаем переменные для забора заказов
status_id_default=13164489
#урл запроса заказов
url = 'https://booking.geoapteka.com.ua/pop-order'#  http://195.128.18.78:9080/pop-order
#урл обновления заказов
url_upd='https://booking.geoapteka.com.ua/upd-order' # http://195.128.18.78:9080/upd-order
#список результатов бронирования
orders_result=[]
#период проверки поступления заказов
pause=20
#период повторной отправки подтверждения заказа в апи, чтобы не приходил второй раз
pause1=5
#шаблон отправки сделки
data_to_send={
	'request': {
		'leads': {
			'add': [{
				'name': 'Тест добавление заказов с сайта',
				'date_create': 0,
				'last_modified': 0,
				'status_id': 13164489,
				'price': 0,
				'tags': 'Заявка с сайта-новый контакт',
				'custom_fields': [{
					'values': [{
						'value': ''
					}],
					'id': '250770',
					'name': 'Наименование'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '427368',
					'name': 'Номер заказа'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250736',
					'name': 'Количество упаковок'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250764',
					'name': 'Цена упаковки'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250776',
					'name': 'Лекформа'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250850',
					'name': 'Бренд Аптеки'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250854',
					'name': 'Город'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250856',
					'name': 'Адрес'
				}, {
					'values': [{
						'value': ''
					}],
					'id': '250898',
					'name': 'Телефон аптеки'
				}]
			}]
		}
	}
}
#Шаблон отправки нового контакта
contact_to_send={
	'request': {
		'contacts': {
			'add': [{
				'name': 'Новый контакт с сайта',
				'date_create': 0,
				'last_modified': 0,
				'responsible_user_id': 1001278,
				'linked_leads_id': [
					
				],
				'company_name': '',
				'tags': 'Заявка с сайта',
				"custom_fields": [{
					'name': 'Телефон',
					'code': 'PHONE',
					'id': '244556',
					'values': [{
						'enum': '561776',
						'value': ''
					}]
				}]
			}]
		}
	}
}

#Шаблон для обновления контакта
contact_to_update={
	'request': {
		'contacts': {
			'update': [{
				'id': 0,
                       'last_modified': 0,    
				'linked_leads_id': [],
				'tags': 'Старый Клиент - заявка с сайта',

			}]
		}
	}
}




#post получаем все заказы из API
def get_orders(url):
    try:
        get_orders = requests.post(url, auth=('morion', '3b02be1a2f5821949f5ed644458869cc91811e32'), headers={'Connection':'close'})
        result = get_orders
#        print(type(result))
    except:
        result = None
        print(type(result), 'trouble occure')
    return result
    
#post отправляем заказ с измененным статусом
def upd_orders(url_upd, order):
    try:
        upd_orders=requests.post(url_upd, json=order, auth=('morion', '3b02be1a2f5821949f5ed644458869cc91811e32'), headers={'Connection':'close'})
        upd_orders.raise_for_status()
    except requests.exceptions.HTTPError:
        return upd_orders.status_code
    else:
        return upd_orders.status_code
    return  upd_orders.status_code

#получение информации по аптеке
def get_shop(shop_id):
    try:   
        shop = requests.get("http://geoapt.morion.ua/get_shop/"+str(shop_id), headers={'Connection':'close'})
        shop.raise_for_status()
    except requests.exceptions.HTTPError:
        shop_out = {'mark':'Нет в АПИ', 'addr_city':'Нет в АПИ', 'addr_street':'Нет в АПИ', 'cont_phone':'Нет в АПИ', 'sale_phone':'Нет в АПИ'}
    else:
        shop_out = shop.json()
    return shop_out  

#Функция получения данных препарата по его id
def get_drug(drug_id):
    try:
        drug = requests.get("http://geoapt.morion.ua/get_item/"+str(drug_id), headers={'Connection':'close'})
        drug.raise_for_status()
    except requests.exceptions.HTTPError:
        drug_out_result = {'name':'Нет в АПИ', 'form':'Нет в АПИ', 'dose':'Нет в АПИ', 'pack':'Нет в АПИ', 'numb':'Нет в АПИ', 'make':'Нет в АПИ'}
    else:
        drug_out = drug.json()
        if drug_out['name']=='' and  drug_out['form']=='' and drug_out['dose']=='' and drug_out['pack']=='' and drug_out['numb']=='' and drug_out['make']=='':
            drug_out_result = {'name':'Нет в АПИ', 'form':'Нет в АПИ', 'dose':'Нет в АПИ', 'pack':'Нет в АПИ', 'numb':'Нет в АПИ', 'make':'Нет в АПИ'}
        else:
            drug_out_result=drug.json()                    
    return drug_out_result 


#Формируем строку с названием заказанного препарата
def ordered_drug(drug_out):
    ordered_drug=drug_out['name'] + ' ' + drug_out['make'] + ', '+'Форма выпуска: '+drug_out['form']+', '+'Дозировка: '+drug_out['dose']+', '+'Номер в упаковке: '+ drug_out['numb'] + drug_out['note']    
    return ordered_drug 
     
    
#Функция получения телефонного номера клиента        
def get_client_number(order):
    try:
        a=order['phone']
    except KeyError:
        a='нет номера телефона в АПИ'
    return a    
#Соединяемся с АПИ АМО ЦРМ
def logging_to_AMO(user_login, user_hash, domen, auth):
    r = requests.post(domen+auth, data = {'USER_LOGIN':user_login, 'USER_HASH':user_hash, 'type': 'json'})    
    return r.cookies

#Отправляем сделку в АМО ЦРМ
def send_deals_to_AMO(domen, add_deal, jar, deal_to_send):
    deal_list_send=requests.post(domen+add_deal, cookies=jar, json=deal_to_send)
    if deal_list_send.status_code==200:
        deal_list_send_info=deal_list_send.json()   
        return deal_list_send_info['response']['leads']['add'][0]['id']

#отправляем телефон клиента в АМО ЦРМ
def get_phone_from_AMO(domen, contact_list, jar, order):
    contact_list_result=0
    try:
        contact_list_get=requests.get(domen+contact_list_url+'?query=' + get_client_number(order), cookies=jar, data={'type': 'json'})
    except requests.exceptions.HTTPError:
        contact_list_result=[]
    else:
        contact_list_result=contact_list_get
    return contact_list_result
    
#Добавляем новый контакт в АМО ЦРМ
def post_new_contact_to_AMO(domen, contact_set_url, jar, client_to_sent):
    contact_sent_to_AMO=requests.post(domen+contact_set_url, cookies=jar, json=client_to_sent)
    return contact_sent_to_AMO.status_code   

def new_deal_send_to_AMO(data_to_send, raw, order):
    deal_to_send=data_to_send
    deal_to_send['request']['leads']['add'][0]['name']=get_drug(raw['id'])['name']
    deal_to_send['request']['leads']['add'][0]['date_create']=order['timestamp']
    deal_to_send['request']['leads']['add'][0]['last_modified']=order['timestamp']
    deal_to_send['request']['leads']['add'][0]['status_id']=status_id_default
    deal_to_send['request']['leads']['add'][0]['price']=raw['price']*raw['quant']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][0]['values'][0]['value']=get_drug(raw['id'])['name']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][1]['values'][0]['value']=order['id_order']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][2]['values'][0]['value']=raw['quant']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][3]['values'][0]['value']=raw['price']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][4]['values'][0]['value']=get_drug(raw['id'])['form'] + get_drug(raw['id'])['dose'] + get_drug(raw['id'])["pack"] + get_drug(raw['id'])["numb"] + get_drug(raw['id'])["note"] + get_drug(raw['id'])["make"]
    deal_to_send['request']['leads']['add'][0]['custom_fields'][5]['values'][0]['value']=get_shop(order['id_shop'])['mark']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][6]['values'][0]['value']=get_shop(order['id_shop'])['addr_city']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][7]['values'][0]['value']=get_shop(order['id_shop'])['addr_street']
    deal_to_send['request']['leads']['add'][0]['custom_fields'][8]['values'][0]['value']=get_shop(order['id_shop'])["cont_phone"]+ ", " + get_shop(order['id_shop'])["sale_phone"]    
    return deal_to_send

#создаем новый контакт в АМО ЦРМ    
def new_contact_send_to_AMO(contact_to_send, raw, order, deal_id):
    client_to_send=contact_to_send
    client_to_send['request']['contacts']['add'][0]['date_create']=order['timestamp']
    client_to_send['request']['contacts']['add'][0]['last_modified']=order['timestamp']
    client_to_send['request']['contacts']['add'][0]['custom_fields'][0]['values'][0]['value']=get_client_number(order)
    client_to_send['request']['contacts']['add'][0]['linked_leads_id']=[str(deal_id)]
    return client_to_send

#Изменяем существующий контакт в АМО ЦРМ
def contact_to_update_in_AMO(contact_to_update, order, exist_contact, exist_deals, old_client_in_AMO, pause):
    contact_to_update_in_AMO=contact_to_update
    contact_to_update_in_AMO['request']['contacts']['update'][0]['id']=exist_contact    
    contact_to_update_in_AMO['request']['contacts']['update'][0]['linked_leads_id']=exist_deals
    if order['timestamp']>=old_client_in_AMO['response']['contacts'][0]['last_modified']:
        contact_to_update_in_AMO['request']['contacts']['update'][0]['last_modified']=order['timestamp']
    else:
        contact_to_update_in_AMO['request']['contacts']['update'][0]['last_modified']=old_client_in_AMO['response']['contacts'][0]['last_modified']+pause
    return contact_to_update_in_AMO

#ВРЕМЯ И ВСЕ О НЁМ
#Функция получения представления времени чч-мм-сс-дд-мм-гг из timestamp         
def get_time(from_this_time_sent):
    try:
        value = datetime.datetime.fromtimestamp(from_this_time_sent).strftime('%H:%M:%S %d.%m.%Y')
    except OSError:
        value = datetime.datetime.fromtimestamp(1)   
    return value

#ПОЧТА В КОЛЛ_ЦЕНТР    
#отправка письма
def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd

    TO = recipient if type(recipient) is list else [recipient]
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user
    msg['To'] = ", ".join(TO)
    try:
        server = smtplib.SMTP('post.morion.ua', 25)#("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(msg['From'],TO , msg.as_string())
        server.close()
        a='successfully sent the mail'
    except:
        a="failed to send mail"
    return a

def send_mail_to_client(order, send_list_1):
    subject = 'Заказ от Геоаптеки №' +order['id_order'] + ' от ' +  get_time(order['timestamp']) +' '+'{} ({})'.format(get_shop(order['id_shop'])['name'], get_shop(order['id_shop'])['mark'])+'\n'
    ryadok0 = 'Заказанный товар: {}'.format(ordered_drug(get_drug(raw['id']))) + '\n' + 'Количество: {} шт'.format(raw['quant']) + '\n' + 'Цена: {} грн'.format(raw['price']) + '\n' +  'Сумма к оплате: {} грн'.format(raw['quant']*raw['price']) + '\n' + '\n'
    ryadok1 = 'Телефон покупателя: +{}'.format(order['phone']) + '\n' + 'Номер аптеки: {} ({})'.format(get_shop(order['id_shop'])['name'], get_shop(order['id_shop'])['mark']) + '\n' + 'Адрес: {}'.format(get_shop(order['id_shop'])['addr_city'] + ', ' + get_shop(order['id_shop'])['addr_street']) + '\n' + '\n'
    ryadok2 = 'Время заказа: {}'.format(get_time(order['timestamp'])) + '\n' + 'Номер заказа Geoapteka: {}'.format(order['id_order']) + '\n' + '\n'
    ryadok3 = 'Номер заказа:' + '\n' + 'С какого времени можно забрать из аптеки (ориентировочно):' + '\n' + 'Примечание:' + '\n' + '\n'
    body=ryadok0+ryadok1+ryadok2+ryadok3
    recipient=send_list_1.get(order['id_shop'])
    return send_email(user, pwd, recipient, subject, body)

#запись файла на диск (для логов)
def write_to_disk (save_path, orders_file, order):
    with open(save_path+orders_file, 'a', newline='') as log_file:
            log_file.write(str(order)+'\n')    
        
while True:
    get_orders_result = get_orders(url)
    if get_orders_result is not None:
        if get_orders_result.status_code == 200:
            if get_orders_result.json():
                print('Всего заказов полученных в API',len(get_orders_result.json()), get_time(time.time()))
                for order in get_orders_result.json():
#                    print('Всего заказов полученных в API',len(get_orders_result.json()), get_time(time.time()))
                    if order['test'] is False:# or order['test'] is True
                        if 'data' in order.keys() and order['data']:
                            write_to_disk (save_path, orders_file, order)
        #отправляем заказ на почту, если id_shop в списке рассылки
                            if order['id_shop'] in send_list.keys():
                                for raw in order['data']:
                                    if send_mail_to_client(order, send_list)=='successfully sent the mail':
                                        write_to_disk (save_path, send_mail_file, order)
                                        print('Почта отправилась', '{} ({})'.format(get_shop(order['id_shop'])['name'], get_shop(order['id_shop'])['mark']))
        #включаем счетчик для контроля полноты отправленных в АМО заказов                            
                            count_sending=0
                            for raw in order['data']:                                            
                                if raw['id']:
                                    jar = logging_to_AMO(user_login, user_hash, domen, auth)
                                    contact_list=get_phone_from_AMO(domen, contact_list_url, jar, order)
            
        #Проверяем наличие телефона в контактах по ответу АПИ АМО ЦРМ, код 200 - телефон есть, возможно есть несколько раз
                                    if contact_list.status_code==200:
                                        old_client_in_AMO=contact_list.json()
                                        exist_contact=old_client_in_AMO['response']['contacts'][0]['id']
                                        exist_deals=old_client_in_AMO['response']['contacts'][0]['linked_leads_id']
                                        exist_deals.append(str(send_deals_to_AMO(domen, add_deal, jar, new_deal_send_to_AMO(data_to_send, raw, order))))
                                        update_exist_contact=contact_to_update_in_AMO(contact_to_update, order, exist_contact, exist_deals, old_client_in_AMO, pause)
            
                                        if post_new_contact_to_AMO(domen, contact_set_url, jar, update_exist_contact)==200:
                                            count_sending+=1
        
        #Данный номер телефона в АПИ АМО ЦРМ не представлен 204 код                                                                              
                                    elif contact_list.status_code==204:
                                        new_deal_to_send=new_deal_send_to_AMO(data_to_send, raw, order)
                                        new_deal_id=send_deals_to_AMO(domen, add_deal, jar, new_deal_to_send)
                                        new_client_to_send=new_contact_send_to_AMO(contact_to_send, raw, order, new_deal_id)
                                        
                                        if post_new_contact_to_AMO(domen, contact_set_url, jar, new_client_to_send)==200:
                                            count_sending+=1
                                    
                            if count_sending==len(order['data']):
                                order['state']='Kostyl'
                                if upd_orders(url_upd, order)==200:
                                    write_to_disk (save_path, amo_add_file, order)
                                    count_sending=0
             
#Делаем паузу до следующего забора данных    
    for i in range(pause):
        time.sleep(1)
