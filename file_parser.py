from pathlib import Path


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def old_folders(folder: Path):
    folders_to_delete = []
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'videos', 'audios', 'documents', 'images', 'other'):
                folders_to_delete.append(item)
    return folders_to_delete


def scan(folder: Path) -> {Path: str}:
    container = {}
    for item in list(folder.glob('**/*.*')):
        ext = get_extension(item.name)
        if not ext:
            container[item] = 'OTHER'
        else:
            container[item] = ext
    return container


    #надо дождаться выполнения всех потоков,
    # вроде как в этом месте, но они не останавливаются, а как такое дебажить я не знаю...
    #FOLDERS.join()
    # while threads:
    #     threads.pop().join()

