import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


TELEGRAM_TOKEN = "8535210582:AAFfmovTE2QsB2lG5DcSd4RBgCe7vJgiwHM"

# Build the bot application once
application = (
    Application.builder()
    .token(TELEGRAM_TOKEN)
    .build()
)


# Handlers
async def start(update: Update, context):
    await update.message.reply_text("Hello from Django!")


async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)


application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


@csrf_exempt
def current_datetime(request):
    if request.method == "POST":
        data = json.loads(request.body)

        update = Update.de_json(data, application.bot)

        application.create_task(application.process_update(update))

    return JsonResponse({"ok": True})