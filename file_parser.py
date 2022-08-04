import queue
import sys
from pathlib import Path
from threading import Thread
from collections import defaultdict

IMAGES = []
VIDEO = []
DOCUMENTS = []
AUDIO = []
ARCHIVES = []
OTHER = []


THREAD_POOL_SIZE = 5
FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def old_folders(folder: Path):
    folders_to_delete = []
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'videos', 'audios', 'documents', 'images', 'other'):
                folders_to_delete.append(item)
    return folders_to_delete


def scan(folder: Path) -> {str: Path}:
    container = defaultdict(list)
    for item in list(folder.glob('**/*.*')):
        ext = get_extension(item.name)
        if not ext:  # если у файла нет расширения добавить к неизвестным
            container['OTHER'].append(item)
        else:
            container[ext].append(item)
    return container


    #надо дождаться выполнения всех потоков,
    # вроде как в этом месте, но они не останавливаются, а как такое дебажить я не знаю...
    #FOLDERS.join()
    # while threads:
    #     threads.pop().join()

