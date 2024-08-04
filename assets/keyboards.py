import aiogram
from aiogram import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

#create buttons for main keyboard
button1_main = InlineKeyboardButton(text = "Оформить заказ", callback_data = "main1")
button2_main = InlineKeyboardButton(text = "Калькулятор стоимости", callback_data = "main2")
button3_main = InlineKeyboardButton(text = "Отзывы о нашей работе", callback_data = "main3", url = "https://t.me/poshoozim_feedback")
button4_main = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main4", url = "https://t.me/POSHOOZIM_MANAGER")

#create main keyboard
kb_main = InlineKeyboardMarkup( inline_keyboard = [[button2_main], [button3_main], [button4_main]])

#create buttons for order keyboard
button1_order = InlineKeyboardButton(text = "Как оформить заказ", callback_data = "order1")
button2_order = InlineKeyboardButton(text = "Оформить заказ", callback_data = "order2")
button3_order = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main4", url = "https://t.me/Ehehehdjjd")
button4_order = InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu")

#create a keybord for order 
kb_order = InlineKeyboardMarkup(inline_keyboard = [[button1_order], [button2_order], [button3_order], [button4_order]])

#crete a order product button for canceling order and back to menu
button1_order_product = InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu")
button2_order_product = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main4", url = "https://t.me/Ehehehdjjd")
kb_order_product = InlineKeyboardMarkup(inline_keyboard = [[button2_order_product], [button1_order_product]])

#create the button after succesful order 
button1_order_success = InlineKeyboardButton(text = "Калькулятор стоимости", callback_data = "main2")
button2_order_success = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main4", url = "https://t.me/Ehehehdjjd")
button3_order_success = InlineKeyboardButton(text = "Вернутся в меню" ,callback_data = "menu")

#create keyboard after succesful order
kb_succesful_order = InlineKeyboardMarkup(inline_keyboard = [[button1_order_success], [button2_order_success], [button3_order_success]])

#create keyboard for calculator
button1_calc = InlineKeyboardButton(text = "Кросовки/Ботинки", callback_data = "calc1")
button2_calc = InlineKeyboardButton(text = "Кофты/Штаны/Брюки/Джинсы", callback_data = "calc2")
button3_calc = InlineKeyboardButton(text = "Майки/Рубашки/Шорты", callback_data = "calc3")
button4_calc = InlineKeyboardButton(text = "Куртки", callback_data = "calc4")
button5_calc = InlineKeyboardButton(text = "Аксессуары/Парфюм", callback_data = "calc5")
button6_calc = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main4", url = "https://t.me/Ehehehdjjd")
button7_calc = InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu")

#create a keybord for order 
kb_calc = InlineKeyboardMarkup(inline_keyboard = [[button1_calc], [button2_calc], [button3_calc], [button4_calc], [button5_calc],[button6_calc], [button7_calc]])
