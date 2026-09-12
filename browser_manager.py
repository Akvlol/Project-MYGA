from pathlib import Path
import subprocess
import time

class Browser:

    BROWSER = "/usr/bin/brave"
    PORT = 9222
    WM_CLASS = "ToNhoCauLam_YH"

    def __init__(self):
        self.profile = Path(__file__).parent.parent / "browser" / "profile"
        self.process = None

    def start(self):
        if self.process is not None:
            return
        self.process = subprocess.Popen([self.BROWSER,
                                         f"--user-data-dir={self.profile}",
                                         f'--remote-debugging-port={self.PORT}',
                                         f'--remote-allow-origins=http://127.0.0.1:{self.PORT}',
                                         "--autoplay-policy=no-user-gesture-required",
                                         f"--class={self.WM_CLASS}",
                                         "https://www.youtube.com/"],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)
        time.sleep(3)
        subprocess.run(
            f"kdotool search --class {self.WM_CLASS} windowminimize",
            shell=True
        )

        print("Browser started.")

    def stop(self):
        if self.process is None:
            return
        self.process.terminate()
        self.process = None
        print("Browser stopped.")