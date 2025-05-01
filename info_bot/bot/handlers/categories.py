from bot import bot
from bot.models import Category, SubCategory
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telebot.types import Message
import os

MENU_BUTTON = InlineKeyboardMarkup()
menu_btn = InlineKeyboardButton(text='В меню ↩️️', callback_data='menu')
MENU_BUTTON.add(menu_btn)


def category_view_callback(callback: CallbackQuery) -> None:
    try:
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        category_view(callback.message)
    except:
        category_view(callback.message)


def category_view(message: Message):
    try:
        categories = Category.objects.all()
        keyboard = InlineKeyboardMarkup()
        for category in categories:
            keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.pk}"))

        bot.send_message(
            text="Здравствуйте, что бы вы хотели узнать?",
            chat_id=message.chat.id,
            reply_markup=keyboard,
        )
    except Exception as e:
        bot.send_message(text=f'error: {e}', chat_id=message.chat.id)


def subcategory_view(call: CallbackQuery):
    _, cat_id = call.data.split("_")
    category = Category.objects.get(pk=cat_id)
    subcategories = SubCategory.objects.filter(category=category, parent__isnull=True).order_by('order')
    keyboard = InlineKeyboardMarkup()
    for subcategory in subcategories:
        has_children = SubCategory.objects.filter(parent=subcategory).exists()

        callback_data = f"subcategory_{subcategory.pk}" if has_children else f"subsubcategory_{subcategory.pk}"
        
        keyboard.add(
            InlineKeyboardButton(
                text=subcategory.name,
                callback_data=callback_data
            )
        )
    # Добавляем кнопку "Назад" для возврата к списку категорий
    back_btn = InlineKeyboardButton(text='<< Назад', callback_data='back_to_categories')
    keyboard.add(back_btn)
    keyboard.add(menu_btn)
    
    bot.edit_message_text(
        text="Выберите подкатегорию",
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard
    )


def subsubcategory_view(call: CallbackQuery):
    _, subcat_id = call.data.split("_")
    subcategory = SubCategory.objects.get(pk=subcat_id)
    subsubcategories = SubCategory.objects.filter(parent=subcategory).order_by('order')
    keyboard = InlineKeyboardMarkup()
    
    for subsubcategory in subsubcategories:
        has_children = SubCategory.objects.filter(parent=subsubcategory).exists()
        
        # Если есть дочерние элементы, используем другой callback_data
        callback_data = f"subsubcategory_{subsubcategory.pk}" if not has_children else f"subsubsubcategory_{subsubcategory.pk}"
        
        keyboard.add(
            InlineKeyboardButton(
                text=subsubcategory.name,
                callback_data=callback_data
            )
        )
    
    back_btn = InlineKeyboardButton(text='<< Назад', callback_data=f'category_{subcategory.category.pk}')
    keyboard.add(back_btn)
    keyboard.add(menu_btn)
    
    bot.edit_message_text(
        text="Выберите подподкатегорию",
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard
    )


def show_info(call: CallbackQuery):
    chat_id = call.message.chat.id

    msg = bot.edit_message_text(
        text='Ожидайте... 😊',
        message_id=call.message.message_id,
        chat_id=chat_id,
    )

    _, subcategory_id = call.data.split("_")
    subcategory = SubCategory.objects.get(pk=subcategory_id)
    
    has_children = SubCategory.objects.filter(parent=subcategory).exists()
    
    if has_children:
        subsubcategory_view(call)
        return

    if subcategory.image and subcategory.text:
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=subcategory.image,
            caption=subcategory.text[:1000],
            parse_mode='Markdown',
            reply_markup=MENU_BUTTON,
        )
        if len(subcategory.text) > 1000:
            bot.send_message(
                chat_id=chat_id,
                text=subcategory.text[1000:],
                reply_markup=MENU_BUTTON,
            )

    elif subcategory.text:
        bot.edit_message_text(
            text=subcategory.text,
            chat_id=call.message.chat.id,
            message_id=msg.message_id,
            parse_mode='Markdown',
            reply_markup=MENU_BUTTON,
        )

    if subcategory.file:
        file_extension = os.path.splitext(subcategory.file.path)[1][1:]
        bot.send_document(
            chat_id=call.message.chat.id,
            document=subcategory.file,
            caption=f'  Вот документ для изучения {subcategory.name}',
            visible_file_name=f'{subcategory.name}.{file_extension}',
            reply_markup=MENU_BUTTON,
        )
        bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

    elif subcategory.image:
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=subcategory.image,
            reply_markup=MENU_BUTTON,
        )
        bot.delete_message(chat_id=chat_id, message_id=msg.message_id)


def back_to_subcategory(call: CallbackQuery):
    try:
        subcategory_view(call)
    except Exception as e:
        bot.send_message(text=f'error: {e}', chat_id=call.message.chat.id)


def back_to_categories(call: CallbackQuery):
    try:
        category_view_callback(call)
    except Exception as e:
        bot.send_message(text=f'error: {e}', chat_id=call.message.chat.id)