# Telegram_filesender
## Auto file sender for Telegram desktop app

An easy and automatic way to post a series of files to the telegram desktop app, along with personalized descriptions.

## How to use

At the moment, only applicable to the O.S. Windows (soon available for linux).

### How to customize file descriptions

First create a `descriptions.xlsx` file by following the steps below.
- Create a empty folder and fill only with the files to be upload
- Run the file `telegram_filesender.bat`
- Press `2` to set the option `2-Create a new one` and type `Enter` to create a new descriptions.xlsx file from you filled folder
- Paste the link of the filled folder and press `Enter`
- Will appear the message `Report Created. Press a key to continue.`, indicating that the `descriptions.xlsx` file was created successfully
- Press `Enter`

### Let's send to Telegram!
There are 2 ways to send to the telegram:
1. Via the Telegram app
2. Via the telegram API

#### Quick FAQ
- "Why send by the Telegram API?"
- Because its is faster, does not generate conflict in virtual machines where you cannot use keyboard/mouse macros and does not freeze your ability to send files in the App Telegram while sending the files

- "When sending via the Telegram app is preferable?"
- When you are not an administrator of the target group/channel, having difficulty extracting the `chat_id` code, necessary when sending via API.

#### For sending via Telegram app:
- select the files folder window
- select the first file from the folder
- select the window of telegram desktop app
- select the open cmd window and press `Enter`

**This steps are crucial** because the script will constantly switch between windows by typing the hotkey `alt + tab` and the `down-arrow` key to select the file bellow in folder.


#### To send via the telegram API:

To connect to Telegram via API, it's necessary get an api_id and an api_hash. But do not worry, it is only necessary to follow these steps once in a lifetime.
- To get the credentials to Telegram API, the codes `api_id` and an `api_hash`:
  - Login to your [Telegram core](https://my.telegram.org/) website
  - Go to the [API development](https://my.telegram.org/apps) tools area
  - There is a form that you need to fill out, and after that, you can receive your `api_id` and `api_hash`
  - To know more, access the Telegram’s help documentation about [how to get your API credentials](https://core.telegram.org/api/obtaining_api_id)
- Open the file `credentials.py` in any text editor, like notepad
- Fill in the `api_id` and `api_hash` flags according to those obtained with the instructions above, similar to the example below:
- `api_id = 1111111` (just an example. replace by the obtained value)
- `api_hash = "sKwrdX7tb2xFDkPU9h0AsKwrdX7tb2xF"` (just an example. replace by the obtained value.)
- Save and close the file

- If you wish to create a new channel (faster option :satisfied:):
  - Open the file `config/config.py` in any text editor
  - Change the flag `create_new_channel` to `1`
  - Save and close the file
  - If you wish to automatically **add adms** to the new channel, add your @Nicks in file `config/channel_adms.txt`
  - If you wish to automatically **customize description** of the new channel:
    - Fill in the file `header_project.txt` so that the first line must be the name of the channel and the other lines must be the description. If you wish, use the flag `{chat_invite_link}` to automatically replaced with the invitation link for the new channel.

- If you wish to send to an existing group/channel (slower option :neutral_face:):
  - First, you need to get the group/channel chat_id. Follow the steps below:
    - Add the bot `@MissRose_bot` to the group/channel
    - Send the msg `/id` in group/channel
    - Bot Rose will respond with the `chat_id`. Must be a negative number with more then or equal to 9 characters.
    - Copy the `chat_id` (including the hyphen)
  - Open the file `config/config.py` in any text editor
  - Change the `chat_id` flag to the value of the copied chat_id, similar to example below
  - e.g.: `chat_id = -111111111`
  - Change the `create_new_channel` flag to `0`, equal to example below
  - e.g.: `create_new_channel = 0`
  - Save and close the file

#### Another Quick FAQ:
- "What suffering! Do I need to repeat all these steps the next time I send files via Telegram API?"
- No! :satisfied: If you are uploading files to a new channel, just adjust the `header_project.txt` file. If the files are going to be send to the same group/channel as previously sent, there is no need to edit `chat_id`.

## Requirement
- [Python](https://www.python.org/downloads/windows/) installed and [added in Windows Path](https://datatofish.com/add-python-to-windows-path/).
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z ) installed and [added in Windows Path](https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/).
- Libs needed:
  - unidecode
  - pyperclip
  - pandas :panda_face:
  - pyautogui (required for sending via Telegram app)
  - pyrogram (required for sending via Telegram API)
- To install the libs, just run the file `update_libs.bat`

Last Update: 2021-03-17

---
Do you wish to buy a coffee to say thanks?
LBC (from LBRY) digital Wallet
> bFmGgebff4kRfo5pXUTZrhAL3zW2GXwJSX

### We recommend:
[mises.org](https://mises.org/) - Educate yourself about economic and political freedom\
[lbry.tv](http://lbry.tv/) - Store files and videos on blockchain ensuring free speech\
https://www.activism.net/cypherpunk/manifesto.html -  How encryption is essential to Free Speech and Privacy