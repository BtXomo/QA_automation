
from playwright.sync_api import Page, Locator
from playwright.sync_api import TimeoutError
import ffmpeg
import subprocess
# from config import CAMERA_RTSP_URL


class CameraSettings:
    def __init__(self, page: Page):
        self.page = page
        self.input_container_search: Locator = page.locator("xpath=//input") # Поисковоя строчка
        self.div_tree_view_header_row: Locator = page.locator("xpath=//div[contains(@class, 'iv-ui-icon-button__m-size-small')]") # Всплывающее окно камеры
        self.resolution_select: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div/select") # main stream Разрешение
        self.select_bitrate: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div/select") # main stream Битрейт
        self.select_fps: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div/div/select") # main stream FPS
        self.select_2nd_stream_resolution: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/div/select") # 2nd stream resolution
        self.select_2nd_stream_bitrate: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div/div/div/select") # 2nd stream bitrate
        self.select_2nd_stream_fps: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div/select") # 2nd stream fps
        self.save_button: Locator = page.locator("button[class*='m-theme-light-primary-filled'] span") # Кнопка применения настроек
        self.div_item_interactive: Locator = page.locator("xpath=/html/body/div[9]/div/div[2]/div/div[1]/div/div/div[4]") # Меню настроек во всплывашке
        self.span: Locator = page.locator("xpath=/html/body/div[3]/div/div/div/div/div[2]/div[4]/div/span") #  сообщение успешного применения настроек
        self.span_main_current_resolution: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/span") # выставленное значение текущего разрешения основного потока для сравнения
        self.span_2nd_stream_current_resolution: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/span") # выставленное значение текущего разрешения доп потока для сравнения
        self.span_main_current_fps: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div/div/div[1]/div/span")  # выставленное значение текущего fps для основного потока
        self.span_2nd_stream_current_fps: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div/div[1]/div/span") # выставленное значение текущего fps для доп потока
        self.span_main_stream_current_bitrate: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/span") # выставленное значение текущего битрейта для основного потока
        self.span_2nd_stream_current_bitrate: Locator = page.locator("xpath=/html/body/div[9]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/span") # выставленное значение текущего битрейта для доп потока


# Открытие меню настроек
    def div_scrollable_wrapper(self, camera_name: str): # область с камерой после ввода в поиск имени камеры, необходима для клика всплывающего окна камеры
        return self.page.locator(f"xpath=//div[@style='overflow: hidden;'][.//div[@title='{camera_name}']]")


    def open_camera(self, camera_name: str):
        self.input_container_search.fill(camera_name)                                     # Тыкаем имя камеры в поиск
        print("------------    область камер прогрузилась   ------------")
        self.page.wait_for_timeout(1000)
        self.div_tree_view_header_row.click()                                             # тыкаем три точки для всплывашки
        print("------------    тык три точки для всплывашки    ------------")
        self.div_item_interactive.click()                                                 # тыкаем меню настройки
        print("------------    тык меню настроек, open_camera выполнено    ------------")


# Main stream settings
    def try_select_resolution(self, resolution_value: str) -> bool: # Проверка доступности и выбор нужного разрешения
        try:
            self.resolution_select.select_option(value=resolution_value, timeout=3000)
            print("------------    select_resolution_by_value done    ------------")
            return True
        except TimeoutError:
            print(f"resolution not found: {resolution_value}")
            return False
        
    def try_select_bitrate(self, bitrate_value: str) -> bool: #Проверка доступности и выбор нужного битрейта
        try:
            self.select_bitrate.select_option(value=bitrate_value, timeout=3000)
            print("------------    select_bitrate_by_value done    ------------")
            return True
        except TimeoutError:
            print(f"bitrate not found: {bitrate_value}")
            return False

    def try_select_fps(self, fps_value: str) -> bool: # Проверка доступности и выбор FPS
        try:
            self.select_fps.select_option(value=fps_value, timeout=3000)
            print("------------    select_fps_by_value done    ------------")
            return True
        except TimeoutError:
            print(f"fps not found: {fps_value}")
            return False


# 2nd stream settings
    def try_select_2nd_stream_resolution(self, resolution_value: str) -> bool:  # Проверка доступности и выбор нужного разрешения
        try:
            self.select_2nd_stream_resolution.select_option(value=resolution_value, timeout=3000)
            print("------------    select_resolution_by_value done    ------------")
            return True
        except TimeoutError:
            print(f"resolution not found: {resolution_value}")
            return False

    def try_select_2nd_stream_bitrate(self, bitrate_value: str) -> bool:  # Проверка доступности и выбор нужного битрейта
        try:
            self.select_2nd_stream_bitrate.select_option(value=bitrate_value, timeout=3000)
            print("------------    select_bitrate_by_value done    ------------")
            return True
        except TimeoutError:
            print(f"bitrate not found: {bitrate_value}")
            return False

    def try_select_2nd_stream_fps(self, fps_value: str) -> bool:  # Проверка доступности и выбор FPS
        try:
            self.select_2nd_stream_fps.select_option(value=fps_value, timeout=3000)
            print("------------    select_fps_by_value done    ------------")
            return True
        except TimeoutError:
            print(f"fps not found: {fps_value}")
            return False


    def get_rtsp_info(self, CAMERA_RTSP_URL: str):  # Получение значения разрешения, fps, битрейта
        ffprobe_path = r"ffmpeg/bin/ffprobe.exe" # Путь к исполнительному файлу

        try:
            #  Получение метаданных потока: ширина, высота и частота.
            probe = ffmpeg.probe(
                CAMERA_RTSP_URL,
                cmd=ffprobe_path,
                rtsp_transport='tcp',  # Принудительно используем TCP вместо UDP.
                analyzeduration='2000000',  # Анализировать первые 2 секунды
                probesize='5000000',  # Лимит данных для анализа (5 МБ)
                find_stream_info=None  # Включаем глубокий анализ для точного FPS
            )

            # Ищем видеопоток среди всех дорожек
            # Проходит по всем потокам и берёт первый, у которого codec_type == 'video', поток найден - идут вычисления
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

            if video_stream:
                # 1. Разрешение
                width = video_stream.get('width')
                height = video_stream.get('height')
                resolution = f"{width}x{height}"

                # 2. FPS
                # Используем avg_frame_rate вместо r_frame_rate для исключения удвоения полей
                # Берётся средняя частота кадров
                fps_string = video_stream.get('avg_frame_rate', '0/1')

                # Если avg_frame_rate пустой или равен "0/0", берем r_frame_rate(иногда показывает не реальный FPS, а номинальное значение)
                if fps_string in ('0/1', '0/0'):
                    fps_string = video_stream.get('r_frame_rate', '0/1')

                # Преобразование строки вида 25/1 в 25.0
                num, den = map(int, fps_string.split('/'))
                fps = num / den if den != 0 else 0

                # 3. Точный битрейт
                cmd_bitrate = [
                    ffprobe_path,
                    "-rtsp_transport", "tcp",
                    "-select_streams", "v:0", # подключается к первому видеопотоку v:0
                    "-read_intervals", "%+5", # чтение данных только за 5 секунд ("%+5")
                    "-hide_banner",
                    "-show_entries", "packet=size", # выводит размер каждого пакета (packet=size)
                    "-of", "csv=p=0", # результат в простом CSV-формате
                    CAMERA_RTSP_URL
                ]

                try:
                    # Запускаем сбор пакетов на 5 секунд, запускается как отдельный процесс
                    # Из stdout берутся размеры пакетов
                    result = subprocess.run(cmd_bitrate, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                            check=True)
                    # Суммируем размеры всех пакетов, что бы получить общий объем данных за 5 сек
                    total_bytes = sum(int(line) for line in result.stdout.splitlines() if line.strip().isdigit())

                    if total_bytes > 0:
                        bitrate_value = (total_bytes * 8) / 5 / 1024 # перевод байтов в биты, деление на 5 секунд, перевод в килобиты
                        bit_rate_kbps = f"{bitrate_value:.2f}"  # Возвращаем строку с числом вида 362.93
                    else:
                        bit_rate_kbps = "Не определен (пустой поток)" # Если поток пустой
                except Exception as e:
                    bit_rate_kbps = "Ошибка замера" # Если произошла любая ошибка при замере

                # Вывод результатов в консоль
                print(f"Разрешение: {resolution}")
                print(f"Кадры в секунду (FPS): {fps:.2f}")
                print(f"Битрейт: {bit_rate_kbps} kbps")

                return {
                        "resolution": resolution,
                        "fps": fps,
                        "bitrate_kbps": bit_rate_kbps,
                        }

            else: # если видеопоток не найден или произошла ошибка
                print("Видеопоток не найден в данном RTSP-адресе.")
                return None, None, None

        except ffmpeg.Error as e:
            print("Ошибка при подключении к RTSP или анализе потока:")
            print(e.stderr.decode('utf-8') if e.stderr else str(e))
            return None, None, None


    def get_current_resolution_main (self): # Получение значения установленного на основной поток разрешения
        return self.span_main_current_resolution.text_content()

    def get_current_resolution_2nd_Stream (self): # Получение значения установленного на дополнительный поток разрешения
        return self.span_2nd_stream_current_resolution.text_content()
    
    def get_current_fps_main (self): # Получение значения установленного на основной поток FPS
        return self.span_main_current_fps.text_content()

    def get_current_fps_2nd_Stream (self): # Получение значения установленного на дополнительный поток FPS
        return self.span_2nd_stream_current_fps.text_content()
    
    def get_current_bitrate_main (self): # Получение значения установленного на основной поток битрейта
        return self.span_main_stream_current_bitrate.text_content()

    def get_current_bitrate_2nd_Stream (self): # Получение значения установленного на дополнительный поток битрейта
        return self.span_2nd_stream_current_bitrate.text_content()
    

# Применение настроек
    def save(self): # применение настроек
        self.save_button.click()
        try:
            self.span.wait_for(state="visible", timeout=3000)
            print("------------    Save done    ------------")
            return True
        except TimeoutError:
            print("------------    Save failed    ------------")
            return False

