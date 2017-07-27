# -*- coding: utf-8 -*-
"""
Created on Wed May  3 15:42:56 2017

@author: Kirill
"""

#modules to work
import requests

#Задаем переменные для отправки в АМО заказов
user_login='v.shulha@proximaresearch.com'
user_hash='c62705082bcff19796c55ef5a105054d'
domen='https://geoapteka.amocrm.ru'
auth='/private/api/auth.php'
contact_list_url='/private/api/v2/json/contacts/list'




#Соединяемся с АПИ АМО ЦРМ
def logging_to_AMO(user_login, user_hash, domen, auth):
    r = requests.post(domen+auth, data = {'USER_LOGIN':user_login, 'USER_HASH':user_hash, 'type': 'json'})    
    return r.cookies


#отправляем телефон клиента в АМО ЦРМ
def get_phone_list_from_AMO(domen, contact_list_url, jar):
    contact_list_result = []
    try:
        contact_list_get = requests.get(domen+contact_list_url, cookies=jar, data={'type': 'json'})
    except requests.exceptions.HTTPError:
        contact_list_result = []
    else:
        contact_list_result = contact_list_get
    return contact_list_result

    
def full_contact_list_AMO():
    row_in_block = 0
    result_contact_list = []
    jar = logging_to_AMO(user_login, user_hash, domen, auth)
    contact_list = get_phone_list_from_AMO(domen, (contact_list_url + '?full=Y&limit_rows=500' + '&limit_offset=' + str(row_in_block)), jar)
    result_contact_list.extend((contact_list.json())['response']['contacts'])
    while len(contact_list.json()['response']['contacts']) == 500:
        row_in_block +=500
        contact_list = get_phone_list_from_AMO(domen, (contact_list_url + '?full=Y&limit_rows=500' + '&limit_offset=' + str(row_in_block)), jar)
        result_contact_list.extend((contact_list.json())['response']['contacts'])
    return result_contact_list

def get_full_fields_plan_AMO():
    jar = logging_to_AMO(user_login, user_hash, domen, auth)
    fields_list = requests.get(domen+'/private/api/v2/json/accounts/current', cookies=jar, data={'type': 'json'})
    return fields_list.json()
    
    
full_contact_list =  full_contact_list_AMO()
print(len(full_contact_list))
full_fields_plan = get_full_fields_plan_AMO()
print(len(full_fields_plan))






   
#jar = logging_to_AMO(user_login, user_hash, domen, auth)
#row_in_block = 0
#result_contact_list = []
#contact_list = get_phone_list_from_AMO(domen, (contact_list_url + '?full=Y&limit_rows=500' + '&limit_offset=' + str(row_in_block)), jar)
#result_contact_list.extend((contact_list.json())['response']['contacts'])
#
#print(len(result_contact_list))
#
#while len(contact_list.json()['response']['contacts']) == 500:
#    row_in_block +=500
#    contact_list = get_phone_list_from_AMO(domen, (contact_list_url + '?full=Y&limit_rows=500' + '&limit_offset=' + str(row_in_block)), jar)
#    result_contact_list.extend((contact_list.json())['response']['contacts'])
#    print(len(result_contact_list))
#    print(contact_list.status_code)
    

#print(contact_list.status_code)

