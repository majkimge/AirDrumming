import math
import os
import cv2
import numpy as np
import imutils
from Instrument import Instrument
import pygame


class DrumController:

    def __init__(self):
        pygame.mixer.init()
        self.circ_buff_size = 10
        self.circ_buff_green = [(0.0, 0.0)] * self.circ_buff_size
        self.circ_buff_blue = [(0.0, 0.0)] * self.circ_buff_size
        self.circ_buff = [self.circ_buff_green, self.circ_buff_blue]
        self.circ_buff_ite = [0, 0]
        self.lower_colors = [(36, 25, 25), (90, 100, 100)]
        self.upper_colors = [(100, 255, 255), (110, 255, 255)]
        self.speed_cap = 100
        self.speed_frame_number = 2

    def update_buff(self, x, y, stick_id):
        self.circ_buff[stick_id][self.circ_buff_ite[stick_id]] = (x, y)
        self.circ_buff_ite[stick_id] = (self.circ_buff_ite[stick_id] + 1) % self.circ_buff_size

    def get_previous_center(self, num_of_frames_before, stick_id):
        correct_index = (self.circ_buff_ite[stick_id] - (
                num_of_frames_before + 1) % self.circ_buff_size + self.circ_buff_size) % self.circ_buff_size

        return self.circ_buff[stick_id][correct_index]

    def speed_of_hit(self, num_of_frames, stick_id):
        dist = self.get_previous_center(0, stick_id)[1] - self.get_previous_center(num_of_frames, stick_id)[1]
        return dist / num_of_frames

    def nothing(x):
        # any operation
        pass

    def start(self):
        cap = cv2.VideoCapture(0)
        instruments = []
        dirname = os.path.dirname(__file__)
        hi_hat_filename = os.path.join(dirname, 'sounds/hi_hat.ogg')
        snare_filename = os.path.join(dirname, 'sounds/snare.ogg')
        crash_filename = os.path.join(dirname, 'sounds/crash.ogg')
        floor_tom_filename = os.path.join(dirname, 'sounds/floor_tom.ogg')
        medium_tom_filename = os.path.join(dirname, 'sounds/medium_tom.ogg')
        high_tom_filename = os.path.join(dirname, 'sounds/high_tom.ogg')

        hi_hat = Instrument(hi_hat_filename, (0, 250), (100, 500), 0)
        snare = Instrument(snare_filename, (110, 350), (200, 500), 1)
        crash_cymbal = Instrument(crash_filename, (550, 200), (650,400), 2)
        floor_tom = Instrument(floor_tom_filename, (430, 380), (530, 500), 3)
        medium_tom = Instrument(medium_tom_filename, (320, 200), (440, 300), 4)
        high_tom = Instrument(high_tom_filename, (200, 200), (320, 300), 5)
        instruments.append(hi_hat)
        instruments.append(snare)
        instruments.append(crash_cymbal)
        instruments.append(floor_tom)
        instruments.append(medium_tom)
        instruments.append(high_tom)
        appear = False

        while True:
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            for stick_index in range(2):
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_green = np.array([36, 25, 25])
                upper_green = np.array([70, 255, 255])

                mask = cv2.inRange(hsv, self.lower_colors[stick_index], self.upper_colors[stick_index])
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.erode(mask, kernel)

                # Contours detection
                if int(cv2.__version__[0]) > 3:
                    # Opencv 4.x.x
                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                else:
                    # Opencv 3.x.x
                    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                # cnts = imutils.grab_contours(contours)

                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                    x = approx.ravel()[0]
                    y = approx.ravel()[1]
                    # print(approx)

                    M = cv2.moments(cnt)
                    cX = 0
                    cY = 0
                    if M["m00"] > 0.001:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                    # print(M)

                    if area > 500:
                        cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                        if M["m00"] > 0.001 and len(approx) > 5:
                            centre = (cX, cY)
                            cv2.circle(frame, centre, 7, (255, 255, 255), -1)
                            self.update_buff(cX, cY, stick_index)
                            for instrument in instruments:
                                if instrument.is_inside(cX, cY):
                                    if not instrument.inside_info()[stick_index]:
                                        speed = self.speed_of_hit(self.speed_frame_number, stick_index)
                                        vol = (max(0, (speed - 20) / self.speed_cap) / 2)
                                        if self.get_previous_center(1, stick_index)[1] < cY and speed > 10.0:
                                            instrument.play(vol)
                                        instrument.enter(stick_index)
                                        # print(self.get_previous_center(2))
                                        # print(self.get_previous_center(1))
                                        # print(self.get_previous_center(0))
                                        # print(self.speed_of_hit(2))
                                        # print("________")
                                else:
                                    if instrument.inside_info()[stick_index]:
                                        instrument.leave(stick_index)
                            appear = True
                cv2.imshow("Mask" + str(stick_index), mask)

            for instrument in instruments:
                cv2.rectangle(frame, instrument.corners()[0], instrument.corners()[1], (200, 200, 200), 2)

            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    dc = DrumController()
    dc.start()
