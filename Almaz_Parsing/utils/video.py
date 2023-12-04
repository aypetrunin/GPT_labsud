## **🔰 Упрощенный код для Whisper [ver.2 Google Colab] 08-09-2023**
#!ls -ahl
#@markdown Проврека выделенной видео-карты (нужна T4 или выше)
#!nvidia-smi
#!nvidia-smi --query-gpu=name --format=csv,noheader,nounits

# Установка yt-dlp
#!pip install -q yt-dlp
# Функция очистки ссылок
import re

def clean_youtube_url(url: str) -> str:
    """
    Преобразует любую ссылку на видео YouTube в формат короткой ссылки (https://youtu.be/ID_ВИДЕО).

    Параметры:
        url (str): Исходная ссылка на видео на YouTube.

    Возвращает:
        str: Короткая ссылка на видео или None, если исходная ссылка не соответствует формату YouTube.

    Пример:
        >>> clean_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        "https://youtu.be/dQw4w9WgXcQ"
    """

    # Регулярное выражение для поиска идентификаторов видео YouTube:
    # 1. (?:https?:\/\/)? - необязательный протокол (http или https).
    # 2. (?:www\.)? - необязательный префикс "www".
    # 3. (?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/) - паттерн для длинных (стандартных и embed) и коротких ссылок YouTube.
    # 4. ([a-zA-Z0-9_-]{11}) - идентификатор видео, состоящий из 11 символов.
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

    # Поиск совпадения с помощью регулярного выражения
    match = re.search(pattern, url)
    if match:
        # Если найдено совпадение, извлекаем идентификатор видео
        video_id = match.group(1)
        return f"https://youtu.be/{video_id}"
    else:
        return None
# Список ссылок для загрузки

urls_list = [

"https://www.youtube.com/watch?v=2E7OYulX9bY",
"https://www.youtube.com/watch?v=gWVWUl7m_Wg",
"https://www.youtube.com/watch?v=O6nEtTgXpDE",
"https://www.youtube.com/watch?v=zcP02DOPQ98",


]
# Создаем список "очищенных" коротких ссылок на видео YouTube.
# Все недопустимые или неподходящие ссылки будут проигнорированы.
cleaned_urls = set(filter(None, map(clean_youtube_url, urls_list)))

# Выводим результат
print(cleaned_urls)
# Функция загрузки видео в формате m4a (аудиофайл) с YouTube в директоррию /content/videos/
import subprocess

def download_video(url: str) -> None:
    """
    Загружает видео с YouTube в формате m4a (аудиофайл) и сохраняет в директории /content/audios/.

    Параметры:
        url (str): Ссылка на видео на YouTube.

    Пример:
        >>> download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        ...
    """

    # Команда для yt-dlp, которая:
    # 1. Использует опцию "-x" для извлечения аудио.
    # 2. Устанавливает формат аудио в "m4a".
    # 3. Определяет путь для сохранения файла.
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "m4a",
        "-o", "/content/audios/%(title)s.%(ext)s",
        url
    ]

    try:
        # Инициализация подпроцесса с заданной командой.
        # stdout=subprocess.PIPE позволяет читать вывод в реальном времени.
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Чтение вывода команды в реальном времени и его вывод на экран.
        for line in process.stdout:
            print(line.strip())

        # Ожидание завершения подпроцесса и получение кода завершения.
        return_code = process.wait()

        # Если процесс завершился с ошибкой (не нулевой код завершения), генерируем исключение.
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)

    # Обработка исключений при выполнении команды.
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обработке ссылки {url}:")
        print(str(e))
# Перебор каждой очищенной ссылки из списка cleaned_urls.
# Для каждой ссылки будет вызвана функция download_video,
# которая загрузит видео в формате m4a и сохранит его в директории /content/audios/.
for url in cleaned_urls:
    download_video(url)
# Установка whisper
# !pip install -q git+https://github.com/openai/whisper.git
import os
from typing import List

def _construct_whisper_command(input_path: str, output_dir: str) -> List[str]:
    """
    Формирование команды для программы whisper.

    Args:
    - input_path (str): Путь к исходному аудиофайлу.
    - output_dir (str): Путь к директории, где сохранить результаты транскрибации.

    Returns:
    - List[str]: Список аргументов для команды whisper.

    Команда whisper используется для автоматической транскрибации аудиозаписей.
    В данной функции мы формируем список аргументов для этой команды:
    1. `--model large-v2`: использование улучшенной большой модели (версии 2) для транскрибации.
    2. `--language ru`: указание языка речи на русском.
    3. `--device cuda`: использование графического процессора (GPU) для ускорения транскрибации.
    4. `--output_format txt`: формат вывода результатов транскрибации в текстовом файле.
    """
    return [
        'whisper',
        input_path,
        '--model', "large-v2",
        '--language', 'ru',
        '--device', 'cuda',
        '--output_format', 'all',
        '--output_dir', output_dir
    ]


def transcribe_audio_files(input_directory: str, output_directory: str) -> None:
    """
    Транскрибирование всех аудиофайлов из указанной директории с помощью whisper.

    Args:
    - input_directory (str): Директория с исходными аудиофайлами.
    - output_directory (str): Директория для сохранения результатов транскрибации.

    Для каждого файла из `input_directory` запускается процесс транскрибации.
    Результаты сохраняются в поддиректории `output_directory`, где каждая поддиректория соответствует одному аудиофайлу.
    """

    # Проверка наличия выходной директории и её создание при отсутствии
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Формирование списка аудиофайлов с расширением .m4a
    files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f)) and f.endswith('.m4a')]

    # Для каждого аудиофайла:
    for file in files:
        input_path = os.path.join(input_directory, file)

        # Имя поддиректории формируется на основе имени файла без расширения
        subdir_name = os.path.splitext(file)[0]
        subdir_path = os.path.join(output_directory, subdir_name)

        # Информирование пользователя о текущем файле
        print(f"Транскрибирование файла: {file}...")

        # Формирование команды для whisper
        cmd = _construct_whisper_command(input_path, subdir_path)

        # Запуск процесса транскрибации и вывод результатов в реальном времени
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True) as process:
            for line in iter(process.stdout.readline, ''):
                print(line, end='')  # Вывод строки в реальном времени
            print(f"\nТранскрибирование файла {file} завершено.")

transcribe_audio_files('/content/audios', '/content/out')
#!ls -ahl /content/audios
#!ls -ahl /content/out
#!zip -r /content/out.zip /content/out
from google.colab import files
files.download("/content/out.zip")

#import os

directory = '/content/out'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print(f)
#создаем папку для вывода текстовый файлов с заголовками для БД
os.mkdir("/content/out_txt2")
#Пройдемся по всем файлам каталога out и найдем текстовые
#Преобразуем файл следующим образом
#1. Из названия файла сформируем его заголовок (заменив символ '|' на точку)
#2. Добавим заловок в начало, оформив в "#"
#3. Из содержимого файла уберу символы переноса строк (все равно оцифровывать)
directory = '/content/out'
directory_final = '/content/out_txt'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.txt'):
             TextHeader = file.replace( " ｜ ", '. ')

             with open (os.path.join(root, file )  , 'r') as f:
                old_data = f.read()
             #print(old_data)
             #new_data = f"#{TextHeader}#\n {old_data}"
             #print(new_data)
             print(f"{directory_final}/{file}")
             with open (f"{directory_final}/{file}" , 'w') as f:
                f.write(f"#{file.replace( ' ｜ ', '. ')}#\n{old_data}" )



#!zip -r /content/out_txt.zip /content/out_txt
from google.colab import files
files.download("/content/out_txt.zip")
#Собираем все файлы из директории в один
import fileinput, glob, os

# каталог текстовых файлов
path = '/content/out_txt'
# паттерн поиска файлов по расширению
pattern = '*.txt'

glob_path = os.path.join(path, pattern)
list_files = glob.glob(glob_path)
# расширение нового файла установим как '.all'
new_file = '/content/video_database.txt'

if list_files:
    # открываем список файлов 'list_files' на чтение
    # и новый общий файл 'new_file' на запись
    with fileinput.FileInput(files=list_files) as fr, open(new_file, 'w') as fw:
        # читаем данные построчно
        for line in fr:
            # определяем первую строку нового файла
            if fr.isfirstline():
                # название читаемого файла
                file_name = fr.filename()
                # дописываем строку с названием файла
                #fw.write(f'\n {file_name}\n')
                fw.write(f'\n')
            # если нужно, то здесь обрабатываем каждую строку 'line'
            # после обработки дописываем в общий файл
            #fw.write(line)
            fw.write(f"{line.replace( '.txt', '. ')}")
