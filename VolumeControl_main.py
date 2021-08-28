from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2 as cv
import time
import numpy as np
import handTrackingModule as htm


target_fps, smoothness, url = htm.getJson('config.json')
prev_time = time.time()

# distance between the fingers
minDist = 40  # 25 na pcju
maxDist = 400  # 170

# volume init
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

volBar = 400
volPer = 0
area = 0

cap = cv.VideoCapture(url)
detector = htm.HandDetector(detectionConfidence=0.8, maxHands=1)


def fps(prev_time, target_fps):
    curr_time = time.time()  # so now we have time after processing
    diff = curr_time - prev_time  # frame took this much time to process and render
    # if we finished early, wait the remaining time to desired fps, else wait 0 ms!
    delay = max(1.0/target_fps - diff, 0)
    prev_time = curr_time
    return prev_time, delay


if __name__ == "__main__":
    starttime = time.time()
    while True:
        prev_time, delay = fps(prev_time, target_fps)
        time.sleep(delay)
        success, image = cap.read()
        # print(image)
        print(success)
        print()
        if image is not None:
            # Find Hand
            image = detector.findHands(image)
            lmList, bbox = detector.findPosition(image, draw=False)
            if len(lmList) != 0:
                # Filter based on size
                area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
                if 950 < area < 3250:
                    cv.rectangle(
                        image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 255, 255), 2)

                    # Find Distance between index and Thumb
                    length, img, lineInfo = detector.findDistance(4, 8, image)

                    # Convert Volume
                    #print(minDist, maxDist)
                    vol = np.interp(
                        length, [minDist, maxDist], [minVol, maxVol])
                    volBar = np.interp(length, [minDist, maxDist], [397, 153])
                    volPer = np.interp(length, [minDist, maxDist], [0, 100])

                    # Reduce resol to make it smoother
                    volPer = smoothness * round(volPer/smoothness)

                    # Check fingers up
                    fingers = detector.fingersUp()

                    # if pinky is down set volume
                    if not fingers[4]:
                        volume.SetMasterVolumeLevelScalar(volPer/100, None)
                        cv.circle(
                            image, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv.FILLED)
                        # draw
                else:
                    pass

            cv.rectangle(image, (50, 150), (85, 400), (0, 0, 0), 3)
            cv.rectangle(image, (53, int(volBar)), (82, 397),
                         (255, 255, 255), cv.FILLED)
            cv.putText(image, '{}%'.format(int(volPer)), (35, 430),
                       cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
            cv.putText(image, 'Vol Set: {}'.format(round(volume.GetMasterVolumeLevelScalar(
            )*100)), (440, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

        try:
            cv.imshow('OpenCV-Volume Control', image)
        except(cv.error):
            print("There seems to be an error -> check for internet error")

        if (cv.waitKey(5) & 0xFF == 27):
            break

cv.destroyAllWindows()
