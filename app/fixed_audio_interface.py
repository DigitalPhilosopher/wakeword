import queue
import threading
from typing import Callable
from elevenlabs.conversational_ai.conversation import AudioInterface

class FixedAudioInterface(AudioInterface):
    INPUT_FRAMES_PER_BUFFER = 4000
    OUTPUT_FRAMES_PER_BUFFER = 1000

    def __init__(self):
        try:
            import pyaudio
        except ImportError:
            raise ImportError("To use FixedAudioInterface you must install pyaudio.")
        self.pyaudio = pyaudio
        self.recording = False
        self.input_callback = None
        self.output_queue: queue.Queue[bytes] = queue.Queue()
        self.should_stop = threading.Event()
        self.output_thread = threading.Thread(target=self._output_thread)

    def start(self, input_callback: Callable[[bytes], None]):
        self.input_callback = input_callback
        self.p = self.pyaudio.PyAudio()
        self.in_stream = self.p.open(
            format=self.pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            stream_callback=self._in_callback,
            frames_per_buffer=self.INPUT_FRAMES_PER_BUFFER,
            start=True,
        )
        self.out_stream = self.p.open(
            format=self.pyaudio.paInt16,
            channels=1,
            rate=16000,
            output=True,
            frames_per_buffer=self.OUTPUT_FRAMES_PER_BUFFER,
            start=True,
        )
        self.recording = True
        self.output_thread.start()

    def stop(self):
        self.should_stop.set()
        self.output_thread.join()
        self.in_stream.stop_stream()
        self.in_stream.close()
        self.out_stream.stop_stream()
        self.out_stream.close()
        self.p.terminate()

    def output(self, audio: bytes):
        self.output_queue.put(audio)

    def interrupt(self):
        try:
            while True:
                _ = self.output_queue.get(block=False)
        except queue.Empty:
            pass

    def _output_thread(self):
        while not self.should_stop.is_set():
            try:
                audio = self.output_queue.get(timeout=0.25)
                if self.recording:
                    self._pause_recording()
                self.out_stream.write(audio)
                if not self.recording:
                    self._resume_recording()
            except queue.Empty:
                pass

    def _pause_recording(self):
        if self.in_stream.is_active():
            self.in_stream.stop_stream()
            self.recording = False

    def _resume_recording(self):
        if not self.in_stream.is_active():
            self.in_stream.start_stream()
            self.recording = True

    def _in_callback(self, in_data, frame_count, time_info, status):
        if self.input_callback and self.recording:
            self.input_callback(in_data)
        return (None, self.pyaudio.paContinue)
