from pathlib import Path
import shutil
import file_parser as parser
import re
from threading import Thread


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.name) + filename.suffix))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.name) + filename.suffix))


def handle_archive(filename: Path, target_folder: Path):
    # Создаем папку для архивов
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив
    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    #  создаем папку для архива с именем файла

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'{folder} isn`t deleted')


def main(folder: Path):
    parser.scan(folder)

    for file in parser.IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.VIDEO:
        handle_media(file, folder / 'videos')
    for file in parser.DOCUMENTS:
        handle_media(file, folder / 'documents')
    for file in parser.AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.OTHER:
        handle_other(file, folder / 'OTHER')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    #print([el for i in iter(parser.FOLDERS.get,None)])
    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in list(parser.FOLDERS.queue)[::-1]:
        handle_folder(folder)


def sorter():
    while True:
        print("Print a full way to folder which you want to sort")
        user_input = input(">>>")
        if user_input.lower() == 'exit' or user_input == '.':
            print(f'Opening main menu')
            break        
        folder_for_scan = Path(user_input)
        if folder_for_scan.exists():
            print(f'Start in folder {folder_for_scan.resolve()}')
            main(folder_for_scan.resolve())
            print(f'Folder is sorted, opening main menu')
            break
        else:
            print('Such path or folder isn`t exsist, try again or type exit to go back into main menu')


if __name__ == '__main__':
    # print("Print a full way to folder which you wont to sort")
    # user_input = input(">>>")
    # folder_for_scan = Path(user_input)
    # print(f'Start in folder {folder_for_scan.resolve()}')
    # main(folder_for_scan.resolve())
    while True:
        print("Print a full way to folder which you want to sort")
        user_input = input(">>>")
        if user_input.lower() == 'exit':
            break        
        folder_for_scan = Path(user_input)
        if folder_for_scan.exists():
            print(f'Start in folder {folder_for_scan.resolve()}')
            main(folder_for_scan.resolve())
            print('Folder is sorted, opening main menu')
            break
        else:
            print('Such path or folder doesn`t exist, try again or type exit to go back into main menu')

