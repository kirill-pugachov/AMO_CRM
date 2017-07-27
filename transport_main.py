# -*- coding: utf-8 -*-
"""
Created on Tue May 30 12:11:01 2017

@author: Kirill
"""

#транспорт заказов
from get_data_from_api import get_orders, positive_api_reply, real_order_list, get_shop, new_deal, url_shop, lead_shop_forming, lead_drug_forming, lead_order_forming, lead_lek_forma_forming, lead_source_forming
import time
import send_list
import variables
from get_data_from_api import url, pause
import smtplib
from email.mime.text import MIMEText
from email.header import Header

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



#ВРЕМЯ И ВСЕ О НЁМ
#Функция получения представления времени чч-мм-сс-дд-мм-гг из timestamp         
def get_time(from_this_time_sent):
    try:
        value = datetime.datetime.fromtimestamp(from_this_time_sent).strftime('%H:%M:%S %d.%m.%Y')
    except OSError:
        value = datetime.datetime.fromtimestamp(1)   
    return value


#ПОЧТА В ТИМ-СОФТ ЧТОБЫ ИМ ХОРОШО БЫЛО    
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

def send_mail_to_client(order, send_list_1, key = 'id_shop'):
    subject = 'Заказ от Геоаптеки №' +order['id_order'] + ' от ' +  get_time(order['timestamp']) +' '+'{} ({})'.format(get_shop(order['id_shop'])['name'], get_shop(order['id_shop'])['mark'])+'\n'
    ryadok0 = 'Заказанный товар: {}'.format(ordered_drug(get_drug(raw['id']))) + '\n' + 'Количество: {} шт'.format(raw['quant']) + '\n' + 'Цена: {} грн'.format(raw['price']) + '\n' +  'Сумма к оплате: {} грн'.format(raw['quant']*raw['price']) + '\n' + '\n'
    ryadok1 = 'Телефон покупателя: +{}'.format(order['phone']) + '\n' + 'Номер аптеки: {} ({})'.format(get_shop(order['id_shop'])['name'], get_shop(order['id_shop'])['mark']) + '\n' + 'Адрес: {}'.format(get_shop(order['id_shop'])['addr_city'] + ', ' + get_shop(order['id_shop'])['addr_street']) + '\n' + '\n'
    ryadok2 = 'Время заказа: {}'.format(get_time(order['timestamp'])) + '\n' + 'Номер заказа Geoapteka: {}'.format(order['id_order']) + '\n' + '\n'
    ryadok3 = 'Номер заказа:' + '\n' + 'С какого времени можно забрать из аптеки (ориентировочно):' + '\n' + 'Примечание:' + '\n' + '\n'
    body=ryadok0+ryadok1+ryadok2+ryadok3
    recipient=send_list_1.get(order[key])
    return send_email(user, pwd, recipient, subject, body)

result = {}
while True:
    get_orders_result = get_orders(url)
    api_replay = positive_api_reply(get_orders_result)
    real_orders = real_order_list(api_replay)
    for order in real_orders:
        if order.get('agent'):
            result.add(order.get('agent'))
            print(get_shop(url_shop, order['id_shop']), '\n')
            for lek_forma in order['data']:
                print(new_deal(lead_shop_forming, lead_drug_forming, lead_order_forming, lead_lek_forma_forming, lead_source_forming))
            if order.get('id_shop') in send_list.send_list:
                print('e-mail sent to the pharmacy')
    for i in range(pause):
        time.sleep(1)
    print(result, len(result))