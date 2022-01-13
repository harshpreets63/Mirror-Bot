import os
import shutil
import signal
import time
from sys import executable

import psutil
from pyrogram import idle
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from bot import IGNORE_PENDING_REQUESTS, app, bot, botStartTime, dispatcher, updater
from bot.helper.ext_utils import fs_utils
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper import button_build
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import (
    LOGGER,
    editMessage,
    sendLogFile,
    sendMessage,
    sendMarkup,
)
from bot.modules import (  # noqa
    authorize,
    cancel_mirror,
    clone,
    delete,
    list,
    mirror,
    mirror_status,
    watch,
    leech_settings,
    speedtest,
    count,
)


def stats(update, context):
    currentTime = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = (
        f"<b>Bot Uptime:</b> {currentTime}\n"
        f"<b>Total disk space:</b> {total}\n"
        f"<b>Used:</b> {used}  "
        f"<b>Free:</b> {free}\n\n"
        f"Data Usage\n<b>Upload:</b> {sent}\n"
        f"<b>Down:</b> {recv}\n\n"
        f"<b>CPU:</b> {cpuUsage}% "
        f"<b>RAM:</b> {memory}% "
        f"<b>Disk:</b> {disk}%"
    )
    sendMessage(stats, context.bot, update)

def start(update, context):
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Repo", "https://github.com/harshpreets63/Mirror-Bot")
    buttons.buildbutton("Channel", "https://t.me/HarshMirror")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
This bot can mirror all your links to Google Drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
        sendMarkup(start_string, context.bot, update, reply_markup)
    else:
        sendMarkup(
            'Oops! not a Authorized user.\nPlease join our Channel.\nOr Host Your Own Bot Using My Repo.',
            context.bot,
            update,
            reply_markup,
        )

def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message ID and chat ID in order to edit it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    fs_utils.clean_all()
    os.execl(executable, executable, "-m", "bot")


def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f"{end_time - start_time} ms", reply)


def log(update, context):
    sendLogFile(context.bot, update)


def bot_help(update, context):
    help_string = f"""
/{BotCommands.HelpCommand}: To get this message

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring the link to google drive.

/{BotCommands.CloneCommand} [Drive_Link]: Copy link to google drive
/{BotCommands.CountCommand} [Drive_Link]: Count Files Of a Drive Link

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link] : starts mirroring and if downloaded file is any archive , extracts it to google drive
/{BotCommands.ZipMirrorCommand} [download_url][magnet_link]: start mirroring and upload the archived (.zip) version of the download
/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: start mirroring and upload the archived (.tar) version of the download

/{BotCommands.LeechCommand} [download_url][magnet_link]: Start mirroring the link to telegram
/{BotCommands.UnzipLeechCommand} [download_url][magnet_link] : starts mirroring and if downloaded file is any archive , extracts it to telegram
/{BotCommands.ZipLeechCommand} [download_url][magnet_link]: start mirroring and upload the archived (.zip) version of the download
/{BotCommands.TarLeechCommand} [download_url][magnet_link]: start mirroring and upload the archived (.tar) version of the download

/{BotCommands.WatchCommand} [youtube-dl supported link]: Mirror through youtube-dl. Click /{BotCommands.WatchCommand} for more help
/{BotCommands.LeechWatchCommand} Mirror Youtube-dl support link(Leech)"),
/{BotCommands.LeechTarWatchCommand} Mirror Youtube playlist link as .tar(Leech)"),
/{BotCommands.LeechZipWatchCommand} Mirror Youtube playlist link as .zip(Leech)"),
/{BotCommands.ZipWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and zip before uploading
/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.CancelMirror} Reply to the message by which the download was initiated and that download will be cancelled

/{BotCommands.StatusCommand} Shows a status of all the downloads

/{BotCommands.SpeedCommand} Test Internet Speed Of the Bot

/{BotCommands.ListCommand} [search term]: Searches the search term in the Google drive, if found replies with the link

/{BotCommands.StatsCommand} Show Stats of the machine the bot is hosted on

/{BotCommands.AuthorizeCommand} Authorize a chat or a user to use the bot (Can only be invoked by owner of the bot)

/{BotCommands.LogCommand} Get a log file of the bot. Handy for getting crash reports
/{BotCommands.LeechSetCommand} Leech settings
/{BotCommands.SetThumbCommand} Reply photo to set it as Thumbnail
"""
    button = button_build.ButtonMaker()
    button.buildbutton("Renaming Tips", "https://telegra.ph/Magneto-Python-Aria---Custom-Filename-Examples-01-20")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update, reply_markup)
""""""


botcmds = [
    (f"{BotCommands.HelpCommand}", "Get detailed help"),
    (f"{BotCommands.MirrorCommand}", "Start mirroring"),
    (f"{BotCommands.LeechCommand}", "Start Leeching"),
    (f"{BotCommands.UnzipLeechCommand}", "Extract files(Leech)"),
    (f"{BotCommands.LeechWatchCommand}", "Mirror Youtube-dl support link(Leech)"),
    (f"{BotCommands.LeechTarWatchCommand}", "Mirror Youtube playlist link as .zip(Leech)"),
    (f"{BotCommands.LeechZipWatchCommand}", "Mirror Youtube playlist link as .zip(Leech)"),
    (f"{BotCommands.ZipLeechCommand}", "Start mirroring and upload as .zip(Leech)"),
    (f"{BotCommands.TarLeechCommand}", "Start mirroring and upload as .tar(Leech)"),
    (f"{BotCommands.ZipMirrorCommand}", "Start mirroring and upload as .zip"),
    (f"{BotCommands.TarMirrorCommand}", "Start mirroring and upload as .tar"),
    (f"{BotCommands.UnzipMirrorCommand}", "Extract files"),
    (f"{BotCommands.CloneCommand}", "Copy file/folder from GDrive"),
    (f"{BotCommands.deleteCommand}", "Delete file from GDrive [owner only]"),
    (f"{BotCommands.WatchCommand}", "Mirror Youtube-dl support link"),
    (f"{BotCommands.ZipWatchCommand}", "Mirror Youtube playlist link as .zip"),
    (f"{BotCommands.TarWatchCommand}", "Mirror Youtube playlist link as .tar"),
    (f'{BotCommands.ListCommand}','Search in Drive'),
    (f"{BotCommands.CancelMirror}", "Cancel a task"),
    (f"{BotCommands.CancelAllCommand}", "Cancel all tasks [owner only]"),
    (f"{BotCommands.CountCommand}", "Count files/folders of G-Drive Links"),
    (f"{BotCommands.StatusCommand}", "Get mirror status"),
    (f"{BotCommands.StatsCommand}", "Bot usage stats"),
    (f"{BotCommands.SpeedCommand}", "Check Internet Speed of the Host"),
    (f"{BotCommands.PingCommand}", "Ping the bot"),
    (f"{BotCommands.RestartCommand}", "Restart the bot [owner only]"),
    (f"{BotCommands.LogCommand}", "Get the bot log [owner only]"),
    (f"{BotCommands.AuthorizedUsersCommand}", "Get Authorized Users List[owner only]"),
    (f"{BotCommands.AuthorizeCommand}", "Authorize User To Use Bot [owner only]"),
    (f"{BotCommands.UnAuthorizeCommand}", "UnAuthorize User From Bot [owner only]"),
    (f"{BotCommands.AddSudoCommand}", "Add Sudo User [owner only]"),
    (f"{BotCommands.RmSudoCommand}", "Remove sudo User [owner only]"),
    (f'{BotCommands.LeechSetCommand}','Leech settings'),
    (f'{BotCommands.SetThumbCommand}','Set thumbnail'),
]


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("Restarted successfully!", chat_id, msg_id)
        os.remove(".restartmsg")
    bot.set_my_commands(botcmds)

    start_handler = CommandHandler(
        BotCommands.StartCommand,
        start,
        run_async=True,
    )
    ping_handler = CommandHandler(
        BotCommands.PingCommand,
        ping,
        filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
        run_async=True,
    )
    restart_handler = CommandHandler(
        BotCommands.RestartCommand,
        restart,
        filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
        run_async=True,
    )
    help_handler = CommandHandler(
        BotCommands.HelpCommand,
        bot_help,
        filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
        run_async=True,
    )
    stats_handler = CommandHandler(
        BotCommands.StatsCommand,
        stats,
        filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
        run_async=True,
    )
    log_handler = CommandHandler(
        BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


app.start()
main()
idle()
