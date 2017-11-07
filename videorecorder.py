#!/usr/bin/env python3

import cv2
import time
import sys
from threading import Thread

class VideoRecorder(Thread):
    def __init__(self, filename, device_index=0, fps=25, frameSize=(640,480), format="MJPG", *args):
        super(VideoRecorder, self).__init__(*args, target=self.worker)
        self.frameSize = frameSize
        self.fps = fps
        self.keep_going=False
        if(filename == ""):
            return null
        self.filename = filename
        try:
            self.video_r=cv2.VideoCapture(device_index)
            self.video_w=cv2.VideoWriter(filename,
                                         cv2.VideoWriter_fourcc(*format),
                                         fps, frameSize)
        except:
            return null

    def stop(self):
        self.keep_going=False

    def worker(self):
        self.frame_counts=0
        # On limite la capture à 60sec (ou pas... à confirmer)
        self.keep_going=True
        while(self.frame_counts < 60*self.fps and self.keep_going != False):
            ret, video_frame = self.video_r.read()
            if(ret == True):
                #cv2.imshow("Frame", video_frame)
                video_frame = cv2.resize(video_frame, self.frameSize)
                self.video_w.write(video_frame)
                self.frame_counts+=1
                time.sleep(0.04)
            else:
                break

