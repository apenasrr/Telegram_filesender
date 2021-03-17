import os

def get_txt_content(file_path):

    file = open(file_path, 'r', encoding='utf-8')
    file_content = file.readlines()
    file_content = ''.join(file_content)
    file.close()
    return file_content


def create_txt(file_path, stringa):

    f = open(file_path, "w", encoding='utf8')
    f.write(stringa)
    f.close()


def create_thumb(file_path):

    path_dir = os.path.split(file_path)[0]
    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    file_name_output = file_name_without_extension + '.jpg'
    file_path_output = os.path.join(path_dir, file_name_output)

    # create thumb
    os.system(f'ffmpeg -i {file_path} -vframes 1 {file_path_output}')
    return file_path_output

