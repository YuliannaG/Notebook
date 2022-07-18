import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MKV_VIDEO = []
MOV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
OTHER = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MKV': MKV_VIDEO,
    'MOV': MOV_VIDEO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Если это папка то добавляем ее с список FOLDERS и преходим к следующему элементу папки
        if item.is_dir():
            # проверяем, чтобы папка не была той в которую мы складываем уже файлы
            if item.name not in ('archives', 'videos', 'audios', 'documents', 'images', 'other'):
                FOLDERS.append(item)
                #  сканируем эту вложенную папку - рекурсия
                scan(item)
            #  перейти к следующему элементу в сканируемой папке
            continue

        #  Пошла работа с файлом
        ext = get_extension(item.name)  # взять расширение
        fullname = folder / item.name  # взять полный путь к файлу
        if not ext:  # если у файла нет расширения добавить к неизвестным
            OTHER.append(fullname)
        else:
            try:
                # взять список куда положить полный путь к файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Если мы не регистрировали расширение в REGISTER_EXTENSIONS, то добавить в другое
                UNKNOWN.add(ext)
                OTHER.append(fullname)


