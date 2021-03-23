#!/usr/bin/python

import telebot
from telebot import types
#import wrong_parsing
from bs4 import BeautifulSoup
import requests as req
import re
from array import *

API_TOKEN = '1769942020:AAHV2XgSW6QfkHqOGLIygm2oKYbh9Dm8cb0'

resp = req.get("https://timetable.tusur.ru/faculties/fb/groups/717-1")
soup = BeautifulSoup(resp.text, 'lxml')
all_table = soup.find('div', {'class':['timetable_wrapper']})
tables = all_table.find('div', {'class':['table-responsive']})

bot = telebot.TeleBot(API_TOKEN)
#keyboard1 = telebot.types.ReplyKeyboardMarkup(selective=True)
#keyboard1.row('Timetable')
keyboard_timetable = telebot.types.InlineKeyboardMarkup()
key_timetable = types.InlineKeyboardButton(text='Вывести рассписание', callback_data='timetable')
keyboard_timetable.add(key_timetable)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, это бот Расписания ТУСУР ФБ 717-1', reply_markup=keyboard_timetable)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, "Напиши Timetable или нажми на команду /start")

@bot.message_handler(content_types=['text']) 
def get_text_messages(message):
    if message.text == "Timetable":
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_monday = types.InlineKeyboardButton(text='Понедельник', callback_data='monday')
        keyboard.add(key_monday)
        key_tues = types.InlineKeyboardButton(text='Вторник', callback_data='tuesday')
        keyboard.add(key_tues)
        key_wednes = types.InlineKeyboardButton(text='Среда', callback_data='wednesday')
        keyboard.add(key_wednes)
        key_thurs = types.InlineKeyboardButton(text='Четверг', callback_data='thursday')
        keyboard.add(key_thurs)
        key_fri = types.InlineKeyboardButton(text='Пятница', callback_data='friday')
        keyboard.add(key_fri)
        key_satur = types.InlineKeyboardButton(text='Суббота', callback_data='saturday')
        keyboard.add(key_satur)
        key_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
        keyboard.add(key_today)
        test = types.InlineKeyboardButton(text='Помощь', callback_data='help')
        keyboard.add(test)
        bot.send_message(message.from_user.id, text='Выбери день недели:', reply_markup=keyboard)
        #print("1111")
    elif message.text == "help": 
        bot.send_message(message.from_user.id, "Напиши Timetable или нажми на команду /start")
    else: 
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "timetable":
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_monday = types.InlineKeyboardButton(text='Понедельник', callback_data='monday')
        keyboard.add(key_monday)
        key_tues = types.InlineKeyboardButton(text='Вторник', callback_data='tuesday')
        keyboard.add(key_tues)
        key_wednes = types.InlineKeyboardButton(text='Среда', callback_data='wednesday')
        keyboard.add(key_wednes)
        key_thurs = types.InlineKeyboardButton(text='Четверг', callback_data='thursday')
        keyboard.add(key_thurs)
        key_fri = types.InlineKeyboardButton(text='Пятница', callback_data='friday')
        keyboard.add(key_fri)
        key_satur = types.InlineKeyboardButton(text='Суббота', callback_data='saturday')
        keyboard.add(key_satur)
        key_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
        keyboard.add(key_today)
        test = types.InlineKeyboardButton(text='Помощь', callback_data='help')
        keyboard.add(test)
        bot.send_message(call.from_user.id, text='Выбери день недели:', reply_markup=keyboard)
        
        #keyboard2 = telebot.types.InlineKeyboardMarkup()
        #key_8 = types.InlineKeyboardButton(text='1 пара: 8:50 - 10:25', callback_data='8')
        #keyboard2.add(key_8)
        #key_10 = types.InlineKeyboardButton(text='2 пара: 10:40 - 12:15', callback_data='10')
        #keyboard2.add(key_10)
        #key_13 = types.InlineKeyboardButton(text='3 пара: 13:00 - 14:35', callback_data='13')
        #keyboard2.add(key_13)
        #key_14 = types.InlineKeyboardButton(text='4 пара: 14:50 - 16:25', callback_data='14')
        #keyboard2.add(key_14)
        #key_17 = types.InlineKeyboardButton(text='5 пара: 17:10 - 18:45', callback_data='17')
        #keyboard2.add(key_17)
        #key_19 = types.InlineKeyboardButton(text='6 пара: 19:00 - 20:35', callback_data='19')
        #keyboard2.add(key_19)
        #key_allpar = types.InlineKeyboardButton(text='Весь день', callback_data='all_day')
        #keyboard2.add(key_allpar)
        #bot.send_message(call.from_user.id, text='Выбери время:', reply_markup=keyboard2)
    
    elif call.data == "monday":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['day_1']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para1 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)

            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['day_1']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)

            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['day_1']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['day_1']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)

            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['day_1']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para5 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['day_1']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        name_para = para6_day1.find('span', {'class':['discipline']})
        try:
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para6 + name_para6 + type_para6 + prepod6
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text) 
            bot.answer_callback_query(call.id, show_alert=True, text = str_text)
    
    elif call.data == "tuesday":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['day_2']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para1 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)

            
            
            
            
            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['day_2']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['day_2']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['day_2']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['day_2']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para5 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)

            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['day_2']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para6_day1.find('span', {'class':['discipline']})
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para6 + name_para6 + type_para6 + prepod6
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
    elif call.data == "wednesday":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['day_3']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            temp = time_para1 + 'Нет Пары'
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            
            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['day_3']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['day_3']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)

            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['day_3']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['day_3']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para5 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['day_3']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para6_day1.find('span', {'class':['discipline']})
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
   
    elif call.data == "thursday":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['day_4']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para1 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['day_4']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['day_4']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['day_4']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['day_4']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
           non_para = ['Нет Пары']
           temp = time_para5 + non_para
           str_text = '\n'.join(temp)
           print(str_text)
           bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['day_4']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para6_day1.find('span', {'class':['discipline']})
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para6 + name_para6 + type_para6 + prepod6
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
    
    elif call.data == "friday":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['day_5']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para1 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['day_5']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['day_5']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['day_5']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['day_5']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para5 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['day_5']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para6_day1.find('span', {'class':['discipline']})
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para6 + name_para6 + type_para6 + prepod6
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
    
    elif call.data == "saturday":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['day_6']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para1 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['day_6']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['day_6']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['day_6']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['day_6']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para5 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['day_6']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para6_day1.find('span', {'class':['discipline']})
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para6 + name_para6 + type_para6 + prepod6
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
    
    elif call.data == "today":
        para1 = tables.find('tr', {'class':['lesson_1']})
        para1_day1 = para1.find('td', {'class':['current_day']})
        time_para = para1.find('th',{'class':['time']})
        time_para1 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para1_day1.find('span', {'class':['discipline']})
            name_para1 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para1 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para1 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para1_day1.find('span', {'class':['kind']})
            type_para1 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para1_day1.find('span', {'class':['group']})
            prepod1 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para1 + name_para1 + type_para1 + prepod1
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            
            
        para2 = tables.find('tr', {'class':['lesson_2']})
        para2_day1 = para2.find('td', {'class':['current_day']})
        time_para = para2.find('th',{'class':['time']})
        time_para2 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para2_day1.find('span', {'class':['discipline']})
            name_para2 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para2 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para2 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para2_day1.find('span', {'class':['kind']})
            type_para2 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para2_day1.find('span', {'class':['group']})
            prepod2 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para2 + name_para2 + type_para2 + prepod2
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para3 = tables.find('tr', {'class':['lesson_3']})
        para3_day1 = para3.find('td', {'class':['current_day']})
        time_para = para3.find('th',{'class':['time']})
        time_para3 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para3_day1.find('span', {'class':['discipline']})
            name_para3 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para3 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:    
            name_para3 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para3_day1.find('span', {'class':['kind']})
            type_para3 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para3_day1.find('span', {'class':['group']})
            prepod3 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para3 + name_para3 + type_para3 + prepod3
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para4 = tables.find('tr', {'class':['lesson_4']})
        para4_day1 = para4.find('td', {'class':['current_day']})
        time_para = para4.find('th',{'class':['time']})
        time_para4 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para4_day1.find('span', {'class':['discipline']})
            name_para4 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para4 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para4 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para4_day1.find('span', {'class':['kind']})
            type_para4 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para4_day1.find('span', {'class':['group']})
            prepod4 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para4 + name_para4 + type_para4 + prepod4
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
            

        para5 = tables.find('tr', {'class':['lesson_5']})
        para5_day1 = para5.find('td', {'class':['current_day']})
        time_para = para5.find('th',{'class':['time']})
        time_para5 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para5_day1.find('span', {'class':['discipline']})
            name_para5 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para5 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para5 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para5_day1.find('span', {'class':['kind']})
            type_para5 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para5_day1.find('span', {'class':['group']})
            prepod5 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para5 + name_para5 + type_para5 + prepod5
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
            
            
            
             

        para6 = tables.find('tr', {'class':['lesson_6']})
        para6_day1 = para6.find('td', {'class':['current_day']})
        time_para = para6.find('th',{'class':['time']})
        time_para6 = re.findall(r'\d\d:\d\d', time_para.text)
        try:
            name_para = para6_day1.find('span', {'class':['discipline']})
            name_para6 = re.findall(r'[А-Я][а-я]*', name_para.text)
        except AttributeError:
            non_para = ['Нет Пары']
            temp = time_para6 + non_para
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
        else:
            name_para6 = re.findall(r'(\w[\s\S]*)', name_para.text)
            type_para = para6_day1.find('span', {'class':['kind']})
            type_para6 = re.findall(r'[А-Я][а-я]*', type_para.text)
            prepod = para6_day1.find('span', {'class':['group']})
            prepod6 = re.findall(r'(\w[\s\S]\w+[\s\S]+\w[\s\S])', prepod.text)
            temp = time_para6 + name_para6 + type_para6 + prepod6
            str_text = '\n'.join(temp)
            print(str_text)
            bot.send_message(call.from_user.id, str_text)
    
    elif call.data == "help":
        bot.answer_callback_query(call.id, show_alert=True, text ='У тебя есть два выбора: \n 1)Пользоваться ботом \n 2)Нахуй выйти от сюда')
        
bot.polling(none_stop=True, interval=0)


#@bot.message_handler(commands=['start'])
#def start_message(message):
#    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
#
#@bot.message_handler(content_types=['text'])
#def send_text(message):
#    if message.text.lower() == 'привет':
#        bot.send_message(message.chat.id, 'Привет, мой создатель')
#    elif message.text.lower() == 'пока':
#        bot.send_message(message.chat.id, 'Прощай, создатель')
#    elif message.text.lower() == 'я тебя люблю':
#        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
#
#@bot.message_handler(content_types=['sticker'])
#def sticker_id(message):
#    print(message)
#
#bot.polling()