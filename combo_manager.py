from pico2d import get_time

class ComboManager:
    def __init__(self, retention=1.0, time_func=None):
        self.buffer = []  # list of (name, timestamp)
        self.retention = retention
        self._time = time_func or get_time

    def record_input(self, name, t=None):
        t = t if t is not None else self._time()
        self.buffer.append((name, t))
        self._cleanup()

    def consume_if_within(self, name, start_time, window, pre_window=0.0):
        self._cleanup()
        for i, (n, t) in enumerate(self.buffer):
            if n == name and (start_time - pre_window) <= t <= (start_time + window):
                del self.buffer[i]
                return True
        return False

    def _cleanup(self):
        cutoff = self._time() - self.retention
        self.buffer = [(n, t) for (n, t) in self.buffer if t >= cutoff]