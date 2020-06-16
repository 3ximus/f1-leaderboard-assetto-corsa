import ac
from utils import get_image_size, time_to_string

from constants import FC

class FastestLapBanner:

    def __init__(self, appName):
        self.timer = 0

        self.window = ac.newApp(appName)
        ac.setTitle(self.window, "")
        ac.drawBorder(self.window, 0)
        ac.setIconPosition(self.window, 0, -10000)
        ac.setSize(self.window, 367, 73)
        ac.setBackgroundOpacity(self.window, 0)

        self.fastestLapBanner = ac.addLabel(self.window, "")
        ac.setPosition(self.fastestLapBanner, 0, 0)
        w, h = get_image_size(FC.FASTEST_LAP_BANNER)
        ac.setSize(self.fastestLapBanner, w, h)
        ac.setBackgroundTexture(self.fastestLapBanner, FC.FASTEST_LAP_BANNER)

        self.fastestLapBackground = ac.addLabel(self.window, "")
        ac.setPosition(self.fastestLapBackground, w, 0)
        ac.setSize(self.fastestLapBackground, 400, h)
        ac.setBackgroundTexture(self.fastestLapBackground, FC.DRIVER_WIDGET_BACKGROUND);

        self.nameLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.nameLabel, w + 10, 11)
        ac.setFontSize(self.nameLabel, 22)
        ac.setCustomFont(self.nameLabel, FC.FONT_NAME, 0, 0)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel, "left")

        self.lastNameLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.lastNameLabel, w + 10, 37)
        ac.setFontSize(self.lastNameLabel, 28)
        ac.setCustomFont(self.lastNameLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.lastNameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.lastNameLabel, "left")

        self.timeLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.timeLabel, w + 385, 22)
        ac.setFontSize(self.timeLabel, 35)
        ac.setCustomFont(self.timeLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.timeLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.timeLabel, "right")

    def show(self, time, driver_name):
        ac.setText(self.nameLabel, driver_name.split()[0])
        ac.setText(self.lastNameLabel, driver_name.split()[-1].upper())
        ac.setText(self.timeLabel, time_to_string(time))
        ac.setVisible(self.fastestLapBackground, 1)
        ac.setVisible(self.fastestLapBanner, 1)
        ac.setVisible(self.nameLabel, 1)
        ac.setVisible(self.lastNameLabel, 1)
        ac.setVisible(self.timeLabel, 1)
        self.timer = FC.FASTEST_LAP_DISPLAY_TIME

    def hide(self):
        if self.timer > 0: return
        ac.setVisible(self.fastestLapBackground, 0)
        ac.setVisible(self.fastestLapBanner, 0)
        ac.setVisible(self.nameLabel, 0)
        ac.setVisible(self.lastNameLabel, 0)
        ac.setVisible(self.timeLabel, 0)
