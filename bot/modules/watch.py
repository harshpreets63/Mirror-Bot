import threading

from telegram import Bot
from telegram.ext import CommandHandler

from bot import DOWNLOAD_DIR, DOWNLOAD_STATUS_UPDATE_INTERVAL, Interval, dispatcher
from bot.helper.ext_utils.bot_utils import setInterval
from bot.helper.mirror_utils.download_utils.youtube_dl_download_helper import (
    YoutubeDLHelper,
)
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import (
    sendMessage,
    sendStatusMessage,
    update_all_messages,
)

from .mirror import MirrorListener


def _watch(bot: Bot, update,isTar=False, isZip=False, isLeech=False):
    mssg = update.message.text
    message_args = mssg.split(" ")
    name_args = mssg.split("|")
    try:
        link = message_args[1]
    except IndexError:
        msg = f"/{BotCommands.WatchCommand} [yt_dl supported link] [quality] |[CustomName] to mirror with youtube_dl.\n\n"
        msg += "<b>Note :- Quality and custom name are optional</b>\n\nExample of quality :- audio, 144, 240, 360, 480, 720, 1080, 2160."
        msg += "\n\nIf you want to use custom filename, plz enter it after |"
        msg += f"\n\nExample :-\n<code>/{BotCommands.WatchCommand} https://youtu.be/ocX2FN1nguA 720 |My video bro</code>\n\n"
        msg += "This file will be downloaded in 720p quality and it's name will be <b>My video bro</b>"
        sendMessage(msg, bot, update)
        return
    try:
        if "|" in mssg:
            mssg = mssg.split("|")
            qual = mssg[0].split(" ")[2]
            if qual == "":
                raise IndexError
        else:
            qual = message_args[2]
        if qual != "audio":
            qual = f"bestvideo[height<={qual}]+bestaudio/best[height<={qual}]"
    except IndexError:
        qual = "bestvideo+bestaudio/best"
    try:
        name = name_args[1]
    except IndexError:
        name = ""
    reply_to = update.message.reply_to_message
    tag = reply_to.from_user.username if reply_to is not None else None
    pswd = ""
    listener = MirrorListener(bot, update, pswd,isTar, isZip, tag, isLeech=isLeech)
    ydl = YoutubeDLHelper(listener)
    threading.Thread(
        target=ydl.add_download,
        args=(link, f"{DOWNLOAD_DIR}{listener.uid}", qual, name),
    ).start()
    sendStatusMessage(update, bot)
    if len(Interval) == 0:
        Interval.append(
            setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages)
        )


def watchZip(update, context):
    _watch(context.bot, update, True, True)

def watchTar(update, context):
    _watch(context.bot, update, True)   

def watch(update, context):
    _watch(context.bot, update)

def leechWatch(update, context):
    _watch(context.bot, update, isLeech=True)

def leechWatchTar(update, context):
    _watch(context.bot, update, True, isLeech=True)

def leechWatchZip(update, context):
    _watch(context.bot, update, True, True, isLeech=True)

zip_watch_handler = CommandHandler(BotCommands.ZipWatchCommand, watchZip,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
tar_watch_handler = CommandHandler(BotCommands.ZipWatchCommand, watchTar,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)                                    
leech_watch_handler = CommandHandler(BotCommands.LeechWatchCommand, leechWatch,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
leech_tar_watch_handler = CommandHandler(BotCommands.LeechTarWatchCommand, leechWatchTar,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
leech_zip_watch_handler = CommandHandler(BotCommands.LeechZipWatchCommand, leechWatchZip,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

mirror_handler = CommandHandler(
    BotCommands.WatchCommand,
    watch,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True,
)
zip_mirror_handler = CommandHandler(
    BotCommands.ZipWatchCommand,
    watchZip,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True,
)
tar_mirror_handler = CommandHandler(
    BotCommands.TarWatchCommand,
    watchTar,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(mirror_handler)
dispatcher.add_handler(zip_mirror_handler)
dispatcher.add_handler(tar_mirror_handler)
dispatcher.add_handler(leech_watch_handler)
dispatcher.add_handler(leech_tar_watch_handler)
dispatcher.add_handler(leech_zip_watch_handler)