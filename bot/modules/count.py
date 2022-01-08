from telegram.ext import CommandHandler, run_async
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import deleteMessage, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import get_readable_file_size, is_gdrive_link, is_gdtot_link, new_thread
from bot.helper.mirror_utils.download_utils.direct_link_generator import gdtot
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
from bot import dispatcher

@new_thread
def countNode(update,context):
    args = update.message.text.split(" ",maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(args) > 1:
        link = args[1]
    elif reply_to is not None:
        link = reply_to.text
    else:
        link = ''
    gdtot_link = is_gdtot_link(link)
    if gdtot_link:
        try:
            msg = sendMessage(f"Bypassing GDTOT Link.", context.bot, update)
            link = gdtot(link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update)
    if is_gdrive_link(link):
        msg = sendMessage(f"Counting: <code>{link}</code>",context.bot,update)
        gd = GoogleDriveHelper()
        result = gd.count(link)
        deleteMessage(context.bot,msg)
        sendMessage(result,context.bot,update)
        if gdtot_link:
            gd.deletefile(link)
    else:
        sendMessage("Provide G-Drive Or Gdtot Shareable Link to Count.",context.bot,update)

count_handler = CommandHandler(BotCommands.CountCommand,countNode,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(count_handler)
