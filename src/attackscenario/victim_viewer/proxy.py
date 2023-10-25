import os
import threading
import time
from subprocess import Popen, PIPE
import victim_viewer.settings as se

class ProxyThread:
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._proxy, args=(self._stop_event,))
        self._process = None
        self._stdout = ""
        self._stderr = ""
        self._port = "8899"

    def __enter__(self):
        self._thread.start()
        time.sleep(5)

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"exc_type: {exc_type}")
        print(f"exc_value: {exc_value}")
        print(f"traceback: {traceback}")
        self._stop_event.set()
        self._thread.join()

        if self._process:
            self._stdout, self._stderr = self._process.communicate()

        else:
            print("[-]Thread is not NONE!")
        print("JOIN COMPLETED")

    def _proxy(self, stop_event):
        try:
            self._process = Popen(
                [se.PYPATH, "-m" "proxy", "--port", self._port], cwd=se.PROXY_PY, stdout=PIPE, stderr=PIPE
            )

            while not stop_event.is_set():
                time.sleep(1)

            os.system(f"kill {self._process.pid}")

        except Exception as ex:
            print(ex)
