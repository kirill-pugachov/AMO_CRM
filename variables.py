# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:09:13 2017

@author: Kirill
"""

#data send structure
#шаблон отправки сделки
data_to_send={
    "request": {
        "leads": {
            "add": [
                {
                    "name": "Тест добавление заказов с сайта",
                    "date_create": 0,
                    "last_modified": 0,
                    "status_id": 13164489,
                    "price": 0,
                    "tags": "Заявка с сайта-новый контакт",
                    "custom_fields": [
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250770",
                            "name": "Наименование"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "427368",
                            "name": "Номер заказа"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250736",
                            "name": "Количество упаковок"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250764",
                            "name": "Цена упаковки"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250776",
                            "name": "Лекформа"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250850",
                            "name": "Бренд Аптеки"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250854",
                            "name": "Город"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250856",
                            "name": "Адрес"
                        },
                        {
                            "values": [
                                {
                                    "value": ""
                                }
                            ],
                            "id": "250898",
                            "name": "Телефон аптеки"
                        },
                        {
                            "id": "436537",
                            "name": "Источник сделки",
                            "values": [
                                {
                                    "enum": "987959",
                                    "value": ""
                                },
                                {
                                    "enum": "987961",
                                    "value": ""
                                },
                                {
                                    "enum": "987963",
                                    "value": ""
                                },
                                {
                                    "enum": "988773",
                                    "value": ""
                                }
                            ]
                        },
                        {
                            "id": "250762",
                            "name": "В упаковке",
                            "values": [
                                {
                                    "value": "3"
                                }
                            ]
                        },
                        {
                            "id": "250768",
                            "name": "Дозировка",
                            "values": [
                                {
                                    "value": "1 мг"
                                }
                            ]
                        },
                        {
                            "id": "436731",
                            "name": "E-MAIL с заказом отправлен в аптеку",
                            "values": [
                                {
                                    "value": "0"
                                }
                            ]
                        }
                    ]
                }
            ]
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
