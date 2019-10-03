#!/usr/bin/env python3
from multiprocessing import Queue
from TimeSync import TimeSync
from FrameReader import FrameReader
from FrameProcessor import FrameProcessor


update_frequency = 4  # Times a second
frame_queue = Queue(120 * update_frequency)  # 2 minutes worth of frames queued

frame_reader = FrameReader("./bbb_sunflower_1080p_60fps_normal.mp4", update_frequency, frame_queue)
frame_reader.start()

time_sync = TimeSync(update_frequency)

frame_processor = FrameProcessor(frame_queue)
frame_processor.start()


def on_time_sync_change(time):
    frame_reader.set_frame_time(time)


def on_time_sync_interval(time):
    frame = frame_reader.time_to_frame(time)
    dominant = frame_processor.get_frame_colour(frame)
    print("Frame: " + str(frame) + ", Colour: " + str(dominant))
    #if dominant is not None:

        # hue_sync.set_colour(dominant)


time_sync.change_callback(on_time_sync_change)
time_sync.interval_callback(on_time_sync_interval)

time_sync.play()
