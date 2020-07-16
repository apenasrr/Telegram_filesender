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
    time.sleep(0.5)
    

def get_list_desc():

    df_list = pd.read_excel(f'list.xlsx')
    list_desc = df_list['description'].tolist()
    
    return list_desc

def paste_on_telegram_app(desc):

    pag.hotkey('ctrl', 'v')
    pyperclip.copy(desc)
    time.sleep(0.5)
    pag.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pag.press('enter')


def main():
    
    """
    An easy and automatic way to post a series of files to the telegram desktop 
    app, along with personalized descriptions.
    
    # About file list.xlsx
    The excel file 'list.xlsx' in the same folder as this script needs a column 
    named as 'description'
    Fill that column with rows with description of each file
    
    # Before start script
    Follow the steps above:
     -create a empty folder and fill only with the files to be upload
     -select this folder window of 'windows explorer'
     -select first file from the folder
     -select windows of telegram desktop app
     -run the script 
     
    This steps are crucial because the script will constantly switch between 
     windows by alt+tab and select the file above by pressing 'down arrow key'
    """
    
    set_win_positions()
    
    list_desc = get_list_desc()
    
    qt_files = len(list_desc)
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
        
        return
    
    
if __name__ == "__main__":
    main()
