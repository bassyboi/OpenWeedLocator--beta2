from tqdm import tqdm
from datetime import datetime, timezone
from greenonbrown import GreenOnBrown
from image_sampler import bounding_box_image_sample, whole_image_save
from imutils.video import count_frames, FileVideoStream
from threading import Thread
import pandas as pd
import numpy as np
import imutils
import time
import glob
import cv2
import csv
import os


def four_frame_analysis(exgFile: str, exgsFile: str, hueFile: str, exhuFile: str, HDFile: str):
    baseName = os.path.splitext(os.path.basename(exhuFile))[0]

    exgVideo = cv2.VideoCapture(exgFile)
    print("[INFO] Loaded {}".format(exgFile))
    lenexg = count_frames(exgFile, override=True) - 1

    exgsVideo = cv2.VideoCapture(exgsFile)
    print("[INFO] Loaded {}".format(exgsFile))
    lenexgs = count_frames(exgsFile, override=True) - 1

    hueVideo = cv2.VideoCapture(hueFile)
    print("[INFO] Loaded {}".format(hueFile))
    lenhue = count_frames(hueFile, override=True) - 1

    exhuVideo = cv2.VideoCapture(exhuFile)
    print("[INFO] Loaded {}".format(exhuFile))
    lenexhu = count_frames(exhuFile, override=True) - 1

    videoHD = cv2.VideoCapture(HDFile)
    print("[INFO] Loaded {}".format(HDFile))
    lenHD = count_frames(HDFile, override=True) - 1

    hdFrame = None
    exgFrame = None
    exgsFrame = None
    hueFrame = None
    exhuFrame = None

    hdframecount = 0
    exgframecount = 0
    exgsframecount = 0
    hueframecount = 0
    exhuframecount = 0

    hdFramesAll = []
    exgFramesAll = []
    exgsFramesAll = []
    hueFramesAll = []
    exhuFramesAll = []

    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord('v') or hdFrame is None:
            if hdframecount >= len(hdFramesAll):
                hdFrame = next(frame_processor(videoHD, 'hd'))
                hdFrame = imutils.resize(hdFrame, height=640)
                hdFrame = imutils.rotate(hdFrame, angle=180)
                hdframecount += 1
                hdFramesAll.append(hdFrame)
            else:
                hdFrame = hdFramesAll[hdframecount]
                hdframecount += 1

        if k == ord('q') or exgFrame is None:
            if exgframecount >= len(exgFramesAll):
                exgFrame = next(frame_processor(exgVideo, 'exg'))
                exgframecount += 1
                exgFramesAll.append(exgFrame)
            else:
                exgFrame = exgFramesAll[exgframecount]
                exgframecount += 1

        if k == ord('w') or exgsFrame is None:
            if exgsframecount >= len(exgsFramesAll):
                exgsFrame = next(frame_processor(exgsVideo, 'exgs'))
                exgsframecount += 1
                exgsFramesAll.append(exgsFrame)
            else:
                exgsFrame = exgsFramesAll[exgsframecount]
                exgsframecount += 1

        if k == ord('e') or hueFrame is None:
            if hueframecount >= len(hueFramesAll):
                hueFrame = next(frame_processor(hueVideo, 'hsv'))
                hueframecount += 1
                hueFramesAll.append(hueFrame)
            else:
                hueFrame = hueFramesAll[hueframecount]
                hueframecount += 1

        if k == ord('r') or exhuFrame is None:
            if exhuframecount >= len(exhuFramesAll):
                exhuFrame = next(frame_processor(exhuVideo, 'exhu'))
                exhuframecount += 1
                exhuFramesAll.append(exhuFrame)
            else:
                exhuFrame = exhuFramesAll[exhuframecount]
                exhuframecount += 1

        if k == ord('b'):
            if hdframecount > 0:
                hdframecount -= 1
                hdFrame = hdFramesAll[hdframecount]
            else:
                hdFrame = hdFramesAll[hdframecount]

        if k == ord('a'):
            if exgframecount > 0:
                exgframecount -= 1
                exgFrame = exgFramesAll[exgframecount]
            else:
                exgFrame = exgFramesAll[exgframecount]

        if k == ord('s'):
            if exgsframecount > 0:
                exgsframecount -= 1
                exgsFrame = exgsFramesAll[exgsframecount]
            else:
                exgsFrame = exgsFramesAll[exgsframecount]

        if k == ord('d'):
            if hueframecount > 0:
                hueframecount -= 1
                hueFrame = hueFramesAll[hueframecount]
            else:
                hueFrame = hueFramesAll[hueframecount]

        if k == ord('f'):
            if exhuframecount > 0:
                exhuframecount -= 1
                exhuFrame = exhuFramesAll[exhuframecount]
            else:
                exhuFrame = exhuFramesAll[exhuframecount]

        # save current frames for the video comparison
        if k == ord('y'):
            cv2.imwrite('images/frameGrabs/{}_frame{}_exg.png'.format(baseName, exgframecount), exgFrame)
            cv2.imwrite('images/frameGrabs/{}_frame{}_exgs.png'.format(baseName, exgsframecount), exgsFrame)
            cv2.imwrite('images/frameGrabs/{}_frame{}_hue.png'.format(baseName, hueframecount), hueFrame)
            cv2.imwrite('images/frameGrabs/{}_frame{}_exhu.png'.format(baseName, exhuframecount), exhuFrame)
            print('[INFO] All frames written.')

        # write text on each video frame
        exgVis = exgFrame.copy()
        exgsVis = exgsFrame.copy()
        hueVis = hueFrame.copy()
        exhuVis = exhuFrame.copy()

        cv2.putText(exhuVis, 'exhu: {} / {}'.format(exhuframecount, lenexhu), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(hueVis, 'hue: {} / {}'.format(hueframecount, lenhue), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(exgsVis, 'exgs: {} / {}'.format(exgsframecount, lenexgs), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(exgVis, 'exg: {} / {}'.format(exgframecount, lenexg), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(hdFrame, 'HD: {} / {}'.format(hdframecount, lenHD), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        # stack the video frames
        topRow = np.hstack((exgVis, exgsVis))
        bottomRow = np.hstack((hueVis, exhuVis))
        combined = np.vstack((topRow, bottomRow))
        combined = np.hstack((combined, hdFrame))

        cv2.imshow('Output', combined)

        if k == 27:
            break


def single_frame_analysis(videoFile: str, HDFile: str, algorithm='exhsv'):
    baseName = os.path.splitext(os.path.basename(videoFile))[0]

    video = cv2.VideoCapture(videoFile)
    print("[INFO] Loaded {}".format(video))
    lenVideo = count_frames(videoFile, override=True) - 1

    videoHD = cv2.VideoCapture(HDFile)
    print("[INFO] Loaded {}".format(HDFile))
    lenHD = count_frames(HDFile, override=True) - 1

    hdFrame = None
    videoFrame = None

    hdframecount = 0
    videoframecount = 0

    hdFramesAll = []
    videoFramesAll = []

    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord('d') or hdFrame is None:
            if hdframecount >= len(hdFramesAll):
                hdFrame = next(frame_processor(videoHD, videoName='hd'))
                hdFrame = imutils.resize(hdFrame, height=640)
                # hdFrame = imutils.rotate(hdFrame, angle=180)
                hdframecount += 1
                hdFramesAll.append(hdFrame)
            else:
                hdFrame = hdFramesAll[hdframecount]
                hdframecount += 1

        if k == ord('s') or videoFrame is None:
            if videoframecount >= len(videoFramesAll):
                videoFrame = next(frame_processor(video, algorithm=algorithm))
                videoFrame = imutils.resize(videoFrame, height=640)
                videoframecount += 1
                videoFramesAll.append(videoFrame)
            else:
                videoFrame = videoFramesAll[videoframecount]
                videoframecount += 1

        if k == ord('e'):
            if hdframecount > 0:
                hdframecount -= 1
                hdFrame = hdFramesAll[hdframecount]
            else:
                hdFrame = hdFramesAll[hdframecount]

        if k == ord('w'):
            if videoframecount > 0:
                videoframecount -= 1
                videoFrame = videoFramesAll[videoframecount]
            else:
                videoFrame = videoFramesAll[videoframecount]

        # save current frames for the video comparison
        if k == ord('y'):
            cv2.imwrite('images/frameGrabs/{}_frame{}_{}.png'.format(baseName, videoframecount, algorithm), videoFrame)
            print('[INFO] All frames written.')

        # write text on each video frame
        videoVis = videoFrame.copy()

        cv2.putText(videoVis, '!CHECK! -> {}: {} / {}'.format(algorithm, videoframecount, lenVideo), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 255, 0), 2)
        cv2.putText(hdFrame, 'HD: {} / {}'.format(hdframecount, lenHD), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        # stack the video frames
        combined = np.hstack((videoVis, hdFrame))
        cv2.putText(combined, 'Controls: "d/e" - HD fwd/back | "s/w" - vid fwd/back | ESC - quit | "y" - save frame'.format(algorithm, videoframecount, lenVideo), (450, 620),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow('Output', combined)

        if k == 27:
            break


def frame_processor(videoFeed, videoName='', algorithm='exhsv'):
    frameShape = None
    gob = GreenOnBrown(algorithm=algorithm)
    while True:
        k = cv2.waitKey(1) & 0xFF
        ret, frame = videoFeed.read()

        if ret == False:
            frame = np.zeros(frameShape, dtype='uint8')

        if frameShape is None:
            frameShape = frame.shape

        if videoName == "hd":
            yield frame

        else:
            cnts, boxes, weedCentres, imageOut = gob.inference(frame, exgMin=29,
                                                                exgMax=200,
                                                                hueMin=30,
                                                                hueMax=92,
                                                                saturationMin=10,
                                                                saturationMax=250,
                                                                brightnessMin=60,
                                                                brightnessMax=250,
                                                                show_display=False,
                                                                minArea=10)

            yield imageOut
        if k == 27:
            videoFeed.stop()
            break


def size_analysis(directory, sample_number=10, save_directory=None):
    '''
    take a directory of videos, save all frames to a list, randomly sample X number of frames, run EXHSV algorithm that returns contour list
    iterate over each contour and save frame ID, contour ID, contour area, bbox area, calibrated area
    :param directory:
    :return:
    '''
    ### IMPORTANT ###
    # this sets the random state - random values won't change unless you change this number
    RANDOM_STATE = 42
    np.random.seed(RANDOM_STATE)
    #################

    ### ALSO IMPORTANT ###
    # based on bench calibration - changing this will change the calibrated area
    # structure: 'camera': (on_ground_width_in_mm / image_width_pixels) ** 2 = area of one pixel
    calibration_dictionary = {
        'ard': (964 / 416) ** 2,
        'hq1': (1125 / 640) ** 2,
        'hq2': (1125 / 416) ** 2,
        'v2': (1153 / 416) ** 2,
    }
    df_columns = ['video_name', 'camera', 'rep', 'speed', 'frame_id',
                  'contour_px_area', 'bbox_px_area', 'mm2_contour_area', 'mm2_bbox_area']

    df = pd.DataFrame(columns=df_columns)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for videoPath in tqdm(glob.iglob(directory + '\*.mp4')):
        video_name = os.path.basename(videoPath).split('.')[0]
        camera_name = video_name.split('-')[0].lower()
        rep = video_name.split('-')[1]
        speed = video_name.split('-')[2]

        cap = cv2.VideoCapture(videoPath)
        video_length = count_frames(videoPath, override=True) - 1

        gob = GreenOnBrown(algorithm='exhsv')

        # randomly sample frames
        for i in tqdm(range(sample_number)):

            randint = np.random.randint(0, video_length)
            cap.set(1, randint)
            ret, frame = cap.read()

            # uses same parameters as the above image analysis settings
            cnts, boxes, weedCentres, imageOut = gob.inference(frame.copy(), exgMin=29,
                                                                exgMax=200,
                                                                hueMin=30,
                                                                hueMax=92,
                                                                saturationMin=10,
                                                                saturationMax=250,
                                                                brightnessMin=60,
                                                                brightnessMax=250,
                                                                show_display=False,
                                                                minArea=-10)
            # cv2.imshow('Output', imageOut)
            # cv2.waitKey(10)
            # calculate and append the individual contour areas
            px_contour_area = []
            cal_contour_area = []
            px_bbox_area = []
            cal_bbox_area = []

            if save_directory is not None:
                save_frame = frame.copy()
                sample_thread = Thread(target=bounding_box_image_sample,
                                       args=[save_frame, boxes, save_directory, randint])
                sample_thread.start()

                whole_image_thread = Thread(target=whole_image_save,
                                            args=[imageOut, save_directory, randint])
                whole_image_thread.start()


            for c in cnts:
                c_px_area = cv2.contourArea(c)
                c_cal_area = c_px_area * calibration_dictionary[camera_name]
                px_contour_area.append(c_px_area)
                cal_contour_area.append(c_cal_area)

            for box in boxes:
                boxW = box[2]
                boxH = box[3]

                bbox_px_area = boxW * boxH
                bbox_cal_area = bbox_px_area * calibration_dictionary[camera_name]

                px_bbox_area.append(bbox_px_area)
                cal_bbox_area.append(bbox_cal_area)

            print(px_bbox_area)
            print("-----------------------")
            print(cal_bbox_area)
            frame_id = [randint for x in boxes]
            video_name_id = [video_name for x in boxes]
            camera_id = [camera_name for x in boxes]
            rep_id = [rep for x in boxes]
            speed_id = [speed for x in boxes]

            df2 = pd.DataFrame(list(zip(video_name_id, camera_id, rep_id, speed_id, frame_id,
                                        px_contour_area, px_bbox_area, cal_contour_area, cal_bbox_area)),
                               columns=df_columns)

            print(df2)
            df = df.append(df2)

    df.to_csv(r"logs\{}_size_analysis_rstate_{}.csv".format(datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
                                                                      RANDOM_STATE))
    time.sleep(2)

def blur_analysis(directory, csv_save_directory='logs', sample_number=10, im_save_directory=None, display=False,
                  use_brisque=False, use_blur_detector=False, use_fft=False):
    import utils.blur_algorithms as blur
    from utils.blur_algorithms import normalize_brightness

    if use_brisque:
        from brisque import BRISQUE
        iqa_obj = BRISQUE(url=False)

    if use_blur_detector:
        from blur_detector import detectBlur

    ### IMPORTANT ###
    # this sets the random state - random values won't change unless you change this number
    RANDOM_STATE = 42
    np.random.seed(RANDOM_STATE)
    #################

    df_columns = ['video_name', 'camera', 'rep', 'speed', 'frame_id',
                  'laplacian_blur', 'variance_of_gradient_blur', 'tenengrad_blur', 'entropy_blur', 'wavelet_blur', 'gradient_blur']
    if use_brisque:
        df_columns.append('brisque')

    if use_fft:
        df_columns.append('fft_blur')

    df = pd.DataFrame(columns=df_columns)

    for videoPath in tqdm(glob.iglob(directory + '\*.mp4')):
        blur_scores = {'laplacian_blur': [],
                       'variance_of_gradient_blur': [],
                       'tenengrad_blur': [],
                       'entropy_blur': [],
                       'wavelet_blur': [],
                       'gradient_blur': []}
        if use_brisque:
            blur_scores['brisque'] = []

        if use_fft:
            blur_scores['fft_blur'] = []

        video_name = os.path.basename(videoPath).split('.')[0]
        camera_name = video_name.split('-')[0].lower()
        rep = video_name.split('-')[1]
        speed = video_name.split('-')[2]

        cap = cv2.VideoCapture(videoPath)
        video_length = count_frames(videoPath, override=True) - 1

        # randomly sample frames
        for i in tqdm(range(sample_number)):
            scores = []
            randint = np.random.randint(0, video_length)
            cap.set(1, randint)
            ret, frame = cap.read()
            # if frame.shape[1] != 416:
            #     frame = cv2.resize(frame, (416, 320), interpolation=cv2.INTER_CUBIC)
            #     print('RESIZED', camera_name)

            if im_save_directory is not None:
                save_frame = frame.copy()

                whole_image_thread = Thread(target=whole_image_save,
                                            args=[save_frame, im_save_directory, randint])
                whole_image_thread.start()

            if use_blur_detector:
                gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

                blur_map = detectBlur(gray.copy(), downsampling_factor=4, num_scales=4, scale_start=2, num_iterations_RF_filter=3)
                cv2.imshow(f'{camera_name} | {speed}', frame.copy())
                cv2.imshow(f'{camera_name} | {speed} MAP', blur_map)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                blur_id = f"{randint}_blur"
                blur_image_thread = Thread(target=whole_image_save,
                                            args=[blur_map, im_save_directory, blur_id])
                blur_image_thread.start()

            # frame = normalize_brightness(frame.copy())
            for algo_name in blur_scores.keys():
                if algo_name == "brisque":
                    score = iqa_obj.score(frame.copy())
                    blur_scores[algo_name].append(score)
                    scores.append(score)

                elif algo_name == "fft_blur":
                    fft_func = getattr(blur, algo_name)
                    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
                    score = fft_func(gray, size=10)
                    blur_scores[algo_name].append(score)
                    scores.append(score)


                else:
                    blur_func = getattr(blur, algo_name)
                    score = blur_func(frame.copy())
                    blur_scores[algo_name].append(score)
                    scores.append(score)

            if use_brisque and use_fft:
                data = [video_name, camera_name, rep, speed, randint, scores[0], scores[1], scores[2], scores[3],
                        scores[4], scores[5], scores[6], scores[7]]


            elif use_brisque or use_fft:
                data = [video_name, camera_name, rep, speed, randint, scores[0], scores[1], scores[2], scores[3],
                        scores[4], scores[5], scores[6]]

            else:
                data = [video_name, camera_name, rep, speed, randint, scores[0], scores[1], scores[2], scores[3],
                        scores[4], scores[5]]

            df2 = pd.DataFrame([data], columns=df_columns)

            if display:
                display_frame = frame.copy()
                cv2.imshow(video_name, display_frame)
                cv2.waitKey(100)
                cv2.destroyAllWindows()

            df = df.append(df2)

    df.to_csv(os.path.join(csv_save_directory, f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_BLUR_rstate_{RANDOM_STATE}.csv"))
    time.sleep(2)


if __name__ == "__main__":
    # videoFile = r"videos/HQ2-1-5.avi"
    # hdFile = r"videos/ard-1-5.avi"
    #
    # single_frame_analysis(videoFile=videoFile,
    #                       HDFile=hdFile,
    #                       algorithm='exg')
    #
    # blur analysis
    directory = r"input_video_directory"
    csv_save_directory = "csv_output_directory"
    im_save_directory = False

    blur_analysis(directory=directory,
                  csv_save_directory=csv_save_directory,
                  sample_number=10,
                  im_save_directory=im_save_directory,
                  display=False,
                  use_brisque=True,
                  use_blur_detector=True,
                  use_fft=True)
