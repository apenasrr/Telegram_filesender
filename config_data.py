import sys
import os
import config


def import_config():
    # TODO: test config import

    folder_script_path_relative = os.path.dirname(__file__)
    folder_script_path = os.path.realpath(folder_script_path_relative)
    folder_config_path = os.path.join(folder_script_path, 'config')
    sys.path.append(folder_config_path)


def config_data():

    import_config()
    d = {}
    try:
        d['create_new_channel_flag'] = config.create_new_channel
    except:
        d['create_new_channel_flag'] = 1
        pass

    try:
        d['chat_id'] = config.chat_id
    except:
        pass
    config_data = d
    return config_data
