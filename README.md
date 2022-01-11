What's Different in this fork?!

**just** the mirroring massage 👇

[![New Mirroring Massage](https://telegra.ph/file/eace7633a5fb6f94833db.jpg)](https://t.me/MMETMA)

Original Mirroring Massage looked like this 👇

[![Original Mirroring Massage](https://telegra.ph/file/66f215ab585a89cf9aa02.jpg)](https://github.com/harshpreets63/Mirror-Bot)


[![HarshMirroRepo](https://telegra.ph/file/5d6de8adcfc1a7917c422.jpg)](https://t.me/HarshMirrorRepo)

# Important - Read these points first

- Original repo is https://github.com/lzzy12/python-aria-mirror-bot
- I have collected some cool features from various repositories and merged them
  in one.
- So, credits goes to original repo holder, not to me. I have just collected
  them.
- This (or any custom) repo is not supported in official bot support group.
- So if you have any issue then check first that issue is in official repo or
  not, You are only allowed to report that issue in bot support group if that
  issue is also present in official repo.

# Features supported:

- Mirroring direct download links to google drive
- Mirroring Mega.nz links to google drive (In development stage)
- Mirror Telegram files to google drive
- Mirror all youtube-dl supported links
- Mirror Torrent Files and magnet links
- Mirror By Reply
- Custom filename support in direct link, telegram files, YT-DL links
- Extract these filetypes and uploads to google drive
  > ZIP, RAR, TAR, 7z, ISO, WIM, CAB, GZIP, BZIP2, APM, ARJ, CHM, CPIO, CramFS,
  > DEB, DMG, FAT, HFS, LZH, LZMA, LZMA2, MBR, MSI, MSLZ, NSIS, NTFS, RPM,
  > SquashFS, UDF, VHD, XAR, Z.
- Copy files from someone's drive to your drive (using Autorclone)
- Service account support in cloning and uploading
- Download progress
- Upload progress
- Download/upload speeds and ETAs
- Docker support
- Uploading To Team Drives.
- Index Link support
- Shortener support
- View Index Links To Steam Videos Or Music Online (Works With Bhadoo)
- Leech Files To Telegram Supported. 
- Clone Status.
- Multi Drive Search. 
- SpeedTest.
- Count Drive Files.
- Extract password protected files (It's not hack, you have to enter password
  for extracting. LOL)

- For extracting password protected files, using custom filename and download
  from password protected index links see these examples :-
  > https://telegra.ph/Magneto-Python-Aria---Custom-Filename-Examples-01-20

# Multi Search IDs
To use list from multi TD/folder. Run driveid.py in your terminal and follow it. It will generate **drive_folder** file or u can simply create `drive_folder` file in working directory and fill it, check below format:
```
MyTdName tdID IndexLink(if available)
MyTdName2 tdID IndexLink(if available)
```
Turn On RECURSIVE_SEARCH In Config -RECURSIVE_SEARCH = "True"

## Credits :-

- First of all, full credit goes to
  [Shivam Jha aka lzzy12](https://github.com/lzzy12) and
  [JaskaranSM aka Zero Cool](https://github.com/jaskaranSM) They build up this
  bot from scratch.
- Then a huge thanks to [Sreeraj V R](https://github.com/SVR666) You can
  checkout his [repo here](https://github.com/SVR666/LoaderX-Bot)
- Features added from [Sreeraj V R's](https://github.com/SVR666) repo 
    And Anas [repo here](https://github.com/breakdowns/slam-mirrorbot) Repo (Archived)
- Thanks To Ken For Base Repo 
    checkout his [repo here](https://github.com/KenHV/Mirror-Bot)
      

````
1. Added Inline Buttons
2. Added /del command to delete files from drive
3. /list module will post search result on telegra.ph ```
````

- Special thanks to [archie](https://github.com/archie9211) for very much useful
  feature **Unzipmirror**

````
1. unzipmirror
2. Update tracker list dynamically
3. Fix SSL handsake error ```
````

# What is this repo about?

This is a telegram bot writen in python for mirroring files on the internet to
our beloved Google Drive.

# Inspiration

This project is heavily inspired from @out386 's telegram bot which is written
in JS.

## Deploying on Heroku
- Guide For Deploying on Heroku 
<p><a href="https://telegra.ph/Hosting-Mirror-Bot-Guide-10-26"> <img src="https://img.shields.io/badge/Deploy%20Guide-blueviolet?style=for-the-badge&logo=heroku" width="170""/></a></p>

# Contact Me 
- [Telegram](https://T.me/HarshMirrorRepo)

## Generate Database
<details>
    <summary><b>Click Here For More Details</b></summary>

**1. Using ElephantSQL**
- Go to https://elephantsql.com and create account (skip this if you already have **ElephantSQL** account)
- Hit `Create New Instance`
- Follow the further instructions in the screen
- Hit `Select Region`
- Hit `Review`
- Hit `Create instance`
- Select your database name
- Copy your database url, and fill to `DATABASE_URL` in config

**2. Using Heroku PostgreSQL**
<p><a href="https://dev.to/prisma/how-to-setup-a-free-postgresql-database-on-heroku-1dc1"> <img src="https://img.shields.io/badge/See%20Dev.to-black?style=for-the-badge&logo=dev.to" width="160""/></a></p>

</details>

-----

## Gdtot Cookies
To Clone or Leech gdtot link follow these steps:
1. Login/Register to [gdtot](https://new.gdtot.top).
2. Copy this script and paste it in browser address bar.
   - **Note**: After pasting it check at the beginning of the script in broswer address bar if `javascript:` exists or not, if not so write it as shown below.
   ```
   javascript:(function () {
     const input = document.createElement('input');
     input.value = JSON.stringify({url : window.location.href, cookie : document.cookie});
     document.body.appendChild(input);
     input.focus();
     input.select();
     var result = document.execCommand('copy');
     document.body.removeChild(input);
     if(result)
       alert('Cookie copied to clipboard');
     else
       prompt('Failed to copy cookie. Manually copy below cookie\n\n', input.value);
   })();
   ```
   - After pressing enter your browser will prompt a alert.
3. Now you'll get this type of data in your clipboard
   ```
   {"url":"https://new.gdtot.org/","cookie":"PHPSESSID=k2xxxxxxxxxxxxxxxxxxxxj63o; crypt=NGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxWdSVT0%3D"}

   ```
4. From this you have to paste value of PHPSESSID and crypt in config.env file.

-----

# How to deploy?

Deploying is pretty much straight forward and is divided into several steps as
follows:

## Installing requirements

- Clone this repo:

```
git clone https://github.com/magneto261290/magneto-python-aria mirror-bot/
cd mirror-bot
```

- Install requirements For Debian based distros

```
sudo apt install python3
```

Install Docker by following the
[official docker docs](https://docs.docker.com/engine/install/debian/)

- For Arch and it's derivatives:

```
sudo pacman -S docker python
```

- Install dependencies for running setup scripts:

```
pip3 install -r requirements-cli.txt
```

## Setting up config file

```
cp config_sample.env config.env
```

- Remove the first line saying:

```
_____REMOVE_THIS_LINE_____=True
```

Fill up rest of the fields. Meaning of each fields are discussed below:

- **BOT_TOKEN** : The telegram bot token that you get from @BotFather
- **GDRIVE_FOLDER_ID** : This is the folder ID of the Google Drive Folder to
  which you want to upload all the mirrors.
- **DOWNLOAD_DIR** : The path to the local folder where the downloads should be
  downloaded to
- **DOWNLOAD_STATUS_UPDATE_INTERVAL** : A short interval of time in seconds
  after which the Mirror progress message is updated. (I recommend to keep it 5
  seconds at least)
- **OWNER_ID** : The Telegram user ID (not username) of the owner of the bot
- **AUTO_DELETE_MESSAGE_DURATION** : Interval of time (in seconds), after which
  the bot deletes it's message (and command message) which is expected to be
  viewed instantly. Note: Set to -1 to never automatically delete messages
- **IS_TEAM_DRIVE** : (Optional field) Set to "True" if GDRIVE_FOLDER_ID is from
  a Team Drive else False or Leave it empty.
- **USE_SERVICE_ACCOUNTS**: (Optional field) (Leave empty if unsure) Whether to
  use service accounts or not. For this to work see "Using service accounts"
  section below.
- **INDEX_URL** : (Optional field) Refer to
  https://github.com/maple3142/GDIndex/ The URL should not have any trailing '/'
- **API_KEY** : This is to authenticate to your telegram account for downloading
  Telegram files. You can get this from https://my.telegram.org DO NOT put this
  in quotes.
- **API_HASH** : This is to authenticate to your telegram account for
  downloading Telegram files. You can get this from https://my.telegram.org
- **MEGA_KEY**: Mega.nz api key to mirror mega.nz links. Get it from
  [Mega SDK Page](https://mega.nz/sdk)
- **MEGA_USERNAME**: Your email id you used to sign up on mega.nz for using
  premium accounts (Leave th)
- **MEGA_PASSWORD**: Your password for your mega.nz account
- **BLOCK_MEGA_LINKS**: (Optional field) If you want to remove mega.nz mirror
  support (bcoz it's too much buggy and unstable), set it to `True`.
- **SHORTENER**: (Optional field) if you want to use shortener in Gdrive and
  index link, fill shotener url here. Examples :-
  - exe.io
  - gplinks.in
  - shrinkme.io
  - urlshortx.com
  - shortzon.com



Note :- Above are the supported url shorteners. Except these only some url
shorteners are supported. If you want to use any other url shortener then first
ask me that shortener is supported or not.

- **SHORTENER_API**: Fill your shortener api key if you are using shortener.
- **IGNORE_PENDING_REQUESTS**: (Optional field) If you want the bot to ignore
  pending requests after it restarts, set this to `True`.

Note: You can limit maximum concurrent downloads by changing the value of
MAX_CONCURRENT_DOWNLOADS in aria.sh. By default, it's set to 4

## Getting Google OAuth API credential file

- Visit the
  [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Other and Create.
- Use the download button to download your credentials.
- Move that file to the root of mirror-bot, and rename it to credentials.json
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it if it is disabled
- Finally, run the script to generate token file (token.pickle) for Google
  Drive:

````pip install google-api-python-client google-auth-httplib2
google-auth-oauthlib python3 generate_drive_token.py ```

## Deploying

- Start docker daemon (skip if already running):
````

sudo dockerd

````

- Build Docker image:
```sudo docker build . -t mirror-bot
````

- Run the image:

```
sudo docker run mirror-bot
```

# Using service accounts for uploading to avoid user rate limit

For Service Account to work, you must set USE_SERVICE_ACCOUNTS="True" in config
file or environment variables Many thanks to
[AutoRClone](https://github.com/xyou365/AutoRclone) for the scripts **NOTE:**
Using service accounts is only recommended while uploading to a team drive.

## Generating service accounts

## Step 1. Generate service accounts [What is service

account](https://cloud.google.com/iam/docs/service-accounts)

Let us create only the service accounts that we need. **Warning:** abuse of this
feature is not the aim of this project and we do **NOT** recommend that you make
a lot of projects, just one project and 100 sa allow you plenty of use, its also
possible that over abuse might get your projects banned by google.

Note: 1 service account can copy around 750gb a day, 1 project can make 100
service accounts so that's 75tb a day, for most users this should easily
suffice.

```
python3 gen_sa_accounts.py --quick-setup 1 --new-only
```

A folder named accounts will be created which will contain keys for the service
accounts

NOTE: If you have created SAs in past from this script, you can also just re
download the keys by running:

```
python3 gen_sa_accounts.py --download-keys project_id
```

### Add all the service accounts to the Team Drive

- Run:

```
python3 add_to_team_drive.py -d SharedTeamDriveSrcID
```

# Youtube-dl authentication using .netrc file

For using your premium accounts in youtube-dl, edit the netrc file (in the root
directory of this repository) according to following format:

```
machine host login username password my_youtube_password
```

where host is the name of extractor (eg. youtube, twitch). Multiple accounts of
different hosts can be added each separated by a new line
