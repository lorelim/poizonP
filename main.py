import asyncio
import logging
import sys
from os import getenv
from assets.config import TOKEN_
from assets import config
from aiogram import Bot, Dispatcher, html

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import types
from assets import keyboards
from aiogram import F
from aiogram.enums import ContentType
from aiogram.methods.send_photo import SendPhoto
from assets import funcs
from aiogram.types import InputFile, BufferedInputFile
from aiogram.methods import SendVideo
from assets.sqlite import SQLighter
from assets.parser_byn.parser_byn import usd_byn
from assets.parser_rub.parser_rub import usd_rub
TOKEN = TOKEN_

dp = Dispatcher()

bot = Bot(token=TOKEN)

SQL = SQLighter("assets/database/db.db")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    
    with open(config.main_photo, "rb") as photo_file:
        photo_bytes = photo_file.read()


    photo = BufferedInputFile(photo_bytes, config.main_photo)

    # if config.previous_id != 0:
    msg = await bot(SendPhoto(
            chat_id = message.from_user.id, 
            photo = photo, 
            caption = config.start_message, 
            reply_markup = keyboards.kb_main)

        )

    if SQL.check_user(message.from_user.id) == True:
        
        pr_message = SQL.get_pr_msg(message.from_user.id)
        SQL.change_state(message.from_user.id, 0)

        # if user was existed then delete pr message and unpdate it

        if pr_message != 0:
            await bot.delete_message(message.from_user.id, pr_message)

        await bot.delete_message(message.from_user.id, message.message_id) # delete user's msg (/start)
        SQL.change_msg(message.from_user.id, msg.message_id) # set state 

    else:     

        SQL.add_new_user(message.from_user.id, msg.message_id)
        SQL.change_state(message.from_user.id, 0) # set state 


async def main() -> None:
    
    await dp.start_polling(bot)

@dp.message(F.text)
async def count_price_order(message: types.Message): 

     # if user count the price of order
    if SQL.get_state(message.from_user.id) == 2:
           
        # count price in usdt   
        price_usdt = funcs.get_price(int(message.text), SQL.get_cl_type(message.from_user.id))

        if SQL.get_pr_msg(message.from_user.id) != 0:
            pr_message = SQL.get_pr_msg(message.from_user.id)
            await bot.delete_message(message.from_user.id, pr_message)

        msg = await bot.send_message(message.from_user.id, text = "Итоговая цена в USDT: " + str(format(price_usdt, ".0f")) + "\n" + "Итоговая цена в BYN: " + str(format((usd_byn() * price_usdt) + 0.05 * (usd_byn() * price_usdt), ".0f")) + "\n" + "Итоговая цена в RUB: " + str(format((usd_rub() * price_usdt) + 0.05 * (usd_rub() * price_usdt), ".0f")), reply_markup = keyboards.kb_order_product)

        SQL.change_msg(message.from_user.id, 0)
        
        SQL.change_state(message.from_user.id, 0)

        SQL.change_cl_type(message.from_user.id, 0)

@dp.message(F.photo)
async def get_order(message:types.Message):


    if SQL.get_state(message.from_user.id) == 1:

        print(message.chat.username)

        photo_id = str(message.photo[0]).split(" ", maxsplit = 1)[0].split("'", maxsplit = 2)[1] # get (file_id) of photo to send it to group
        photo_caption = message.caption # get caption of photo
        
        await bot(SendPhoto(chat_id = config.ORDERS_id, photo = photo_id, caption = photo_caption)) # send this photo in admin's group

        # conifrm the order 
        SQL.change_state(message.from_user.id, 0)

        await bot.send_message(message.from_user.id, text = config.order_succesful_message, reply_markup = keyboards.kb_succesful_order) # offer user to back in menu or use calculator
    
        
# handnler for main kb
@dp.callback_query(lambda c: c.data.startswith("main"))
async def handle_main_kb(callback_query: types.CallbackQuery):

    
    if SQL.get_state(callback_query.from_user.id) == 0:

        if callback_query.data.endswith("1"):

            
            if SQL.get_pr_msg(callback_query.from_user.id) != 0:

                pr_message = SQL.get_pr_msg(callback_query.from_user.id)

                await bot.delete_message(callback_query.from_user.id, pr_message)
            

            await callback_query.answer("Оформить заказ")
            
            with open(config.main_photo, "rb") as photo_file:
                photo_bytes = photo_file.read()

            photo = BufferedInputFile(photo_bytes, config.main_photo)

            msg = await bot(SendPhoto(

                    chat_id = callback_query.from_user.id,
                    photo = photo,
                    caption = config.order_message,
                    reply_markup = keyboards.kb_order,
                ))

            SQL.change_msg(callback_query.from_user.id, msg.message_id)

        if callback_query.data.endswith("2"):

            if SQL.get_pr_msg(callback_query.from_user.id) != 0:

                pr_message = SQL.get_pr_msg(callback_query.from_user.id)
    
                await bot.delete_message(callback_query.from_user.id, pr_message) # delete previous

            msg = await bot.send_message(chat_id = callback_query.from_user.id, text = config.calculator_message, reply_markup = keyboards.kb_calc)


            SQL.change_msg(callback_query.from_user.id, msg.message_id)

        if callback_query.data.endswith("3"):
            await callback_query.answer("Отзывы")   
        if callback_query.data.endswith("4"):
            await callback_query.answer("Поддержка")

#handler for orders 
@dp.callback_query(lambda c:c.data.startswith("order"))
async def handle_order_kb(callback_query: types.CallbackQuery):

    if SQL.get_state(callback_query.from_user.id) == 0:

        if callback_query.data.endswith("1") and SQL.get_state(callback_query.from_user.id) == 0:

            #send guide to user 
            with open(config.guide_video, "rb") as video_file:
                video_bytes = video_file.read()

            video = BufferedInputFile(video_bytes, config.guide_video)

            if SQL.get_pr_msg(callback_query.from_user.id) != 0:
                pr_message = SQL.get_pr_msg(callback_query.from_user.id)

                await bot.delete_message(callback_query.from_user.id, pr_message)

            await bot(SendVideo(

                    chat_id = callback_query.from_user.id,
                    video = video,
                    caption = config.guide_message
                ))

            #send photo to user
            with open(config.main_photo, "rb") as photo_file:
                photo_bytes = photo_file.read()

            photo = BufferedInputFile(photo_bytes, config.main_photo)

            msg = await bot(SendPhoto(

                    chat_id = callback_query.from_user.id,
                    photo = photo,
                    caption = config.order_message,
                    reply_markup = keyboards.kb_order,
                ))

            SQL.change_msg(callback_query.from_user.id, msg.message_id)

            await callback_query.answer()

        if callback_query.data.endswith("2") and SQL.get_state(callback_query.from_user.id) == 0:
        
            
            SQL.change_state(callback_query.from_user.id, 1) 

            # send instruction for evety types of clothes
            with open(config.order_photo, "rb") as photo_file:
                photo_bytes = photo_file.read()

            photo = BufferedInputFile(photo_bytes, config.order_photo)

            if SQL.get_pr_msg(callback_query.from_user.id) != 0:
                pr_message = SQL.get_pr_msg(callback_query.from_user.id)

                await bot.delete_message(callback_query.from_user.id, pr_message)

            msg = await bot(SendPhoto(
                chat_id = callback_query.from_user.id,
                photo = photo,
                caption = config.order_product_message,
                reply_markup = keyboards.kb_order_product
                ))

            SQL.change_msg(callback_query.from_user.id, msg.message_id)

            await callback_query.answer()

@dp.callback_query(lambda c: c.data.startswith("calc"))
async def count_price(callback_query: types.CallbackQuery):
    
    
    if SQL.get_state(callback_query.from_user.id) != 1:

        if SQL.get_pr_msg(callback_query.from_user.id) != 0:
            pr_message = SQL.get_pr_msg(callback_query.from_user.id)
            await bot.delete_message(callback_query.from_user.id, pr_message)

        if (callback_query.data.endswith("1")):
            # config.fee = config.fee_usdt + config.fee_usdt_1

            SQL.change_cl_type(callback_query.from_user.id, 1)
            
            SQL.change_state(callback_query.from_user.id, 2)
            await callback_query.answer()

        if (callback_query.data.endswith("2")):
            # config.fee = config.fee_usdt + config.fee_usdt_2

            SQL.change_cl_type(callback_query.from_user.id, 2)
            
            SQL.change_state(callback_query.from_user.id, 2)
            await callback_query.answer()

        if (callback_query.data.endswith("3")):
            # config.fee = config.fee_usdt + config.fee_usdt_3

            SQL.change_cl_type(callback_query.from_user.id, 3)
            
            SQL.change_state(callback_query.from_user.id, 2)
            await callback_query.answer()

        if (callback_query.data.endswith("4")):
            # config.fee = config.fee_usdt + config.fee_usdt_4

            SQL.change_cl_type(callback_query.from_user.id, 4)
            
            SQL.change_state(callback_query.from_user.id, 2)
            await callback_query.answer()

        if (callback_query.data.endswith("5")):
            # config.fee = config.fee_usdt + config.fee_usdt_5

            SQL.change_cl_type(callback_query.from_user.id, 5)

            SQL.change_state(callback_query.from_user.id, 2)
            await callback_query.answer()

        msg = await bot.send_message(callback_query.from_user.id, text = config.order_succesful_message, reply_markup = keyboards.kb_order_product)
        SQL.change_msg(callback_query.from_user.id, msg.message_id)

#handler for canceling order and back to menu
@dp.callback_query(lambda c: c.data == "menu")
async def back_to_menu(callback_query: types.CallbackQuery):

    SQL.change_state(callback_query.from_user.id, 0)
    with open(config.main_photo, "rb") as photo_file:
        photo_bytes = photo_file.read()

    photo = BufferedInputFile(photo_bytes, config.main_photo)

    if SQL.get_pr_msg(callback_query.from_user.id) != 0:

        pr_message = SQL.get_pr_msg(callback_query.from_user.id)

        await bot.delete_message(callback_query.from_user.id, pr_message)

    msg = await bot(SendPhoto(
            
        chat_id = callback_query.from_user.id,
        photo = photo,
        caption = config.start_message,
        reply_markup = keyboards.kb_main,
    
    ))

    SQL.change_msg(callback_query.from_user.id, msg.message_id)

    await callback_query.answer()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())