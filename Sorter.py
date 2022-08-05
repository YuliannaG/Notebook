import shutil
import re
from threading import Thread
from pathlib import Path
from typing import Dict, List


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W(?!.)', '_', t_name)
    return t_name


def old_folders(folder: Path):
    folders_to_delete = []
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in MAPPING:
                folders_to_delete.append(item)
    return folders_to_delete


def scan(folder: Path) -> Dict[str, List[Path]]:
    container = {}
    for item in list(folder.glob('**/*.*')):
        if item.is_dir():
            continue
        ext = item.suffix.upper()
        if container.get(ext):
            container[ext].append(item)
        else:
            container[ext] = [item]
    return container


MAPPING = {
    'images': ['.JPEG', '.PNG', '.JPG', '.SVG'],
    'video': ['.AVI', '.MP4', '.MKV', '.MOV'],
    'audio': ['.MP3', '.OGG', '.WAV', '.AMR'],
    'documents': ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.XLS', '.PPTX'],
    'archives': ['.ZIP', '.GZ', '.TAR'],
    'other': []
}


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив
    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'This file is not archive:{filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'{folder} isn`t deleted')


def get_folder(ext: str) -> str:
    for folder, extension in MAPPING.items():
        if ext in extension:
            return folder
    return 'other'


def resorting(container: Dict[str, List[Path]], main_path: Path):
    try:
        for ext, items in container.items():
            sort_folder = get_folder(ext)
            if not (main_path / sort_folder).exists():
                (main_path / sort_folder).mkdir()
            for item in items:
                if sort_folder == 'archives':
                    handle_archive(item, main_path / sort_folder)
                else:
                    item.replace(main_path / sort_folder / normalize(item.name))
    except FileNotFoundError:
        pass

def main(folder: Path, options: int = 1):
    container = scan(folder)
    match options:
        case 0:
            resorting(container, folder)
        case 1:
            threads = [Thread(target=resorting, args=(container, folder)) for _ in range(3)]
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]

    my_old_folders = old_folders(folder)
    for folder in list(my_old_folders)[::-1]:
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
            print('Such path or folder does not exist, try again or type exit to go back into main menu')


if __name__ == '__main__':
    main(Path(r'C:\Users\yulia\Documents\Python\test_sorter'))
