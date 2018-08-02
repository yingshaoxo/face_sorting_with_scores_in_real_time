# coding:utf8
import cv2
import sys
import numpy as np

from keras.models import load_model
import face_recognition as fr


try:
    import pyscreenshot as ImageGrab
    import pyautogui
    import time
except Exception as e:
    print(e)


class BeautyDetector():
    def __init__(self):
        self.model = load_model("face_rank_model.h5")

    def camera_detect(self, device=0):
        self.camera = cv2.VideoCapture(device)
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if not self.camera.isOpened():
            print("Could not open camera")
            sys.exit()

        while True:
            res, frame = self.camera.read()

            frame = self.draw(frame)

            cv2.imshow("detection", frame)

            if cv2.waitKey(110) & 0xff == 27:
                break

    def screen_detect(self, record_box_size=600):
        record_box_size = record_box_size // 2

        face_size = 128

        while True:
            pos = pyautogui.position()
            mouse_x = pos[0]
            mouse_y = pos[1]
            left_top_x = mouse_x - record_box_size
            left_top_y = mouse_y - record_box_size
            right_bottom_x = mouse_x + record_box_size
            right_bottom_y = mouse_y + record_box_size

            frame = np.array(ImageGrab.grab(
                bbox=(left_top_x, left_top_y, right_bottom_x, right_bottom_y)))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = self.draw(frame)

            cv2.imshow("Beauty Detector", frame)

            if cv2.waitKey(110) & 0xff == 27:
                break

    def draw(self, frame):
        locations = fr.face_locations(frame)
        for location in locations:
            x1, x2 = location[3], location[1]
            y1, y2 = location[0], location[2]
            face = cv2.resize(frame[y1:y2, x1:x2, :], (128, 128))
            point = (x1 + (x2-x1)//3, y1 - 10)

            # face landmark feature points
            face_encoding = np.array(fr.face_encodings(face))
            if len(face_encoding) == 1:
                score = self.model.predict(face_encoding)[0][0]
                score = int(score/5 * 100)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(frame, str(score), point,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return frame


if __name__ == '__main__':
    detector = BeautyDetector()
    #detector.camera_detect(device=0)
    detector.screen_detect()
