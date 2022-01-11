import logging
import re
import threading
import time

from bot import download_dict, download_dict_lock
from bot.helper.telegram_helper.bot_commands import BotCommands
LOGGER = logging.getLogger(__name__)

MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"


class MirrorStatus:
    STATUS_UPLOADING = "📤 Uploading..."
    STATUS_DOWNLOADING = "📥 Downloading..."
    STATUS_WAITING = "⏳ Queued..."
    STATUS_FAILED = "Failed. Cleaning download..."
    STATUS_CANCELLED = "Cancelled."
    STATUS_ARCHIVING = "Archiving..."
    STATUS_EXTRACTING = "Extracting..."
    STATUS_SPLITTING = "Splitting..."
    STATUS_CLONING = "📂 Cloning..."


PROGRESS_MAX_SIZE = 100 // 8
PROGRESS_INCOMPLETE = ["■", "■", "■", "■", "■", "■", "■"]

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def check_limit(size, limit):
    LOGGER.info('Checking File/Folder Size...')
    if limit is not None:
        limit = limit.split(' ', maxsplit=1)
        limitint = int(limit[0])
        if 'G' in limit[1] or 'g' in limit[1]:
            if size > limitint * 1024**3:
                return True
        elif 'T' in limit[1] or 't' in limit[1]:
            if size > limitint * 1024**4:
                return True        


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"

def getAllDownload():
    with download_dict_lock:
        for dlDetails in download_dict.values():
            status = dlDetails.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                    MirrorStatus.STATUS_CLONING,
                    MirrorStatus.STATUS_UPLOADING,
                ]
                and dlDetails
            ):
                return dlDetails
    return None

def getDownloadByGid(gid):
    with download_dict_lock:
        for dl in download_dict.values():
            status = dl.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                ]
                and dl.gid() == gid
            ):
                return dl
    return None


def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    cPart = p % 8 - 1
    p_str = "■" * cFull
    if cPart >= 0:
        p_str += PROGRESS_INCOMPLETE[cPart]
    p_str += "□" * (PROGRESS_MAX_SIZE - cFull)
    p_str = f"[{p_str}]"
    return p_str

def get_readable_message():
    with download_dict_lock:
        msg = ""
        for download in list(download_dict.values()):
            msg += f"<b>Filename:</b> <code>{download.name()}</code>"
            msg += f"\n\n<b>{download.status()}</b>"
            if download.status() != MirrorStatus.STATUS_ARCHIVING and download.status() != MirrorStatus.STATUS_EXTRACTING and download.status() != MirrorStatus.STATUS_SPLITTING:
                msg += f"\n\n{get_progress_bar_string(download)} {download.progress()}"
                if download.status() == MirrorStatus.STATUS_DOWNLOADING:
                    msg += f"\n\n<b>✅ Downloaded:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                elif download.status() == MirrorStatus.STATUS_CLONING:
                        msg += f"\n\n<b>✅ Cloned:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"                   
                else:
                    msg += f"\n\n<b>✅ Uploaded:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                msg += f"\n\n<b>🚀 Speed:</b> {download.speed()}" \
                        f"\n\n<b>⏰ Time Left:</b> {download.eta()} "
                # if hasattr(download, 'is_torrent'):
                try:
                    msg += f"\n\n<b>🌱 Seeders:</b> {download.aria_download().num_seeders}" \
                        f" | <b>Peers:</b> {download.aria_download().connections}"
                except:
                    pass
                    try:
                        msg += f"\n\n<b>🌱 Seeders:</b> {download.torrent_info().num_seeds}" \
                            f" | <b>Leechers:</b> {download.torrent_info().num_leechs}"
                    except:
                        pass
                msg += f''
                msg += f"\n\n<b>⛔ To Stop:</b> <code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            msg += "\n\n"
        return msg    

def get_readable_time(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result


def is_gdrive_link(url: str):
    return "drive.google.com" in url

def is_gdtot_link(url: str):
    url = re.match(r'https?://.*\.gdtot\.\S+', url)
    return bool(url)

def is_mega_link(url: str):
    return "mega.nz" in url or "mega.co.nz" in url


def is_url(url: str):
    url = re.findall(URL_REGEX, url)
    return bool(url)


def is_magnet(url: str):
    magnet = re.findall(MAGNET_REGEX, url)
    return bool(magnet)


def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
