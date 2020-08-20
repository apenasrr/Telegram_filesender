"""
    An easy and automatic way to post a series of files to the telegram desktop 
    app, along with personalized descriptions.
    
    Create by: apenasrr
    Project origin: https://github.com/apenasrr/Telegram_filesender

"""

import os
import time
import pyautogui as pag
import pyperclip
import pandas as pd


def ask_create_or_use():

    def create_report_descriptions():

        def gen_data_frame(path_folder):
            
            list_data = []
            for root, dirs, files in os.walk(path_folder):
                for file in files:
                    d = {}
                    d['file_output'] = file
                    d['description'] = file
                    list_data.append(d)
            
            df = pd.DataFrame(list_data)
            list_columns = ['file_output', 'description']
            df = df.reindex(list_columns, axis=1)
            
            return df

        str_msg_paste_folder = 'Paste the path folder with your files'
        str_msg_paste_here = 'Paste here: '
        
        print(str_msg_paste_folder)
        path_folder = input(str_msg_paste_here)
        df = gen_data_frame(path_folder)
        df.to_excel('descriptions.xlsx', index=False)
        
    
    str_msg_create_or_use_1 = 'About the descriptions.xlsx report'
    str_msg_create_or_use_2 = '1-Use existing (default)'
    str_msg_create_or_use_3 = '2-Create a new one\n'
    str_msg_answer = 'Type the number: '
    
    print(str_msg_create_or_use_1)
    print(str_msg_create_or_use_2)
    print(str_msg_create_or_use_3)
    
    create_or_use_answer = input(str_msg_answer)
    if create_or_use_answer == '2':
        create_report_descriptions()
        input('Report Created. Press a key to continue.')
    else:
        pass
        

def set_win_positions():
    """
    Keep the 'windows explorer' windows in front
    and telegram windows in back
    """
    
    pag.hotkey('alt', 'tab')
    time.sleep(0.5)
    pag.keyDown('alt')
    pag.press('tab')
    pag.press('tab')
    pag.keyUp('alt')
    
    
def change_between_telegram_winexplorer():

    pag.hotkey('alt', 'tab')
    time.sleep(1)
    

def get_list_desc(folder_path_descriptions):

    file_path_descriptions = os.path.join(folder_path_descriptions, 
                                          'descriptions.xlsx')
    df_list = pd.read_excel(file_path_descriptions)
    list_desc = df_list['description'].tolist()
    
    return list_desc

def paste_on_telegram_app(desc):

    time.sleep(1)
    pag.hotkey('ctrl', 'v')
    pyperclip.copy(desc)
    time.sleep(2)
    pag.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pag.press('enter')


def main(folder_path_descriptions):
    
    """
    An easy and automatic way to post a series of files to the telegram desktop 
    app, along with personalized descriptions.
    
    # About file list.xlsx
    The excel file 'list.xlsx' in the same folder as this script needs a column 
    named as 'description'
    Fill that column with rows with description of each file
    If you prefer, you can generate this file automatically by selecting the 
    option '2-Create a new one', the descriptions will be filled with the name 
    of the files
    
    # Before start script
    Follow the steps above:
    1. create a empty folder and fill only with the files to be upload  
    2. in script folder, type 'cmd' in the adress bar and press Enter  
    3. when the cmd window open, DON'T press Enter after, but type: 
        python telegram_filesender.py
    4. select the files folder window
    5. select the first file from the folder  
    6. select the window of telegram desktop app  
    7. select the open cmd window and press Enter  
     
    This steps are crucial because the script will constantly switch between 
     windows by alt+tab and select the file above by pressing 'down arrow key'
    """
    
    ask_create_or_use()
    
    list_desc = get_list_desc(folder_path_descriptions)

    set_win_positions()
    
    qt_files = len(list_desc)
    
    print(f'Send {qt_files} files')
    time.sleep(0.5)
    
    for desc in list_desc:
    
        # copy file
        pag.hotkey('ctrl', 'c')
        
        # change to telegram
        change_between_telegram_winexplorer()
        
        # paste on telegram app
        paste_on_telegram_app(desc)
        
        # change back to windows explorer and select next file
        change_between_telegram_winexplorer()
        pag.press('down')
        
    

if __name__ == "__main__":

    folder_script_path_relative = os.path.dirname(__file__)
    folder_script_path = os.path.realpath(folder_script_path_relative)
    
    main(folder_script_path)
