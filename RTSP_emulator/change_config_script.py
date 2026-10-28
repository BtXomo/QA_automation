import json
import os
import sys
from pathlib import Path



TARGET_FILE_PATH = Path("/app/data")                                            # Путь к папке с видео
VIDEO_EXTENSIONS = ('.mkv', '.avi', '.mp4')                                     # Искомые расширения
CONFIG_FILE = Path(__file__).resolve().parent / 'tamplate_videoserverd.config'  # Шаблон конфига
TARGET_CONFIG_FILE = Path("/app/config/videoserverd.config")                    # Путь к конфигу сервера

def generate_camera_template(file_id, file_name, absolute_file_path):
    return {
        "archiveId": 1,
        "audioUrl": "",
        "gui": {
            "desktop": {
                "channel": 0,
                "manufacturer": "",
                "model": "",
                "password": "",
                "showAdvancedSettings": True,
                "showSubstreamsSettings": True,
                "syncSubstreams": True,
                "user": ""
            }
        },
        "id": file_id,
        "mdExcludedZoneList": None,
        "mdSensitivity": 50,
        "mdType": "",
        "name": file_name,
        "ptzUrl": "",
        "recordQuality": "high",
        "recordType": "disable",
        "rtspTransport": "auto",
        "schedule": [
            {"action": "rec_m", "begin": 0, "dayOfWeek": day, "end": 86400}
            for day in ["su", "mo", "tu", "we", "th", "fr", "sa"]
        ],
        "soundDetectorThreshold": 50,
        "streamHigh": {"audioMaxFrameSize": 0, "bufferLimitKiB": 0, "bufferLimitSec": 0, "videoMaxFrameSize": 0},
        "streamLow": {"audioMaxFrameSize": 0, "bufferLimitKiB": 0, "bufferLimitSec": 0, "videoMaxFrameSize": 0},
        "streamMedium": {"audioMaxFrameSize": 0, "bufferLimitKiB": 0, "bufferLimitSec": 0, "videoMaxFrameSize": 0},
        "streamPreview": {"audioMaxFrameSize": 0, "bufferLimitKiB": 0, "bufferLimitSec": 0, "videoMaxFrameSize": 0},

        "urlHigh": f"file://{absolute_file_path}",
        "urlLow": "",
        "urlMedium": "",
        "urlPreview": "",
        "useCamera": True,
        "useCameraMotionDetector": False,
        "useMotionDetector": False,
        "usePreview": False,
        "useProbeMode": True,
        "usePtz": False,
        "useSound": True,
        "useSoundDetector": False
    }


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Ошибка: Файл конфигурации {CONFIG_FILE} не найден.")
        sys.exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(data):
    with open(TARGET_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


def main():
    config = load_config()
    cameras = config.get("cameras", [])
    file_id = 0

    # проверяем есть ли в конфиге ртсп сервер
    if "rtspServer" not in config:
        config["rtspServer"] = {}
    if "aliases" not in config["rtspServer"]:
        config["rtspServer"]["aliases"] = {}

    for file_path in TARGET_FILE_PATH.rglob('*'):
        # Проверяем нужную папку на файлы внутри и что эти файлы с нужным расширением. Потом записываем в конфиг
        if file_path.is_file() and file_path.suffix.lower() in VIDEO_EXTENSIONS:
            file_name = file_path.name
            absolute_file_path = str(file_path.resolve())
            file_id = file_id + 1

            aliases = config["rtspServer"]["aliases"]

            add_file = generate_camera_template(file_id, file_name, absolute_file_path)
            cameras.append(add_file)
            config["cameras"] = cameras

            alias_id = file_id << 16
            alias_key = f"/live/{alias_id}/high"

            aliases[alias_key] = {
                "camera": absolute_file_path
            }

    save_config(config)


if __name__ == '__main__':
    main()
