# Видеонастройки камеры\

from pages.login_page import LoginPage
from pages.camera_settings_page import CameraSettings
from config import *


def test_camera_video_setting(page):
    login_page = LoginPage(page)
    login_page.goto(BASE_URL)
    login_page.login(EMAIL, PASSWORD)

    camera_settings = CameraSettings(page)
    page.wait_for_url("**/cameras**")
    print(f"------------    дождался загрузки страницы    ------------")
    camera_settings.open_camera(CAMERA_NAME)

    # resolutions = list(range(6))
    # bitrate = list(range(13))
    # fps = list(range(22))
    # second_resolutions = list(range(6))
    # second_rbitrate = list(range(13))
    # second_rfps = list(range(22))
    #-----------------------------------------------------------------
    # тестовый пример, где мало значений
    resolutions = [0,1]
    bitrate = [0,1]
    fps = [0,1]
    second_resolutions = [0]
    second_rbitrate = [0,1]
    second_rfps = [0,1]
    #------------------------------------------------------------------
    for resolution_value in resolutions:                                        # функция разрешения
        target_resolution = f"{resolution_value}._originalValue"
        if camera_settings.try_select_resolution(target_resolution):
            for bitrate_value in bitrate:                                       # функция битрейта
                target_bitrate = f"{bitrate_value}._originalValue"
                if camera_settings.try_select_bitrate(target_bitrate):
                    for fps_value in fps:                                       # функция фпс
                        target_fps = f"{fps_value}._originalValue"
                        if camera_settings.try_select_fps(target_fps):
                            camera_settings.save()
                            print(f"------------    {resolution_value} {bitrate_value} {fps_value} saved    --------------")
                            page.wait_for_timeout(7000)

                            res_value = camera_settings.get_rtsp_info(MAIN_CAMERA_RTSP_URL) # ffprobe получение реального разрешения для сравнения
                            current_resolution = camera_settings.get_current_resolution_main()
                            current_fps = float(camera_settings.get_current_fps_main())
                            current_bitrate = float(camera_settings.get_current_bitrate_main())

                            if res_value["resolution"] == current_resolution:
                                print("resolution matched")
                            else:
                                print(f"wrong resolution: {current_resolution}")
                                continue
                            if abs(float(res_value["fps"]) - current_fps) <= current_fps * 0.3:
                                print("fps matched")
                            else:
                                print(f"wrong fps: {current_fps}")
                                continue
                            if abs(float(res_value["bitrate_kbps"]) - current_bitrate) <= current_bitrate * 0.5:
                                print("bitrate kbps matched")
                            else:
                                print(f"wrong bitrate: {current_bitrate}")
                                continue
                        else:
                            continue
                else:
                    continue
        else:
            continue


    for resolution_value in second_resolutions:                                        # функция разрешения
        target_resolution = f"{resolution_value}._originalValue"
        if camera_settings.try_select_2nd_stream_resolution(target_resolution):
            for bitrate_value in second_rbitrate:                                       # функция битрейта
                target_bitrate = f"{bitrate_value}._originalValue"
                if camera_settings.try_select_2nd_stream_bitrate(target_bitrate):
                    for fps_value in second_rfps:                                       # функция фпс
                        target_fps = f"{fps_value}._originalValue"
                        if camera_settings.try_select_2nd_stream_fps(target_fps):
                            camera_settings.save()
                            print(f"------------    {resolution_value} {bitrate_value} {fps_value} saved    --------------")
                            page.wait_for_timeout(7000)

                            res_value = camera_settings.get_rtsp_info(SUB_CAMERA_RTSP_URL) # ffprobe получение реального разрешения для сравнения
                            current_resolution = camera_settings.get_current_resolution_2nd_Stream()
                            current_fps = float(camera_settings.get_current_fps_2nd_Stream())
                            current_bitrate = float(camera_settings.get_current_bitrate_2nd_Stream())

                            if res_value["resolution"] == current_resolution:
                                print("resolution matched")
                            else:
                                print(f"wrong resolution: {current_resolution}")
                                continue
                            if abs(float(res_value["fps"]) - current_fps) <= current_fps * 0.3:
                                print("fps matched")
                            else:
                                print(f"wrong fps: {current_fps}")
                                continue
                            if abs(float(res_value["bitrate_kbps"]) - current_bitrate) <= current_bitrate * 0.5:
                                print("bitrate kbps matched")
                            else:
                                print(f"wrong bitrate: {current_bitrate}")
                                continue
                        else:
                            continue
                else:
                    continue
        else:
            continue



