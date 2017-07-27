# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:36:31 2017

@author: Kirill
"""
import requests


#Set variables to get leads from AMO CRM
user_login='v.shulha@proximaresearch.com'
user_hash='c62705082bcff19796c55ef5a105054d'
domen='https://geoapteka.amocrm.ru'
auth='/private/api/auth.php'
deals_list_url='/private/api/v2/json/leads/list'


#Get cookies from AMO CRM
def logging_to_AMO(user_login, user_hash, domen, auth):
    r = requests.post(domen+auth, data = {'USER_LOGIN':user_login, 'USER_HASH':user_hash, 'type': 'json'})    
    return r.cookies


#отправляем телефон клиента в АМО ЦРМ
def get_deals_list_from_AMO(domen, deals_list_url, jar):
    deals_list_result = []
    try:
        deals_list_get = requests.get(domen + deals_list_url, cookies=jar, data={'type': 'json'})
    except requests.exceptions.HTTPError:
        deals_list_result = []
    else:
        deals_list_result = deals_list_get
    return deals_list_result


def get_full_deals_list_AMO():
    row_in_block = 0
    result_deals_list = []
    jar = logging_to_AMO(user_login, user_hash, domen, auth)
    deals_list = get_deals_list_from_AMO(domen, (deals_list_url + '?full=Y&limit_rows=500' + '&limit_offset=' + str(row_in_block)), jar)
    result_deals_list.extend((deals_list.json())['response']['leads'])
    while len(deals_list.json()['response']['leads']) == 500:
        row_in_block +=500
        deals_list = get_deals_list_from_AMO(domen, (deals_list_url + '?full=Y&limit_rows=500' + '&limit_offset=' + str(row_in_block)), jar)
        result_deals_list.extend((deals_list.json())['response']['leads'])
    return result_deals_list


full_deals_list =  get_full_deals_list_AMO()
print(len(full_deals_list))