import ac
from utils import get_image_size

from constants import FC

class DriverWidget:
    extended = False
    def __init__(self, appName):
        self.id = -1
        self.visible = True
        self.extended = False
        self.position = -1

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

        self.numberLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.numberLabel, w - 63, 7)
        ac.setSize(self.numberLabel, 55, 55)

        self.button = ac.addButton(self.window, "")
        ac.setPosition(self.button, 0, 0)
        ac.setSize(self.button, w, h)
        ac.addOnClickedListener(self.button, self.toogle_extended)
        ac.setBackgroundOpacity(self.button, 0)
        ac.drawBorder(self.button, 0)

        self.extendedBackgroundTexture = ac.addLabel(self.window, "")
        ac.setPosition(self.extendedBackgroundTexture, 0,h)
        w, h = get_image_size(FC.DRIVER_WIDGET_EXTENDED_BACKGROUND)
        ac.setSize(self.extendedBackgroundTexture, w, h)
        ac.setBackgroundTexture(self.extendedBackgroundTexture, FC.DRIVER_WIDGET_EXTENDED_BACKGROUND);

        self.startedTextLabel = ac.addLabel(self.window, "STARTED")
        ac.setPosition(self.startedTextLabel, 70, 130)
        ac.setFontSize(self.startedTextLabel, 18)
        ac.setCustomFont(self.startedTextLabel, FC.FONT_NAME, 0, 0)
        ac.setFontColor(self.startedTextLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.startedTextLabel, "center")

        self.placesTextLabel = ac.addLabel(self.window, "PLACES")
        ac.setPosition(self.placesTextLabel, 175, 130)
        ac.setFontSize(self.placesTextLabel, 18)
        ac.setCustomFont(self.placesTextLabel, FC.FONT_NAME, 0, 0)
        ac.setFontColor(self.placesTextLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.placesTextLabel, "center")

        self.tyreTextLabel = ac.addLabel(self.window, "TYRES")
        ac.setPosition(self.tyreTextLabel, 285, 130)
        ac.setFontSize(self.tyreTextLabel, 18)
        ac.setCustomFont(self.tyreTextLabel, FC.FONT_NAME, 0, 0)
        ac.setFontColor(self.tyreTextLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.tyreTextLabel, "center")

        self.pitStopTextLabel = ac.addLabel(self.window, "PIT STOPS")
        ac.setPosition(self.pitStopTextLabel, 395, 130)
        ac.setFontSize(self.pitStopTextLabel, 18)
        ac.setCustomFont(self.pitStopTextLabel, FC.FONT_NAME, 0, 0)
        ac.setFontColor(self.pitStopTextLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.pitStopTextLabel, "center")

        self.startedLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.startedLabel, 70, 80)
        ac.setFontSize(self.startedLabel, 34)
        ac.setCustomFont(self.startedLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.startedLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.startedLabel, "center")

        self.placesLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.placesLabel, 175, 80)
        ac.setFontSize(self.placesLabel, 34)
        ac.setCustomFont(self.placesLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.placesLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.placesLabel, "center")

        self.placesIconLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.placesIconLabel, 135, 84)
        ac.setSize(self.placesIconLabel, 35, 35)

        self.tyreLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.tyreLabel, 263, 78)
        ac.setSize(self.tyreLabel, 46, 46)

        self.pitStopLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.pitStopLabel, 395, 80)
        ac.setFontSize(self.pitStopLabel, 34)
        ac.setCustomFont(self.pitStopLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.pitStopLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.pitStopLabel, "center")

        ac.setVisible(self.extendedBackgroundTexture, 0)
        ac.setVisible(self.startedLabel, 0)
        ac.setVisible(self.startedTextLabel, 0)
        ac.setVisible(self.placesLabel, 0)
        ac.setVisible(self.placesTextLabel, 0)
        ac.setVisible(self.placesIconLabel, 0)
        ac.setVisible(self.tyreTextLabel, 0)
        ac.setVisible(self.tyreLabel, 0)
        ac.setVisible(self.pitStopTextLabel, 0)
        ac.setVisible(self.pitStopLabel, 0)

    def hide(self):
        if not self.visible: return
        self.visible = False
        ac.setVisible(self.backgroundTexture, 0)
        ac.setVisible(self.rolexLabel, 0)
        ac.setVisible(self.positionLabel, 0)
        ac.setVisible(self.numberLabel, 0)
        ac.setVisible(self.teamLabel, 0)
        ac.setVisible(self.nameLabel, 0)
        ac.setVisible(self.teamNameLabel, 0)

        if DriverWidget.extended:
            ac.setVisible(self.extendedBackgroundTexture, 0)
            ac.setVisible(self.startedLabel, 0)
            ac.setVisible(self.startedTextLabel, 0)
            ac.setVisible(self.placesLabel, 0)
            ac.setVisible(self.placesTextLabel, 0)
            ac.setVisible(self.placesIconLabel, 0)
            ac.setVisible(self.tyreTextLabel, 0)
            ac.setVisible(self.tyreLabel, 0)
            ac.setVisible(self.pitStopTextLabel, 0)
            ac.setVisible(self.pitStopLabel, 0)

    def show(self, id, pos, starting_position, tyres, pit_stops):
        ac.setBackgroundTexture(self.positionLabel, FC.LEADERBOARD_POSITION_LABEL[pos+1])
        ac.setVisible(self.positionLabel, 1)
        self.visible = True

        if self.extended:
            places = starting_position - (pos+1)
            if places == 0:
                ac.setFontColor(self.placesLabel, 0.86, 0.86, 0.86, 1)
                ac.setVisible(self.placesIconLabel, 0)
                ac.setPosition(self.placesLabel, 175, 80)
            elif places > 0:
                ac.setFontColor(self.placesLabel, 0.3, .85, .28, 1) # green
                ac.setBackgroundTexture(self.placesIconLabel, FC.POSITION_GAINED)
                ac.setPosition(self.placesLabel, 190, 80)
                ac.setVisible(self.placesIconLabel, 1)
            elif places < 0:
                ac.setFontColor(self.placesLabel, 0.97, .25, .25, 1) # red
                ac.setBackgroundTexture(self.placesIconLabel, FC.POSITION_LOST)
                ac.setPosition(self.placesLabel, 190, 80)
                ac.setVisible(self.placesIconLabel, 1)
            ac.setText(self.placesLabel, str(abs(places)))

        if self.id != id:
            ac.setVisible(self.rolexLabel, 1)
            ac.setVisible(self.backgroundTexture, 1)
            ac.setVisible(self.nameLabel, 1)
            name = ac.getDriverName(id)
            sName = name.split()
            ac.setText(self.nameLabel, "%s %s" %(sName[0], sName[-1].upper()))

            if FC.TEAM_COLORS:
                try:
                    ac.setBackgroundTexture(self.teamLabel, FC.TEAM_COLORS[name]);
                    ac.setText(self.teamNameLabel, FC.TEAM_NAME[name])
                    ac.setBackgroundTexture(self.numberLabel, FC.NUMBER_TAGS[name]);
                    ac.setVisible(self.teamLabel, 1)
                    ac.setVisible(self.teamNameLabel, 1)
                    ac.setVisible(self.numberLabel, 1)
                except KeyError:
                    ac.console("%s:Name Missing in teams.txt %s" % (FC.APP_NAME, name))

        if self.extended != DriverWidget.extended or self.id != id:
            self.extended = DriverWidget.extended
            if self.extended:
                ac.setText(self.pitStopLabel, str(pit_stops))
                u = str(starting_position)[-1]
                if u == "1": subscript = "st"
                if u == "2": subscript = "nd"
                if u == "3": subscript = "rd"
                else: subscript = "th"
                ac.setText(self.startedLabel, str(starting_position) + subscript)
                ac.setBackgroundTexture(self.tyreLabel, FC.TYRE_BASE_NAME + tyres + ".png");

                ac.setBackgroundTexture(self.backgroundTexture, FC.DRIVER_WIDGET_BACKGROUND_ALTERNATE)
                ac.setVisible(self.extendedBackgroundTexture, 1)
                ac.setVisible(self.startedLabel, 1)
                ac.setVisible(self.startedTextLabel, 1)
                ac.setVisible(self.placesLabel, 1)
                ac.setVisible(self.placesTextLabel, 1)
                ac.setVisible(self.tyreTextLabel, 1)
                ac.setVisible(self.tyreLabel, 1)
                ac.setVisible(self.pitStopTextLabel, 1)
                ac.setVisible(self.pitStopLabel, 1)
            else:
                ac.setBackgroundTexture(self.backgroundTexture, FC.DRIVER_WIDGET_BACKGROUND)
                ac.setVisible(self.extendedBackgroundTexture, 0)
                ac.setVisible(self.startedLabel, 0)
                ac.setVisible(self.startedTextLabel, 0)
                ac.setVisible(self.placesLabel, 0)
                ac.setVisible(self.placesTextLabel, 0)
                ac.setVisible(self.placesIconLabel, 0)
                ac.setVisible(self.tyreTextLabel, 0)
                ac.setVisible(self.tyreLabel, 0)
                ac.setVisible(self.pitStopTextLabel, 0)
                ac.setVisible(self.pitStopLabel, 0)
        self.id = id
    
    @staticmethod
    def toogle_extended(*args):
        ac.console("HERE")
        DriverWidget.extended = not DriverWidget.extended
