from traceback import format_exc

from asgiref.sync import sync_to_async
from bot.handlers import *
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from telebot.apihelper import ApiTelegramException
from telebot.types import Update

from bot import bot, logger


@require_GET
def set_webhook(request: HttpRequest) -> JsonResponse:
    """Setting webhook."""
    bot.set_webhook(url=f"{settings.HOOK}/bot/{settings.BOT_TOKEN}")
    bot.send_message(settings.OWNER_ID, "webhook set")
    return JsonResponse({"message": "OK"}, status=200)


@require_GET
def status(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "OK"}, status=200)


@csrf_exempt
@require_POST
@sync_to_async
def index(request: HttpRequest) -> JsonResponse:
    if request.META.get("CONTENT_TYPE") != "application/json":
        return JsonResponse({"message": "Bad Request"}, status=403)

    json_string = request.body.decode("utf-8")
    update = Update.de_json(json_string)
    try:
        bot.process_new_updates([update])
    except ApiTelegramException as e:
        logger.error(f"Telegram exception. {e} {format_exc()}")
    except ConnectionError as e:
        logger.error(f"Connection error. {e} {format_exc()}")
    except Exception as e:
        bot.send_message(settings.OWNER_ID, f'Error from index: {e}')
        logger.error(f"Unhandled exception. {e} {format_exc()}")
    return JsonResponse({"message": "OK"}, status=200)


"""Common"""

category_view = bot.message_handler(commands=["start"])(category_view)
subcategory_view = bot.callback_query_handler(lambda c: c.data.startswith('category_'))(subcategory_view)
subsubcategory_view = bot.callback_query_handler(lambda c: c.data.startswith('subcategory_'))(subsubcategory_view)
show_info = bot.callback_query_handler(lambda c: c.data.startswith('subsubcategory_'))(show_info)
category_view_callback = bot.callback_query_handler(lambda c: c.data == 'menu')(category_view_callback)
subsubsubcategory_view = bot.callback_query_handler(lambda c: c.data.startswith('subsubsubcategory_'))(subsubcategory_view)
# Добавляем обработчик для кнопки "Назад" к категориям
back_to_categories_handler = bot.callback_query_handler(lambda c: c.data == 'back_to_categories')(back_to_categories)
