import ac
from utils import get_image_size

from constants import FC

class DriverWidget:
    def __init__(self, appName):
        self.id = -1
        self.visible = True

        self.window = ac.newApp(appName)
        ac.setTitle(self.window, "")
        ac.drawBorder(self.window, 0)
        ac.setIconPosition(self.window, 0, -10000)
        ac.setSize(self.window, 300, 100)
        ac.setBackgroundOpacity(self.window, 0)

        self.backgroundTexture = ac.addLabel(self.window, "")
        w, h = get_image_size(FC.DRIVER_WIDGET_BACKGROUND)
        ac.setPosition(self.backgroundTexture, 0,0)
        ac.setSize(self.backgroundTexture, w, h)
        ac.setBackgroundTexture(self.backgroundTexture, FC.DRIVER_WIDGET_BACKGROUND);

        self.rolexLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.rolexLabel, 0, -72)
        ac.setSize(self.rolexLabel, 123, 70)
        ac.setBackgroundTexture(self.rolexLabel, FC.ROLEX_LOGO);

        self.positionLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.positionLabel, 3,3)
        ac.setSize(self.positionLabel, 62, 62)

        self.teamLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.teamLabel, 70, 10)
        ac.setSize(self.teamLabel, 6, 45)

        self.nameLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.nameLabel, 90, 4)
        ac.setFontSize(self.nameLabel, 26)
        ac.setCustomFont(self.nameLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel, "left")

        self.teamNameLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.teamNameLabel, 90, 35)
        ac.setFontSize(self.teamNameLabel, 20)
        ac.setCustomFont(self.teamNameLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.teamNameLabel, 0.66, 0.66, 0.66, 1)
        ac.setFontAlignment(self.teamNameLabel, "left")

        # TODO
        # self.driverNumberLabel = ac.addLabel(self.window, "")
    
    def hide(self):
        if not self.visible: return
        self.visible = False
        ac.setVisible(self.backgroundTexture, 0)
        ac.setVisible(self.rolexLabel, 0)
        ac.setVisible(self.positionLabel, 0)
        ac.setVisible(self.teamLabel, 0)
        ac.setVisible(self.nameLabel, 0)
        ac.setVisible(self.teamNameLabel, 0)

    def show(self, id, pos):
        ac.setBackgroundTexture(self.positionLabel, FC.LEADERBOARD_POSITION_LABEL[pos+1])
        ac.setVisible(self.positionLabel, 1)
        self.visible = True

        if self.id == id: return # dont update anything else
        self.id = id

        ac.setVisible(self.rolexLabel, 1)
        ac.setVisible(self.backgroundTexture, 1)
        ac.setVisible(self.nameLabel, 1)
        name = ac.getDriverName(id)
        ac.setText(self.nameLabel, name)

        if FC.TEAM_COLORS:
            try:
                ac.setBackgroundTexture(self.teamLabel, FC.TEAM_COLORS[name]);
                ac.setVisible(self.teamLabel, 1)
                ac.setVisible(self.teamNameLabel, 1)
                ac.setText(self.teamNameLabel, FC.TEAM_NAME[name])
            except KeyError:
                ac.console("%s:Name Missing in teams.txt %s" % (FC.APP_NAME, name))