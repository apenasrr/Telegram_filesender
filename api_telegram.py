from pyrogram import Client
import credentials
import config
import os
import logging
import sys
import utils_filesender
from ffprobe_micro import ffprobe


def logging_config():
    log_file_name = 'api_telegram'
    logfilename = 'log-' + log_file_name + '.txt'
    logging.basicConfig(
        level=logging.INFO,
        format=' %(asctime)s-%(levelname)s-%(message)s',
        handlers=[logging.FileHandler(logfilename, 'w', 'utf-8')])
    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter(' %(asctime)s-%(levelname)s-%(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


# Keep track of the progress while uploading
def progress(current, total):

    stringa = f"{current * 100 / total:.1f}%"
    sys.stdout.write(stringa)
    sys.stdout.flush()
    sys.stdout.write('\b' * len(stringa))
    sys.stdout.flush()


def send_video(chat_id, file_path, caption):

    logging.info("Sending video...")
    try:
        metadata = ffprobe(file_path).get_output_as_dict()['streams'][0]
    except:
        
        print(file_path)
        print(ffprobe(file_path).get_output_as_dict())
        metadata = ffprobe(file_path).get_output_as_dict()['streams'][0]
    width = metadata['width']
    height = metadata['height']
    duration = int(float(metadata['duration']))
    thumb = utils_filesender.create_thumb(file_path)
    with Client('user', credentials.api_id, credentials.api_hash) as app:
        return_ = app.send_video(chat_id,
                       file_path,
                       caption=caption,
                       progress=progress,
                       supports_streaming=True,
                       width=width,
                       height=height,
                       duration=duration,
                       thumb=thumb)
    os.remove(thumb)
    return return_


def send_document(chat_id, file_path, caption):
    logging.info("Sending document...")
    with Client('user', credentials.api_id, credentials.api_hash) as app:
        return_ = app.send_document(chat_id,
                          file_path,
                          caption=caption,
                          progress=progress)
    return return_


def get_history(chat_id):

    with Client('user', credentials.api_id, credentials.api_hash) as app:
        return_ = app.get_history(chat_id)
    return return_


def send_files(list_dict, chat_id):
    """[summary]

    Args:
        list_dict (list): list of dict. dict with keys:
            file_path=Absolute file_path
            description=file description
    """

    len_list_dict = len(list_dict)
    for index, d in enumerate(list_dict):
        order = index + 1
        file_path = d['file_output']
        
        #TODO: Test if file exist: {file_path}
        
        print(f'{order}/{len_list_dict} Uploading: {file_path}')
        logging.info(f'{order}/{len_list_dict} Uploading: {file_path}')

        file_extension = os.path.splitext(file_path.lower())[1]
        description = d['description']

        if file_extension == '.mp4':
            type_file = 'video'
        else:
            type_file = 'document'

        list_return = []
        if type_file == 'video':
            return_ = send_video(chat_id=chat_id,
                                 file_path=file_path,
                                 caption=description)

        elif type_file == 'document':
            return_ = send_document(chat_id=chat_id,
                                    file_path=file_path, caption=description)
        list_return.append(return_)
    return list_return


def create_channel(title, description):

    with Client('user', credentials.api_id, credentials.api_hash) as app:
        return_chat = \
            app.create_channel(title=title,
                               description=description)
    chat_id = return_chat['id']
    return chat_id


def add_chat_members(chat_id, user_ids):

    with Client('user', credentials.api_id, credentials.api_hash) as app:
        return_chat = \
            app.add_chat_members(chat_id=chat_id,
                                 user_ids=user_ids)


def promote_chat_members(chat_id, user_ids):

    with Client('user', credentials.api_id, credentials.api_hash) as app:

        for user_id in user_ids:
            app.promote_chat_member(chat_id=chat_id,
                                    user_id=user_id,
                                    can_post_messages=True,
                                    can_edit_messages=True,
                                    can_promote_members=True)


def set_chat_description(chat_id, description):

    with Client('user', credentials.api_id, credentials.api_hash) as app:
        app.set_chat_description(chat_id=chat_id, description=description)


def export_chat_invite_link(chat_id):

    with Client('user', credentials.api_id, credentials.api_hash) as app:
        return_ = app.export_chat_invite_link(chat_id=chat_id)

    return return_


def get_channel_title(folder_path_descriptions):

    file_name = 'header_project.txt'
    path_file = os.path.join(folder_path_descriptions, file_name)

    channel_info_stringa = utils_filesender.get_txt_content(path_file)
    list_channel_info = channel_info_stringa.split('\n')

    title = list_channel_info[0]
    return title


def get_channel_description(chat_invite_link, folder_path_descriptions):

    file_name = 'header_project.txt'
    path_file = os.path.join(folder_path_descriptions, file_name)

    channel_info_stringa = utils_filesender.get_txt_content(path_file)
    list_channel_info = channel_info_stringa.split('\n')

    description = '\n'.join(list_channel_info[1:])
    description = description.replace('{chat_invite_link}', chat_invite_link)
    return description


def get_list_adms(folder_script_path):

    file_name = 'channel_adms.txt'
    path_file = os.path.join(folder_script_path, 'config', file_name)
    # TODO: test if path_file exist

    channel_adms_stringa = utils_filesender.get_txt_content(path_file)
    channel_adms_stringa_list = channel_adms_stringa.split('\n')
    list_adms = []
    for line in channel_adms_stringa_list:
        line_lower = line.lower()
        if line_lower.startswith('#'):
            continue
        else:
            list_adms.append(line.strip())
    return list_adms


def get_config_chat_id(folder_path):

    file_name = 'config.py'
    path_file = os.path.join(folder_path, file_name)

    chat_id_raw = utils_filesender.get_txt_content(path_file)
    split_chat_id = chat_id_raw.split('=')
    chat_id = int(split_chat_id[1])
    return chat_id


def main():

    d = {}
    list_dict = []

    d['file_path'] = os.path.join('files', 'teste.mp4')
    d['description'] = 'exemplo de descricao de video **negrita**'
    list_dict.append(d)

    d = {}
    d['file_path'] = os.path.join('files', 'teste.xlsx')
    d['description'] = 'exemplo de descricao de arquio **negrita**'
    list_dict.append(d)

    send_files(list_dict)


if __name__ == "__main__":
    logging_config()
    main()
