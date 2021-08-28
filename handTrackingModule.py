import cv2 as cv
import mediapipe as mp
import math
import json


def rescale(video, scale_factor=0.5):
    width = int(video.shape[1]*scale_factor)
    height = int(video.shape[0]*scale_factor)
    return cv.resize(video, (width, height), interpolation=cv.INTER_AREA)


def change_res(width, height, video):
    video.set(3, width)
    video.set(4, height)


def getJson(fileName):
    with open(fileName, 'r') as f:
        data = json.load(f)

    list = data['info']
    dict = {}
    dict = list[0]
    return int(dict["target_fps"]), int(dict["smoothness"]), dict["url"]


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.mode, self.maxHands, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, image, draw=True):
        # convert the BGR image to RGB.
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        # Draw the hand annotations on the image.
        self.result = self.hands.process(imgRGB)
        imgRGB.flags.writeable = True
        image = cv.cvtColor(imgRGB, cv.COLOR_RGB2BGR)
        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
                # print(hand_landmarks.landmark)
                if draw:
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, handNo=0, draw=True):
        bbox = []
        xList = []
        yList = []
        self.lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(image, (cx, cy), 5, (255, 255, 255), cv.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
        return self.lmList, bbox

    def findDistance(self, p1, p2, img, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

    def fingersUp(self):
        fingers = []
        # thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(0)
        else:
            fingers.append(1)
        # other 4 fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
