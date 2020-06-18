import ac
from utils import get_image_size, time_to_string

from constants import FC

class DriverComparisonWidget:
    def __init__(self, appName):
        self.id1 = -1
        self.id2 = -1
        self.visible = True

        self.window = ac.newApp(appName)
        ac.setTitle(self.window, "")
        ac.drawBorder(self.window, 0)
        ac.setIconPosition(self.window, 0, -10000)
        ac.setSize(self.window, 300, 100)
        ac.setBackgroundOpacity(self.window, 0)

        self.backgroundTexture = ac.addLabel(self.window, "")
        ac.setPosition(self.backgroundTexture, 0,0)
        ac.setSize(self.backgroundTexture, 800, 50)
        ac.setBackgroundTexture(self.backgroundTexture, FC.DRIVER_WIDGET_BACKGROUND_ALTERNATE);

        self.extendedBackgroundTexture = ac.addLabel(self.window, "")
        ac.setPosition(self.extendedBackgroundTexture, 0, 50)
        ac.setSize(self.extendedBackgroundTexture, 800, 92)
        ac.setBackgroundTexture(self.extendedBackgroundTexture, FC.LEADERBOARD_BACKGROUND);

        self.rolexLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.rolexLabel, 0, -72)
        ac.setSize(self.rolexLabel, 123, 70)
        ac.setBackgroundTexture(self.rolexLabel, FC.ROLEX_LOGO);

        self.speedometerIconLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.speedometerIconLabel, 378, 3)
        ac.setSize(self.speedometerIconLabel, 44, 44)
        ac.setBackgroundTexture(self.speedometerIconLabel, FC.SPEEDOMETER_ICON);

        # ==========================================

        self.positionLabel1 = ac.addLabel(self.window, "")
        ac.setPosition(self.positionLabel1, 3,3)
        ac.setSize(self.positionLabel1, 44, 44)

        self.positionLabel2 = ac.addLabel(self.window, "")
        ac.setPosition(self.positionLabel2, 433,3)
        ac.setSize(self.positionLabel2, 44, 44)

        # ==========================================

        self.teamLabel1 = ac.addLabel(self.window, "")
        ac.setPosition(self.teamLabel1, 56, 10)
        ac.setSize(self.teamLabel1, 6, 27)

        self.teamLabel2 = ac.addLabel(self.window, "")
        ac.setPosition(self.teamLabel2, 486, 10)
        ac.setSize(self.teamLabel2, 6, 27)

        # ==========================================

        self.nameLabel1 = ac.addLabel(self.window, "")
        ac.setPosition(self.nameLabel1, 74, 15)
        ac.setFontSize(self.nameLabel1, 25)
        ac.setCustomFont(self.nameLabel1, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel1, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel1, "left")

        self.nameLabel2 = ac.addLabel(self.window, "")
        ac.setPosition(self.nameLabel2, 504, 15)
        ac.setFontSize(self.nameLabel2, 25)
        ac.setCustomFont(self.nameLabel2, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel2, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel2, "left")

        # ==========================================

        self.carLabel1 = ac.addLabel(self.window, "")
        ac.setPosition(self.carLabel1, 88, 55)
        ac.setSize(self.carLabel1, 195, 85)

        self.carLabel2 = ac.addLabel(self.window, "")
        ac.setPosition(self.carLabel2, 507, 55)
        ac.setSize(self.carLabel2, 195, 85)

        # ==========================================

        self.gapsIconLabelL = ac.addLabel(self.window, "")
        ac.setPosition(self.gapsIconLabelL, 310, 110)
        ac.setSize(self.gapsIconLabelL, 40, 6)
        ac.setBackgroundTexture(self.gapsIconLabelL, FC.GAPS);

        self.gapsIconLabelR = ac.addLabel(self.window, "")
        ac.setPosition(self.gapsIconLabelR, 454, 110)
        ac.setSize(self.gapsIconLabelR, 40, 6)
        ac.setBackgroundTexture(self.gapsIconLabelR, FC.GAPS);

        self.gapLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.gapLabel, 400, 68)
        ac.setFontSize(self.gapLabel, 40)
        ac.setCustomFont(self.gapLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.gapLabel, 0.94, 0.87, 0.17, 1)
        ac.setFontAlignment(self.gapLabel, "center")

        self.secondsLabel = ac.addLabel(self.window, "SECONDS")
        ac.setPosition(self.secondsLabel, 400, 107)
        ac.setFontSize(self.secondsLabel, 16)
        ac.setCustomFont(self.secondsLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.secondsLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.secondsLabel, "center")

    def hide(self):
        if not self.visible: return
        self.visible = False
        ac.setVisible(self.backgroundTexture, 0)
        ac.setVisible(self.extendedBackgroundTexture, 0)
        ac.setVisible(self.rolexLabel, 0)
        ac.setVisible(self.speedometerIconLabel, 0)
        ac.setVisible(self.positionLabel1, 0)
        ac.setVisible(self.positionLabel2, 0)
        ac.setVisible(self.teamLabel1, 0)
        ac.setVisible(self.teamLabel2, 0)
        ac.setVisible(self.nameLabel1, 0)
        ac.setVisible(self.nameLabel2, 0)
        ac.setVisible(self.carLabel1, 0)
        ac.setVisible(self.carLabel2, 0)
        ac.setVisible(self.gapsIconLabelL, 0)
        ac.setVisible(self.gapsIconLabelR, 0)
        ac.setVisible(self.gapLabel, 0)
        ac.setVisible(self.secondsLabel, 0)

    def show(self, id1, pos1, id2, pos2, time_gap):
        ac.setBackgroundTexture(self.positionLabel1, FC.LEADERBOARD_POSITION_LABEL[pos1+1])
        ac.setBackgroundTexture(self.positionLabel2, FC.LEADERBOARD_POSITION_LABEL[pos2+1])
        ac.setText(self.gapLabel, time_to_string(time_gap))

        ac.setVisible(self.rolexLabel, 1)
        ac.setVisible(self.speedometerIconLabel, 1)
        ac.setVisible(self.backgroundTexture, 1)
        ac.setVisible(self.extendedBackgroundTexture, 1)
        ac.setVisible(self.positionLabel1, 1)
        ac.setVisible(self.positionLabel2, 1)
        ac.setVisible(self.nameLabel1, 1)
        ac.setVisible(self.nameLabel2, 1)
        ac.setVisible(self.carLabel1, 1)
        ac.setVisible(self.carLabel2, 1)
        ac.setVisible(self.gapsIconLabelL, 1)
        ac.setVisible(self.gapsIconLabelR, 1)
        ac.setVisible(self.gapLabel, 1)
        ac.setVisible(self.secondsLabel, 1)

        if self.id1 != id1 and self.id2 != id2:
            name1 = ac.getDriverName(id1)
            ac.setText(self.nameLabel1, name1.split()[-1].upper())
            if FC.TEAM_COLORS:
                try:
                    ac.setBackgroundTexture(self.teamLabel1, FC.TEAM_COLORS[name1]);
                    ac.setBackgroundTexture(self.carLabel1, FC.CARS[name1]);
                    ac.setVisible(self.teamLabel1, 1)
                    ac.setVisible(self.carLabel1, 1)
                except KeyError:
                    ac.log("%s:Name Missing in teams.txt" % (FC.APP_NAME))

        if self.id2 != id2:
            name2 = ac.getDriverName(id2)
            ac.setText(self.nameLabel2, name2.split()[-1].upper())
            if FC.TEAM_COLORS:
                try:
                    ac.setBackgroundTexture(self.teamLabel2, FC.TEAM_COLORS[name2]);
                    ac.setBackgroundTexture(self.carLabel2, FC.CARS[name2]);
                    ac.setVisible(self.teamLabel2, 1)
                    ac.setVisible(self.carLabel2, 1)
                except KeyError:
                    ac.log("%s:Name Missing in teams.txt" % (FC.APP_NAME))

        self.id1 = id1
        self.id2 = id2
        self.visible = True
