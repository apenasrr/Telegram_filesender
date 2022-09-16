"""
    An easy and automatic way to post a series of files to the telegram desktop
    app, along with personalized descriptions.

    Create by: apenasrr
    Project origin: https://github.com/apenasrr/Telegram_filesender

    Do you wish to buy a coffee to say thanks?
    LBC (from LBRY) digital Wallet
    > bFmGgebff4kRfo5pXUTZrhAL3zW2GXwJSX

    We recommend:

    mises.org - Educate yourself about economic and political freedom
    lbry.tv - Store files and videos on blockchain ensuring free speech
    https://www.activism.net/cypherpunk/manifesto.html -  How encryption is essential to Free Speech and Privacy
"""

import os
import sys
import time

import pandas as pd
import pyautogui as pag
import pyperclip

from api_telegram import (
    add_chat_members,
    create_channel,
    ensure_connection,
    export_chat_invite_link,
    get_channel_description,
    get_channel_title,
    get_list_adms,
    promote_chat_members,
    send_file,
    send_message,
    set_chat_description,
)
from config_data import config_data
from utils_filesender import create_txt, get_txt_content


def ask_create_or_use():
    def create_report_descriptions():
        def gen_data_frame(path_folder):

            list_data = []
            for root, _, files in os.walk(path_folder):
                for file in files:
                    d = {}
                    file_path = os.path.join(root, file)
                    d["file_output"] = file_path
                    d["description"] = file
                    list_data.append(d)

            df = pd.DataFrame(list_data)
            list_columns = ["file_output", "description"]
            df = df.reindex(list_columns, axis=1)

            return df

        str_msg_paste_folder = "Paste the path folder with your files"
        str_msg_paste_here = "Paste here: "

        print(str_msg_paste_folder)
        path_folder = input(str_msg_paste_here)
        df = gen_data_frame(path_folder)
        df.to_excel("descriptions.xlsx", index=False)

    str_msg_create_or_use_1 = "About the descriptions.xlsx report"
    str_msg_create_or_use_2 = "1-Use existing (default)"
    str_msg_create_or_use_3 = "2-Create a new one\n"
    str_msg_answer = "Type the number: "

    print(str_msg_create_or_use_1)
    print(str_msg_create_or_use_2)
    print(str_msg_create_or_use_3)

    create_or_use_answer = input(str_msg_answer)
    if create_or_use_answer == "2":
        create_report_descriptions()
        input("Report Created. Press a key to continue.")
    else:
        pass


def pag_hotkey(key_1, key_2):

    pag.keyDown(key_1)
    pag.keyDown(key_2)
    pag.keyUp(key_1)
    pag.keyUp(key_2)


def set_win_positions():
    """
    Keep the 'windows explorer' windows in front
    and telegram windows in back
    """

    pag_hotkey("alt", "tab")
    time.sleep(1)
    pag.keyDown("alt")
    pag.press("tab")
    time.sleep(0.5)
    pag.press("tab")
    pag.keyUp("alt")
    time.sleep(0.5)


def change_between_telegram_winexplorer():

    pag_hotkey("alt", "tab")
    time.sleep(2)


def get_next_video_to_send(path_file_description):

    try:
        df = pd.read_excel(path_file_description, engine="openpyxl")
    except Exception as e:
        print(f"Can't open file: {path_file_description}")
        print(e)

    mask_df_to_send = df["sent"].isin([0])
    df_to_send = df.loc[mask_df_to_send, :]
    count_files_to_send = df_to_send.shape[0]
    if count_files_to_send == 0:
        return 0, False
    else:
        file_index = df_to_send.index[0]
        df_to_send = df_to_send.reset_index(drop=True)
        dict_first_line = df_to_send.loc[0, :]
        return file_index, dict_first_line


def update_description_file_sent(path_file_description, dict_file_data):

    try:
        df = pd.read_excel(path_file_description, engine="openpyxl")
    except Exception as e:
        print(f"Can't open file: {path_file_description}")
        print(e)

    file_path = dict_file_data["file_output"]
    mask_file_path = df["file_output"].isin([file_path])
    df_filter = df.loc[mask_file_path, :]
    len_df_filter = len(df_filter)
    if len_df_filter != 1:
        print(f"Find {len_df_filter} line for file: {file_path}")
        sys.exit()
    index_video = df_filter.index
    # update df
    df.loc[index_video, "sent"] = 1
    df.to_excel(path_file_description, index=False)


def ensure_existence_sent_column(df_list, file_path_descriptions):

    description_columns = df_list.columns
    if "sent" not in description_columns:
        df_list["sent"] = 0
        df_list.to_excel(file_path_descriptions, index=False)


def get_list_desc(folder_path_descriptions):

    file_path_descriptions = os.path.join(
        folder_path_descriptions, "descriptions.xlsx"
    )
    df_list = pd.read_excel(file_path_descriptions, engine="openpyxl")

    # TODO: Consider using df.to_dict()
    list_desc = []
    for _, row in df_list.iterrows():
        d = {}
        d["file_output"] = row["file_output"]
        d["description"] = row["description"]
        list_desc.append(d)

    return list_desc


def paste_on_telegram_app(desc):

    time.sleep(2)
    pag_hotkey("ctrl", "v")
    pyperclip.copy(desc)
    time.sleep(3)
    pag_hotkey("ctrl", "v")
    time.sleep(1)
    pag.press("enter")
    time.sleep(1)


def ask_send_app_or_api():

    str_msg_1 = "How do you intend to send the files?"
    str_msg_2 = "1-By telegram desktop app"
    str_msg_3 = "2-By telegram api (default)\n"
    str_msg_answer = "Type the number: "

    print("\n".join([str_msg_1, str_msg_2, str_msg_3]))

    answer = input(str_msg_answer)

    if answer == "":
        return 2

    return int(answer)


def send_via_telegram_app(list_desc):

    set_win_positions()
    qt_files = len(list_desc)
    print(f"Send {qt_files} files")
    time.sleep(0.5)

    for d in list_desc:
        desc = d["description"]
        # copy file
        pag_hotkey("ctrl", "c")

        # change to telegram
        change_between_telegram_winexplorer()

        # paste on telegram app
        paste_on_telegram_app(desc)

        # change back to windows explorer and select next file
        change_between_telegram_winexplorer()
        pag.press("down")
        time.sleep(0.5)


def process_create_channel(folder_path_descriptions):

    title = get_channel_title(folder_path_descriptions)
    description = "channel description"

    chat_id = create_channel(title=title, description=description)
    return chat_id


def config_channel(
    chat_id, chat_invite_link, list_adms, folder_path_descriptions
):

    description = get_channel_description(
        chat_invite_link, folder_path_descriptions
    )
    set_chat_description(chat_id=chat_id, description=description)

    if len(list_adms) != 0:
        add_chat_members(chat_id=chat_id, user_ids=list_adms)
        promote_chat_members(chat_id=chat_id, user_ids=list_adms)


def send_via_telegram_api(folder_path_descriptions, dict_config):

    file_path_descriptions = os.path.join(
        folder_path_descriptions, "descriptions.xlsx"
    )
    df_list = pd.read_excel(file_path_descriptions, engine="openpyxl")
    ensure_existence_sent_column(df_list, file_path_descriptions)
    files_count = df_list.shape[0]

    chat_id = process_to_send_telegram(folder_path_descriptions, dict_config)
    time_limit = int(dict_config["time_limit"])

    # Connection test to avoid infinite loop of asynchronous attempts
    # to send files without pause to fill connection pool

    ensure_connection()

    while True:
        index, dict_file_data = get_next_video_to_send(file_path_descriptions)
        # mark file as sent
        if dict_file_data is False:
            break
        else:
            file_path = dict_file_data["file_output"]
            print(f"{index+1}/{files_count} Uploading: {file_path}")

            send_file(dict_file_data, chat_id, time_limit)

            update_description_file_sent(
                file_path_descriptions, dict_file_data
            )


def test_chat_id(dict_config):

    if "chat_id" in dict_config.keys():
        chat_id = dict_config["chat_id"]
        is_int = isinstance(chat_id, int)
        if is_int:
            if chat_id < 0:
                return True
        print("config['chat_id'] must be negative integer")
        return False
    else:
        print("config['chat_id'] key 'chat_id' not found in config file")
        return False


def save_metadata_file(chat_id, chat_invite_link, file_path_metadata):

    dict_metadata = {"chat_id": chat_id, "chat_invite_link": chat_invite_link}
    create_txt(file_path_metadata, str(dict_metadata))


def process_to_send_telegram(folder_path_descriptions, dict_config):
    """
    Creates a new properly configured channel
    or use the existing chat_id in the configuration file

    Args:
        folder_path_descriptions (str):
            folder path where the descriptions.xlsx file is located
        dict_config (dict):
            configuration data.
            template: {chat_id:negative int, create_new_channel:boolean}

    Returns:
        int: chat_id. negative integer
    """

    folder_script_path_relative = os.path.dirname(__file__)
    folder_script_path = os.path.realpath(folder_script_path_relative)

    # check if there is necessary to continue upload
    file_path_metadata = os.path.realpath(
        os.path.join(folder_path_descriptions, "channel_metadata")
    )
    continue_upload = False
    if os.path.exists(file_path_metadata):
        dict_metadata = eval(get_txt_content(file_path_metadata))
        continue_upload = True

    # get chat_id
    # Create new channel-Default True
    if dict_config["create_new_channel_flag"] == 0 or continue_upload:
        channel_new = False
    else:
        channel_new = True

    if channel_new:
        # create new channel
        chat_id = process_create_channel(folder_path_descriptions)
        chat_invite_link = export_chat_invite_link(chat_id=chat_id)
        save_metadata_file(chat_id, chat_invite_link, file_path_metadata)

        # config new channel
        list_adms = get_list_adms(folder_script_path)
        config_channel(
            chat_id, chat_invite_link, list_adms, folder_path_descriptions
        )
    else:
        # use existent channel
        if continue_upload:
            dict_data = dict_metadata
        else:
            dict_data = dict_config

        chat_id_is_valid = test_chat_id(dict_data)
        if chat_id_is_valid:
            chat_id = dict_data["chat_id"]

    return chat_id


def main(folder_path_descriptions, dict_config):
    """
    An easy and automatic way to post a series of files to the telegram desktop
    app, along with personalized descriptions.

    How to use: https://github.com/apenasrr/Telegram_filesender/blob/master/README.md

    Args:
        folder_path_descriptions (str):
        dict_config (dict): {create_new_channel_flag: int, chat_id: int}
    """

    ask_create_or_use()
    list_desc = get_list_desc(folder_path_descriptions)
    send_mode = ask_send_app_or_api()

    if send_mode == 1:
        send_via_telegram_app(list_desc)
    elif send_mode == 2:
        send_via_telegram_api(folder_path_descriptions, dict_config)


if __name__ == "__main__":

    dict_config = config_data()
    folder_script_path_relative = os.path.dirname(__file__)
    folder_script_path = os.path.realpath(folder_script_path_relative)
    main(folder_script_path, dict_config)
