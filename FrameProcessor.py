from multiprocessing import Process, Manager, cpu_count
import numpy as np


class FrameProcessor(object):
    def __init__(self, frame_queue):
        manager = Manager()

        self._frame_queue = frame_queue
        self._frames = manager.dict()
        self._number_of_processes = cpu_count()
        self._workers = []

    @staticmethod
    def _dominant_colour(frame):
        a2d = frame.reshape(-1, frame.shape[-1])
        col_range = (256, 256, 256)  # generically : a2D.max(0)+1
        a1d = np.ravel_multi_index(a2d.T, col_range)
        dominant = np.unravel_index(np.bincount(a1d).argmax(), col_range)
        return dominant

    def _process_frames(self, process_id, frames):
        while True:
            if not self._frame_queue.empty():
                frame_position, frame = self._frame_queue.get()
                print("Calculating: " + str(frame_position))
                frames[frame_position] = self._dominant_colour(frame)

    def get_frame_colour(self, frame):
        if frame in self._frames:
            return self._frames[frame]
        else:
            return None

    def start(self):
        self._workers = [Process(target=self._process_frames, args=(i, self._frames,))
                         for i in range(self._number_of_processes)]

        for w in self._workers:
            w.start()
