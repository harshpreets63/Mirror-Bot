from speedtest import Speedtest
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher, AUTHORIZED_CHATS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, Filters, CommandHandler


def speedtest(update, context):
    message = update.effective_message
    ed_msg = message.reply_text("Running Speed Test . . . 📈📊")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f'''
<b>🖥️ Server / Stats of The Machine 🖥️</b>
<b>💳 Name:</b> <code>{result['server']['name']}</code>
<b>⛳️ Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
    
<b>✈️ SpeedTest Results 💨</b>
<b>🔺 Upload:</b> <code>{speed_convert(result['upload'] / 8)}</code>
<b>🔻 Download:</b>  <code>{speed_convert(result['download'] / 8)}</code>
<b>📶 Ping:</b> <code>{result['ping']} ms</code>
<b>🏬 ISP:</b> <code>{result['client']['isp']}</code>
'''
    ed_msg.delete()
    try:
        update.effective_message.reply_photo(path, string_speed, parse_mode=ParseMode.HTML)
    except:
        update.effective_message.reply_text(string_speed, parse_mode=ParseMode.HTML)

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


SPEED_HANDLER = CommandHandler(BotCommands.SpeedCommand, speedtest, 
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(SPEED_HANDLER)