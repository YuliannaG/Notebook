from pathlib import Path
from typing import Dict, List
from threading import Thread

# вот этот словарь можно вообще хранить и брать из внешнего файла пользовательских настроек
# код теперь написан та, он от него не зависит, пользователь сам может добавлять или удалять
# папки и расшерения
MAPPING = {
        'images': ['.JPEG', '.PNG', '.JPG', '.SVG'],
        'video': ['.AVI', '.MP4', '.MKV', '.MOV'],
        'audio': ['.MP3', '.OGG', '.WAV', '.AMR'],
        'documents': ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.XLS', '.PPTX'],
        'archives': ['.ZIP', '.GZ', '.TAR'],
        'torrents':['.TORRENT',],
    }



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


def old_folders(folder: Path):
    folders_to_delete = []
    for item in folder.glob('**/*'):
        if item.is_dir():
            if item.name not in MAPPING:
                folders_to_delete.append(item)
    return folders_to_delete


def get_folder(ext: str) -> str:
    
    for folder, extension in MAPPING.items():
        if ext in extension:
            return folder
    return 'other'


def resorting(container: Dict[str, List[Path]], main_path: Path):
    for ext, items in container.items():
        sort_folder = get_folder(ext)
        if not (main_path / sort_folder).exists():
            (main_path / sort_folder).mkdir()
        for item in items:
            item.replace(main_path / sort_folder / item.name)


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'{folder} isn`t deleted')


def main(folder: Path, options: int = 0):
    old_fldrs = old_folders(folder)
    container = scan(folder)

    # option 1, no threads
    # resorting(container, folder)

    # option 2, threads
    match options:
        case 0:
            resorting(container, folder)
        case 1:
            threads = [Thread(target=resorting, args=(container, folder)) for _ in range(3)]
            [thread.start() for thread in threads]

    for folder in list(old_fldrs)[::-1]:
        handle_folder(folder)


if __name__ == "__main__":
    main(Path(r'd:\testfolder'))