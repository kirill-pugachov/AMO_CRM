# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:25:05 2017

@author: Kirill
"""

#modules to work
import requests
import time
import send_list
import variables

#variables to work
#morion authorization parametrs
auth_morion = ('morion', '3b02be1a2f5821949f5ed644458869cc91811e32')

#урл запроса заказов
url = 'https://booking.geoapteka.com.ua/pop-order'
pause = 10

#урл запроса лек.форм
url_item = 'http://geoapt.morion.ua/get_item/'
url_shop = 'http://geoapt.morion.ua/get_shop/'

#Статус куда помещать поступивший заказ - Сайт
status_id_default = 13164489

#Словарь агентов получаемых из АПИ
agent_dict = {'GeoAPT': 'Сайт Геоаптека', 'GeoPharmacyBotUA': 'Телеграмм Бот', 'GeoPharmacyAosUA': 'Android приложение', 'GeoPharmacyiOSUA':'Apple приложение'}

#get data from api
def get_orders(url):
    try:
        get_orders = requests.post(url, auth=auth_morion, headers={'Connection':'close'})
        result = get_orders
    except:
        result = None
        print(type(result), 'trouble occure')
    return result

    
def positive_api_reply(get_orders_result):
    if get_orders_result:
        if get_orders_result.status_code == 200:
            return get_orders_result

            
def real_order_list(api_reply):
    result_list = []
    if api_reply.json():
        for order in api_reply.json():
            if order.get('test') is False:
                if order.get('phone'):
                    if order.get('id_order'):
                        if order.get('id_shop'):
                            if order.get('timestamp'):
                                if order.get('agent'):
                                    if order.get('state'):
                                        if order.get('data'):
                                            for row in order.get('data'):
                                                if row.get('id'):
                                                    if row.get('price'):
                                                        if row.get('quant'):
                                                            result_list.append(order)
        return result_list
    

#Функция получения данных препарата по его id
def get_drug(drug_id):
    try:
        drug = requests.get("http://geoapt.morion.ua/get_item/"+str(drug_id), headers={'Connection':'close'})
        drug.raise_for_status()
    except requests.exceptions.HTTPError:
        drug_out_result = {'name':'Нет связи с АПИ', 'form':'Нет связи с АПИ', 'dose':'Нет связи с АПИ', 'pack':'Нет связи с АПИ', 'numb':'Нет связи с АПИ', 'make':'Нет связи с АПИ'}
    else:
        drug_out = drug.json()
        if drug_out['name']=='' and  drug_out['form']=='' and drug_out['dose']=='' and drug_out['pack']=='' and drug_out['numb']=='' and drug_out['make']=='':
            drug_out_result = {'name':'Нет в АПИ', 'form':'Нет в АПИ', 'dose':'Нет в АПИ', 'pack':'Нет в АПИ', 'numb':'Нет в АПИ', 'make':'Нет в АПИ'}
        else:
            drug_out_result=drug.json()                    
    return drug_out_result         


#получаем данные аптеки и по препарату по adress_id и drug_id
def get_shop_object(url_shop, adress_id):
    shop_data_object = requests.get(url_shop + str(adress_id), headers={'Connection':'close'})
    return shop_data_object


def get_shop_data(shop_data_object):
    if shop_data_object.status_code == 200:
        if shop_data_object:
            shop_data = shop_data_object
            return shop_data
    

def get_shop_parametrs(shop_data):
    shop_parametrs = shop_data.json()
    return shop_parametrs
    

def get_shop(url_shop, adress_id):
    return get_shop_parametrs(get_shop_data(get_shop_object(url_shop, adress_id)))


def lead_shop_forming(shop, new_lead):
    new_lead['request']['leads']['add'][0]['custom_fields'][5]['values'][0]['value'] = shop.get('mark', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][6]['values'][0]['value'] = shop.get('addr_city', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][7]['values'][0]['value'] = shop.get('addr_street', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][8]['values'][0]['value'] = shop.get("cont_phone", 'Не указано в АПИ') + ", " + shop.get('sale_phone', 'Не указано в АПИ')        
    return new_lead


def lead_drug_forming(drug, new_lead):
    new_lead['request']['leads']['add'][0]['name'] = drug.get('name', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][0]['values'][0]['value'] = drug.get('name', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][4]['values'][0]['value'] = drug.get('form', 'Не указано в АПИ') + ' ' + drug.get('note', 'Не указано в АПИ') + ' ' + drug.get('make', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][10]['values'][0]['value'] = drug.get('numb', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][11]['values'][0]['value'] = drug.get('dose', 'Не указано в АПИ')    
    return new_lead
    
    
def lead_order_forming(order, new_lead):
    new_lead['request']['leads']['add'][0]['date_create'] = order.get('timestamp', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['last_modified'] = order.get('timestamp', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['status_id'] = status_id_default
    new_lead['request']['leads']['add'][0]['custom_fields'][1]['values'][0]['value'] = order.get('id_order', 'Не указано в АПИ')
    if order.get('id_shop') in send_list.send_list:
        new_lead['request']['leads']['add'][0]['custom_fields'][12]['values'][0]['value'] = '1'
    return new_lead

    
def lead_lek_forma_forming(lek_forma, new_lead):
    new_lead['request']['leads']['add'][0]['custom_fields'][2]['values'][0]['value'] = lek_forma.get('quant', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['custom_fields'][3]['values'][0]['value'] = lek_forma.get('price', 'Не указано в АПИ')
    new_lead['request']['leads']['add'][0]['price'] = lek_forma.get('price', 0) * lek_forma.get('quant', 0)
    return new_lead

    
def lead_source_forming(agent_dict, new_lead, order):
    if order['agent'] == 'GeoAPT':
        new_lead['request']['leads']['add'][0]['custom_fields'][9]['values'][0]['value'] = agent_dict[order['agent']]
        new_lead['request']['leads']['add'][0]['tags'] = agent_dict[order['agent']]
    elif order['agent'] == 'GeoPharmacyBotUA':
        new_lead['request']['leads']['add'][0]['custom_fields'][9]['values'][1]['value'] = agent_dict[order['agent']]
        new_lead['request']['leads']['add'][0]['tags'] = agent_dict[order['agent']]
    elif order['agent'] == 'GeoPharmacyAosUA':
        new_lead['request']['leads']['add'][0]['custom_fields'][9]['values'][2]['value'] = agent_dict[order['agent']]
        new_lead['request']['leads']['add'][0]['tags'] = agent_dict[order['agent']]
    else:
        new_lead['request']['leads']['add'][0]['custom_fields'][9]['values'][3]['value'] = '9191 Телефон'
        new_lead['request']['leads']['add'][0]['tags'] = agent_dict[order['agent']]          
    return new_lead


def new_deal(lead_shop_forming, lead_drug_forming, lead_order_forming, lead_lek_forma_forming, lead_source_forming):
    shop = get_shop(url_shop, order['id_shop'])
    drug = get_shop(url_item, lek_forma['id'])
    new_lead = variables.data_to_send
    new_lead = lead_shop_forming(shop, new_lead)
    new_lead = lead_drug_forming(drug, new_lead)
    new_lead = lead_order_forming(order, new_lead)
    new_lead = lead_lek_forma_forming(lek_forma, new_lead)
    new_lead = lead_source_forming(agent_dict, new_lead, order)
    return new_lead
        
result = set()
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