import subprocess

from libqtile import widget as old_widget


class MyKeyboardLayout(old_widget.base.BackgroundPoll):
    def __init__(self, **config):
        super().__init__(**config)
        self.add_callbacks({"Button1": self.next_keyboard})

    def poll(self):
        return subprocess.check_output("xkb-switch").decode().strip()[:2].upper()

    def next_keyboard(self):
        subprocess.run(["xkb-switch", "-n"])
        self.tick()
