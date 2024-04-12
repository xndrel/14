import telebot
from telebot import types
import os

bot = telebot.TeleBot('7095549792:AAFqExmSpSVjBUmjZOLswciPuE7YZbwpG-U')

user_states = {}

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    welcome_photo_path = os.path.join('photo', 'WELCOMEE.jpg') 
    try:
        photo = open(welcome_photo_path, 'rb')

        keyboard = types.InlineKeyboardMarkup()
        menu_button = types.InlineKeyboardButton("Перейти в меню", callback_data='menu')
        support_button = types.InlineKeyboardButton("Поддержка", callback_data='support')
        keyboard.add(menu_button, support_button)

        msg = bot.send_photo(message.chat.id, photo, caption="Привет, {0.first_name}!\n\nЯ бот созданный помочь тебя научить турнирным фишкам Dead by Daylight.".format(message.from_user),reply_markup=keyboard)

        user_states[message.chat.id] = {'message_id': msg.message_id, 'state': 'welcome'}

        photo.close()
    except FileNotFoundError as e:
        send_notification(message.chat.id, "Ошибка вывода главного экрана\n\nСообщите в поддержку о данной проблемы.")
    except Exception as e:
        print(f"Ошибка при отправке приветственного фото: {e}")
        
def send_notification(chat_id, text):
    bot.send_message(chat_id, text)
    bot.answer_callback_query(chat_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id

    if call.data == 'menu':
        try:
            menu_keyboard = types.InlineKeyboardMarkup()
            chips_button = types.InlineKeyboardButton("Фишки", callback_data='chips')
            back_button = types.InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')
            menu_keyboard.add(chips_button, back_button)
            
            current_state = user_states.get(chat_id, {}).get('state')
            if current_state == 'welcome':
                menu_photo_path = os.path.join('photo', 'MENU.jpg')
                photo = open(menu_photo_path, 'rb')
                bot.edit_message_media(media=types.InputMediaPhoto(photo), chat_id=chat_id, message_id=user_states[chat_id]['message_id'])
                bot.edit_message_caption(chat_id=chat_id, message_id=user_states[chat_id]['message_id'], caption="Это наше меню.", reply_markup=menu_keyboard)
                
                user_states[chat_id]['state'] = 'menu'
                photo.close()
            
        except FileNotFoundError as e:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Извините, произошла ошибка '02'\n\nСообщите в поддержку о данной проблемы.")
        except Exception as e:
            print(f"Ошибка при отправке фото для меню: {e}")
        

    elif call.data == 'support':
        try:
            support_keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')
            support_keyboard.add(back_button)
            
            current_state = user_states.get(chat_id, {}).get('state')
            if current_state == 'welcome':
                support_photo_path = os.path.join('photo', 'SUPPORT.jpg')
                photo = open(support_photo_path, 'rb')
                bot.edit_message_media(media=types.InputMediaPhoto(photo), chat_id=chat_id, message_id=user_states[chat_id]['message_id'])
                bot.edit_message_caption(chat_id=chat_id, message_id=user_states[chat_id]['message_id'], caption="Это наша поддержка.", reply_markup=support_keyboard)
                
                user_states[chat_id]['state'] = 'support'
                photo.close()

        except FileNotFoundError as e:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Извините, произошла ошибка '03'\n\nСообщите в поддержку о данной проблемы.")
        except Exception as e:
            print(f"Ошибка при отправке фото для поддержки: {e}")

    elif call.data == 'chips':
        bot.send_message(chat_id, "Выберите раздел:")

    elif call.data == 'back_to_main':
        try:
            current_state = user_states.get(chat_id, {}).get('state')

            if current_state == 'menu' or current_state == 'support':
                welcome_photo_path = os.path.join('photo', 'WELCOMEE.jpg')
                keyboard = types.InlineKeyboardMarkup()
                menu_button = types.InlineKeyboardButton("Перейти в меню", callback_data='menu')
                support_button = types.InlineKeyboardButton("Поддержка", callback_data='support')
                keyboard.add(menu_button, support_button)
                
                photo = open(welcome_photo_path, 'rb')

                bot.edit_message_media(media=types.InputMediaPhoto(photo), chat_id=chat_id, message_id=user_states[chat_id]['message_id'])
                bot.edit_message_caption(chat_id=chat_id, message_id=user_states[chat_id]['message_id'], 
                                          caption="Привет, {0.first_name}!\n\nЯ бот, созданный помочь тебе научить турнирным фишкам Dead by Daylight.".format(call.message.from_user), 
                                          reply_markup=keyboard)
                
                user_states[chat_id]['state'] = 'welcome'
                photo.close()
      
        except FileNotFoundError as e:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ошибка вывода главного экрана '04'\n\nСообщите в поддержку о данной проблемы.")
        except Exception as e:
            print(f"Ошибка при редактировании на главный экран: {e}")

bot.polling(none_stop=True)


