from threading import Thread
import cv2


class FrameReader(object):
    def __init__(self, file, interval, frame_queue):
        self._video = cv2.VideoCapture(file)
        self._fps = self._video.get(cv2.CAP_PROP_FPS)
        self._interval = int(self._fps / interval)
        self._frame_queue = frame_queue
        self._frame_override = None
        self._frames = set()
        self.set_frame_time()

    def __del__(self):
        self._video.release()

    def _process_video(self):
        while True:
            if self._frame_override is not None:
                self._video.set(cv2.CAP_PROP_POS_FRAMES, self._frame_override)
                self._frame_override = None

                # Empty out the processing queue :/
                while not self._frame_queue.empty():
                    self._frame_queue.get()

            frame_position = self._video.get(cv2.CAP_PROP_POS_FRAMES)
            has_frame, frame = self._video.read()
            if has_frame:
                if frame_position % self._interval == 0 and frame_position not in self._frames:
                    self._frame_queue.put((frame_position, frame))
                    self._frames.add(frame_position)

                next_frame_position = frame_position + self._interval
                self._video.set(cv2.CAP_PROP_POS_FRAMES, next_frame_position)
            else:
                break

    def time_to_frame(self, time):
        frame = time * self._fps
        return frame - (frame % self._interval)

    def set_frame_time(self, time=0):
        frame = self.time_to_frame(time + 2)
        self._frame_override = frame

    def start(self):
        Thread(target=self._process_video).start()
