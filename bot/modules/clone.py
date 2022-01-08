from telegram.ext import CommandHandler
from telegram import ParseMode
from bot.helper.mirror_utils.upload_utils import gdriveTools
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.status_utils.clone_status import CloneStatus
from bot import dispatcher, LOGGER, STOP_DUPLICATE_CLONE, download_dict, download_dict_lock, Interval, DOWNLOAD_STATUS_UPDATE_INTERVAL, CLONE_LIMIT, LOGS_CHATS
from bot.helper.ext_utils.bot_utils import setInterval, check_limit
from bot.helper.ext_utils.bot_utils import get_readable_file_size, is_gdrive_link, is_gdtot_link, new_thread
from bot.helper.mirror_utils.download_utils.direct_link_generator import gdtot
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
import random
import string

@new_thread
def cloneNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
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
        msg = sendMessage(f"Checking Drive Link...", context.bot, update)
        gd = gdriveTools.GoogleDriveHelper()
        res, size, name, files = gd.clonehelper(link)
        deleteMessage(context.bot, msg)
        if res != "":
            sendMessage(res, context.bot, update)
            return
        if STOP_DUPLICATE_CLONE:
            LOGGER.info('Checking File/Folder if already in Drive...')
            smsg, button = gd.drive_list(name)
            if smsg:
                msg3 = "File/Folder is already available in Drive.\nHere are the search results:"
                sendMarkup(msg3, context.bot, update, button)
                return
        if CLONE_LIMIT is not None:
            result = check_limit(size, CLONE_LIMIT)
            if result:
                msg2 = f'Failed, Clone limit is {CLONE_LIMIT}.\nYour File/Folder size is {get_readable_file_size(size)}.'
                sendMessage(msg2, context.bot, update)
                return        
        if files < 15:
            msg = sendMessage(f"Cloning: <code>{link}</code>", context.bot, update)
            result, button = gd.clone(link)
            deleteMessage(context.bot, msg)
        else:
            drive = gdriveTools.GoogleDriveHelper(name)
            gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=12))
            clone_status = CloneStatus(drive, size, update, gid)
            with download_dict_lock:
                download_dict[update.message.message_id] = clone_status
            if len(Interval) == 0:
                Interval.append(setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages))
            sendStatusMessage(update, context.bot)
            result, button = drive.clone(link)
            with download_dict_lock:
                del download_dict[update.message.message_id]
                count = len(download_dict)
            try:
                if count == 0:
                    Interval[0].cancel()
                    del Interval[0]
                    delete_all_messages()
                else:
                    update_all_messages()
            except IndexError:
                pass
        if update.message.from_user.username:
            uname = f'@{update.message.from_user.username}'
        else:
            uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
        if uname is not None:
            cc = f'\n\ncc: {uname}'
            men = f'{uname} '
        if button in ["cancelled", ""]:
            sendMessage(men + result, context.bot, update)
        else:
            sendMarkup(result + cc, context.bot, update, button)
            if LOGS_CHATS:
                try:
                    for i in LOGS_CHATS:
                        msg1 = f'<b>File Cloned: </b> <code>{name}</code>\n'
                        msg1 += f'<b>Size: </b>{get_readable_file_size(size)}\n'
                        msg1 += f'<b>By: </b>{uname}\n'
                        bot.sendMessage(chat_id=i, text=msg1, reply_markup=button, parse_mode=ParseMode.HTML)
                except Exception as e:
                    LOGGER.warning(e)
        if gdtot_link:
            gd.deletefile(link)                                                     
    else:
        sendMessage('Provide G-Drive Or Gdtot Shareable Link to Clone.', context.bot, update)
        
clone_handler = CommandHandler(BotCommands.CloneCommand, cloneNode, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(clone_handler)