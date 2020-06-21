import ac
import functools

from constants import FC

class INFO_TYPE:
    GAPS = 0
    POSITIONS = 1

    # amount of types, used to cycle between them
    N_TYPES = 2

class LeaderboardRow:
    X_BASE = 5
    Y_BASE = 84
    ROW_HEIGHT = 37
    FASTEST_LAP_ID = -1
    HIGHLIGHT_ID = -1

    update_type = INFO_TYPE.GAPS # false for timings, true for positions lost or gained

    def __init__(self, leaderboardWindow, row):
        # SET SOME VARIABLES
        self.row = row
        px, py = LeaderboardRow.X_BASE, LeaderboardRow.Y_BASE + LeaderboardRow.ROW_HEIGHT * self.row # position of the names
        self.px = px
        self.py = py
        self.positionLabelId = 0 # 0 white, 1 red, 2 green - to prevent loading the labels all the time
        self.out = False
        self.pit = False

        self.highlightLabel = ac.addLabel(leaderboardWindow, "")
        ac.setPosition(self.highlightLabel, px-5, py-6)
        ac.setSize(self.highlightLabel, 258, LeaderboardRow.ROW_HEIGHT+1)
        ac.setBackgroundTexture(self.highlightLabel, FC.LEADERBOARD_PLAYER_HIGHLIGHT);
        ac.setVisible(self.highlightLabel, 0)

        # CREATE LABELS
        self.positionLabel = ac.addLabel(leaderboardWindow, "")
        ac.setPosition(self.positionLabel, px-4, py-7)
        ac.setSize(self.positionLabel, 38, 38)
        ac.setBackgroundTexture(self.positionLabel, FC.LEADERBOARD_POSITION_LABEL[self.row+1]);

        self.driverName = ac.getDriverName(row)
        self.driverId = row
        self.nameLabel = ac.addLabel(leaderboardWindow, self.driverName[:3].upper())
        ac.setPosition(self.nameLabel, px + 65, py+4)
        ac.setFontSize(self.nameLabel, 18)
        ac.setCustomFont(self.nameLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel, "left")

        self.teamLabel = ac.addLabel(leaderboardWindow, "")
        ac.setPosition(self.teamLabel, px + 47, py + 2)
        ac.setSize(self.teamLabel, 5, 18)
        if FC.TEAM_COLORS:
            try:
                ac.setBackgroundTexture(self.teamLabel, FC.TEAM_COLORS[self.driverName]);
            except KeyError:
                ac.log("%s:Name Missing in teams.txt %s" % (FC.APP_NAME, self.driverName))

        self.infoLabel = ac.addLabel(leaderboardWindow, "Interval")
        ac.setPosition(self.infoLabel, 250, py+4)
        ac.setFontSize(self.infoLabel, 18)
        ac.setCustomFont(self.infoLabel, FC.FONT_NAME, 0, 1)
        ac.setFontColor(self.infoLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.infoLabel, "right")

        self.positionChangeLabel = ac.addLabel(leaderboardWindow, "")
        ac.setPosition(self.positionChangeLabel, 205, py + 4)
        ac.setSize(self.positionChangeLabel, 18, 18)
        ac.setVisible(self.positionChangeLabel, 0)

        self.fastestLapLabel = ac.addLabel(leaderboardWindow, "")
        ac.setPosition(self.fastestLapLabel, px-41, py-6)
        ac.setSize(self.fastestLapLabel, 37, 37)
        ac.setBackgroundTexture(self.fastestLapLabel, FC.LEADERBOARD_FASTEST_LAP);
        ac.setVisible(self.fastestLapLabel, 0)

        self.focus_button = ac.addButton(leaderboardWindow, "")
        ac.setPosition(self.focus_button, px, py-7)
        ac.setSize(self.focus_button, 140, 38)
        self.on_click_focus_func = functools.partial(self.on_click_focus, row=self)
        ac.addOnClickedListener(self.focus_button, self.on_click_focus_func)
        ac.setBackgroundOpacity(self.focus_button, 0)
        ac.drawBorder(self.focus_button, 0)

    def update_name(self, id):
        if id == ac.getFocusedCar():
            ac.setVisible(self.highlightLabel, 1)
        else:
            ac.setVisible(self.highlightLabel, 0)
        if self.driverId == id: return # no need to update
        self.driverId = id
        self.driverName = ac.getDriverName(id)
        displayName = self.driverName.split()[-1][:3].upper()
        ac.setText(self.nameLabel, displayName)
        try:
            ac.setBackgroundTexture(self.teamLabel, FC.TEAM_COLORS[self.driverName])
        except KeyError:
            ac.log("%s:Name Missing in teams.txt %s" % (FC.APP_NAME, self.driverName))

    def update_time(self, time):
        if self.out or self.pit: return # no need to update
        if self.update_type == INFO_TYPE.GAPS:
            ac.setVisible(self.positionChangeLabel, 0)
            ac.setText(self.infoLabel, time)

    def update_positions(self, pos_diff):
        if self.out or self.pit: return # no need to update
        if self.update_type == INFO_TYPE.POSITIONS:
            ac.setVisible(self.positionChangeLabel, 1)
            if pos_diff > 0:
                ac.setBackgroundTexture(self.positionChangeLabel, FC.POSITION_GAINED)
            elif pos_diff < 0:
                ac.setBackgroundTexture(self.positionChangeLabel, FC.POSITION_LOST)
            else:
                ac.setBackgroundTexture(self.positionChangeLabel, FC.POSITION_MAINTAINED)
            ac.setText(self.infoLabel, str(abs(pos_diff)))

    def mark_red_position(self):
        if self.out or self.positionLabelId == 1: return # no need to update
        ac.setBackgroundTexture(self.positionLabel, FC.LEADERBOARD_POSITION_RED_LABEL[self.row+1])
        self.positionLabelId = 1

    def mark_green_position(self):
        if self.out or self.positionLabelId == 2: return # no need to update
        ac.setBackgroundTexture(self.positionLabel, FC.LEADERBOARD_POSITION_GREEN_LABEL[self.row+1])
        self.positionLabelId = 2

    def mark_white_position(self):
        if self.out or self.positionLabelId == 0: return # no need to update
        ac.setBackgroundTexture(self.positionLabel, FC.LEADERBOARD_POSITION_LABEL[self.row+1])
        self.positionLabelId = 0

    def mark_in(self):
        if not self.out: return
        self.out = False
        if LeaderboardRow.update_type == INFO_TYPE.POSITIONS:
            ac.setVisible(self.positionChangeLabel, 1)
        ac.setVisible(self.positionLabel, 1)
        ac.setPosition(self.teamLabel, self.px + 47, self.py + 2)
        ac.setPosition(self.nameLabel, self.px + 65, self.py+4)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontColor(self.infoLabel, 0.86, 0.86, 0.86, 1)

    def mark_out(self):
        if self.out: return
        self.out = True
        ac.setVisible(self.positionLabel, 0)
        ac.setVisible(self.positionChangeLabel, 0)
        ac.setPosition(self.teamLabel, self.px + 12, self.py + 2)
        ac.setPosition(self.nameLabel, self.px + 30, self.py+4)
        ac.setFontColor(self.nameLabel, .58,.53,.53, 1)
        ac.setText(self.infoLabel, "OUT")
        ac.setFontColor(self.infoLabel, .58,.53,.53, 1)

    def mark_enter_pits(self):
        if self.out or self.pit: return
        self.pit = True
        ac.setVisible(self.positionChangeLabel, 0)
        ac.setText(self.infoLabel, "IN PIT")
        ac.setFontColor(self.infoLabel, 0,.84,1, 1)

    def mark_left_pits(self):
        if self.out or not self.pit: return
        self.pit = False
        if LeaderboardRow.update_type == INFO_TYPE.POSITIONS:
            ac.setVisible(self.positionChangeLabel, 1)
        if self.driverId == 0:
            ac.setText(self.infoLabel, "Interval")
        ac.setFontColor(self.infoLabel, 0.86, 0.86, 0.86, 1)

    def mark_fastest_lap(self):
        if self.driverId == LeaderboardRow.FASTEST_LAP_ID:
            ac.setVisible(self.fastestLapLabel, 1)
        else:
            ac.setVisible(self.fastestLapLabel, 0)

    @staticmethod
    def on_click_focus(*args, row=None):
        if row:
            ac.focusCar(row.driverId)

