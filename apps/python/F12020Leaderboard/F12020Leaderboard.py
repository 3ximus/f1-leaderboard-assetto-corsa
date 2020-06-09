import sys
import re
import os
import functools

import imghdr
import struct

import ac
import acsys

import ctypes
from ctypes import wintypes

from sim_info_lib.sim_info import info

APP_NAME = "F12020Leaderboard"
FONT_NAME = "Orbitron"

# IMAGES
LEADERBOARD_POSITION_LABEL = ["apps/python/%s/ui/normalized/positions/%d.png" % (APP_NAME, n) for n in range(20)]
LEADERBOARD_POSITION_RED_LABEL = ["apps/python/%s/ui/normalized/positions/red/%d.png" % (APP_NAME, n) for n in range(20)]
LEADERBOARD_POSITION_GREEN_LABEL = ["apps/python/%s/ui/normalized/positions/green/%d.png" % (APP_NAME, n) for n in range(20)]

LEADERBOARD_BACKGROUND = "apps/python/%s/ui/normalized/background.png" % APP_NAME
LEADERBOARD_BASE_RACE = "apps/python/%s/ui/normalized/race_base.png" % APP_NAME 
LEADERBOARD_BASE_QUALI = "apps/python/%s/ui/normalized/quali_base.png" % APP_NAME 

LEADERBOARD_INFO_BACKGROUNG = "apps/python/%s/ui/normalized/background_info.png" % APP_NAME

try:
    TEAM_COLORS = {}
    TEAM_NAME = {}
    with open("apps/python/%s/teams.txt" % APP_NAME) as fp:
        for line in fp:
            line = line.split(":")
            TEAM_COLORS[line[-1][:-1]] = "apps/python/%s/ui/normalized/tags/tag_%s.png" % (APP_NAME, line[1])
            TEAM_NAME[line[-1][:-1]] = line[0]
except FileNotFoundError:
    TEAM_COLORS = None

ROLEX_LOGO = "apps/python/%s/ui/normalized/rolex.png" % APP_NAME
DRIVER_WIDGET_BACKGROUND = "apps/python/%s/ui/normalized/driver_widget_background.png" % APP_NAME

# CONSTANTS
OVERTAKE_POSITION_LABEL_TIMER = 3 # seconds


# TIMERS
timer0, timer1 = 0, 0
    
# VARIABLES
totalDrivers = 0
driverPositions = None
focusedCar = 0

# WINDOWS
leaderboardWindow = None
driverWidget = None

# LABELS
leaderboard = None
lapCountTimerLabel = None

def acMain(ac_version):
    # VARIABLES
    global totalDrivers
    global driverPositions

    global leaderboardWindow, driverWidget
    # LABELS
    global leaderboard
    global lapCountTimerLabel

    totalDrivers = ac.getCarsCount()
    driverPositions = [[0, 0] for i in range(totalDrivers)] # driver positions and update times

    ac.initFont(0, FONT_NAME, 0, 0)

    leaderboardWindow = ac.newApp(APP_NAME)
    ac.setTitle(leaderboardWindow, "")
    ac.drawBorder(leaderboardWindow, 0)
    ac.setIconPosition(leaderboardWindow, 0, -10000)
    ac.setSize(leaderboardWindow, 200, 200)
    ac.setBackgroundOpacity(leaderboardWindow, 0)

    driverWidget = DriverWidget(APP_NAME+"_DriverWidget")

    # ===============================
    # Leaderboard Background
    leaderboardBaseLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(leaderboardBaseLabel, 0, 0)
    w, h = get_image_size(LEADERBOARD_BASE_RACE)
    ac.setSize(leaderboardBaseLabel, w, h)
    ac.setBackgroundTexture(leaderboardBaseLabel, LEADERBOARD_BASE_RACE)

    leaderboardBackgroundLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(leaderboardBackgroundLabel, 0, h)
    ac.setSize(leaderboardBackgroundLabel, w, totalDrivers*LeaderboardRow.ROW_HEIGHT + 2)
    ac.setBackgroundTexture(leaderboardBackgroundLabel, LEADERBOARD_BACKGROUND);

    # ===============================
    # Lap Counter / Time 
    lapCountTimerLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(lapCountTimerLabel, 74, 48)
    ac.setFontSize(lapCountTimerLabel, 22)
    ac.setCustomFont(lapCountTimerLabel, FONT_NAME, 0, 1)
    ac.setFontAlignment(lapCountTimerLabel, "center")
    ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)

    # ===============================
    # Info Background
    infoBackgroundLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(infoBackgroundLabel, w, h)
    ac.setSize(infoBackgroundLabel, 110, totalDrivers*LeaderboardRow.ROW_HEIGHT + 2)
    ac.setBackgroundTexture(infoBackgroundLabel, LEADERBOARD_INFO_BACKGROUNG)

    leaderboard = [None] * totalDrivers
    for i in range(totalDrivers):
        leaderboard[i] = LeaderboardRow(i)
        leaderboard[i].make_row(i)

    return APP_NAME

class DriverWidget:
    def __init__(self, appName):
        self.id = -1

        self.window = ac.newApp(appName)
        ac.setTitle(self.window, "")
        ac.drawBorder(self.window, 0)
        ac.setIconPosition(self.window, 0, -10000)
        ac.setSize(self.window, 300, 100)
        ac.setBackgroundOpacity(self.window, 0)

        self.backgroundTexture = ac.addLabel(self.window, "")
        w, h = get_image_size(DRIVER_WIDGET_BACKGROUND)
        ac.setPosition(self.backgroundTexture, 0,0)
        ac.setSize(self.backgroundTexture, w, h)
        ac.setBackgroundTexture(self.backgroundTexture, DRIVER_WIDGET_BACKGROUND);

        self.rolexLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.rolexLabel, 0, -72)
        ac.setSize(self.rolexLabel, 123, 70)
        ac.setBackgroundTexture(self.rolexLabel, ROLEX_LOGO);

        self.positionLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.positionLabel, 3,3)
        ac.setSize(self.positionLabel, 62, 62)

        self.teamLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.teamLabel, 70, 10)
        ac.setSize(self.teamLabel, 6, 45)

        self.nameLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.nameLabel, 90, 4)
        ac.setFontSize(self.nameLabel, 26)
        ac.setCustomFont(self.nameLabel, FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel, "left")

        self.teamNameLabel = ac.addLabel(self.window, "")
        ac.setPosition(self.teamNameLabel, 90, 35)
        ac.setFontSize(self.teamNameLabel, 20)
        ac.setCustomFont(self.teamNameLabel, FONT_NAME, 0, 1)
        ac.setFontColor(self.teamNameLabel, 0.66, 0.66, 0.66, 1)
        ac.setFontAlignment(self.teamNameLabel, "left")

        # TODO
        # self.driverNumberLabel = ac.addLabel(self.window, "")
    
    def hide(self):
        ac.setVisible(self.rolexLabel, 0)
        ac.setVisible(self.positionLabel, 0)
        ac.setVisible(self.teamLabel, 0)
        ac.setVisible(self.nameLabel, 0)
        ac.setVisible(self.teamNameLabel, 0)

    def show(self, id):
        pos = ac.getCarRealTimeLeaderboardPosition(id)
        ac.setBackgroundTexture(self.positionLabel, LEADERBOARD_POSITION_LABEL[pos+1])
        ac.setVisible(self.positionLabel, 1)

        if self.id == id: return # dont update anything else
        self.id = id

        ac.setVisible(self.rolexLabel, 1)
        ac.setVisible(self.nameLabel, 1)
        name = ac.getDriverName(id)
        ac.setText(self.nameLabel, name)

        if TEAM_COLORS:
            try:
                ac.setBackgroundTexture(self.teamLabel, TEAM_COLORS[name]);
                ac.setVisible(self.teamLabel, 1)
                ac.setVisible(self.teamNameLabel, 1)
                ac.setText(self.teamNameLabel, TEAM_NAME[name])
            except KeyError:
                ac.console("%s:Name Missing in teams.txt %s" % (APP_NAME, name))

class LeaderboardRow:
    X_BASE = 5
    Y_BASE = 84
    ROW_HEIGHT = 37
    def __init__(self, row):
        self.row = row 
        self.positionLabel = None
        self.teamLabel = None
        self.nameLabel = None
        self.pitLabel = None
        self.infoLabel = None

        self.button = None

        self.driverName = None
        self.driverId = -1
        self.interval = 0

        self.positionLabelId = 0 # 0 white, 1 red, 2 green - to prevent loading the labels all the time
        self.out = False

    def make_row(self, id):
        px, py = LeaderboardRow.X_BASE, LeaderboardRow.Y_BASE + LeaderboardRow.ROW_HEIGHT * self.row # position of the names
        self.px = px
        self.py = py

        self.positionLabel = ac.addLabel(leaderboardWindow, "")
        ac.setPosition(self.positionLabel, px-4, py-7)
        ac.setSize(self.positionLabel, 38, 38)
        ac.setBackgroundTexture(self.positionLabel, LEADERBOARD_POSITION_LABEL[self.row+1]);
        self.positionLabelId = 0 # position label white

        self.driverName = ac.getDriverName(id)
        self.driverId = id
        self.nameLabel = ac.addLabel(leaderboardWindow, self.driverName[:3].upper())
        ac.setPosition(self.nameLabel, px + 65, py)
        ac.setFontSize(self.nameLabel, 18)
        ac.setCustomFont(self.nameLabel, FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel, "left")

        if TEAM_COLORS:
            try:
                self.teamLabel = ac.addLabel(leaderboardWindow, "")
                ac.setPosition(self.teamLabel, px + 47, py + 2)
                ac.setSize(self.teamLabel, 5, 18)
                ac.setBackgroundTexture(self.teamLabel, TEAM_COLORS[self.driverName]);
            except KeyError:
                ac.console("%s:Name Missing in teams.txt %s" % (APP_NAME, self.driverName))

        self.infoLabel = ac.addLabel(leaderboardWindow, "Interval")
        ac.setPosition(self.infoLabel, 250, py)
        ac.setFontSize(self.infoLabel, 18)
        ac.setCustomFont(self.infoLabel, FONT_NAME, 0, 1)
        ac.setFontColor(self.infoLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.infoLabel, "right")
        
        # self.button = ac.addButton(leaderboardWindow, "")
        # ac.setPosition(self.button, px, py-4)
        # ac.setSize(self.button, 200,38)
        # ac.addOnClickedListener(self.button, functools.partial(on_click, row=self.row))
    
    def update_name(self, id):
        if self.driverId == id: return # no need to update
        self.driverName = ac.getDriverName(id)
        self.driverId = id
        ac.setText(self.nameLabel, self.driverName[:3].upper())
        try:
            ac.setBackgroundTexture(self.teamLabel, TEAM_COLORS[self.driverName]);
        except KeyError:
            ac.console("%s:Name Missing in teams.txt %s" % (APP_NAME, self.driverName))
    
    def update_time(self, time):
        if self.out or self.row == 0: return # no need to update
        ac.setText(self.infoLabel, time)
    
    def mark_red_position(self):
        if self.out or self.positionLabelId == 1: return # no need to update
        ac.setBackgroundTexture(self.positionLabel, LEADERBOARD_POSITION_RED_LABEL[self.row+1])
        self.positionLabelId = 1

    def mark_green_position(self):
        if self.out or self.positionLabelId == 2: return # no need to update
        ac.setBackgroundTexture(self.positionLabel, LEADERBOARD_POSITION_GREEN_LABEL[self.row+1])
        self.positionLabelId = 2
    
    def mark_white_position(self):
        if self.out or self.positionLabelId == 0: return # no need to update
        ac.setBackgroundTexture(self.positionLabel, LEADERBOARD_POSITION_LABEL[self.row+1])
        self.positionLabelId = 0
    
    def mark_out(self):
        if self.out: return
        self.out = True
        ac.console("OUT %d %s" % (self.row, self.driverName))
        ac.setVisible(self.positionLabel, 0)
        ac.setPosition(self.teamLabel, self.px + 12, self.py + 2)
        ac.setPosition(self.nameLabel, self.px + 30, self.py)
        ac.setFontColor(self.nameLabel, .58,.53,.53, 1)
        ac.setText(self.infoLabel, "OUT")
        ac.setFontColor(self.infoLabel, .58,.53,.53, 1)

# ============================================================================
#                                   UPDATE
# ============================================================================

def acUpdate(deltaT):
    # TIMERS
    global timer0, timer1
    
    # VARIABLES
    global totalDrivers
    global driverPositions
    global focusedCar

    global leaderboardWindow, driverWidget

    # LABELS
    global leaderboard
    global lapCountTimerLabel

    timer0 += deltaT
    timer1 += deltaT
  
    # Once per second
    if timer0 > 1:
        timer0 = 0
        ac.setBackgroundOpacity(leaderboardWindow, 0)
        ac.setBackgroundOpacity(driverWidget.window, 0)

        # ============================
        # SERVER LAP
        lc = max((ac.getCarState(i, acsys.CS.LapCount) for i in range(totalDrivers))) + 1
        if lc >= info.graphics.numberOfLaps:
            ac.setText(lapCountTimerLabel, "FINAL LAP")
            ac.setFontColor(lapCountTimerLabel, 1,0,0,1)
        else:
            ac.setText(lapCountTimerLabel, "%d / %d" % (lc, info.graphics.numberOfLaps))
            ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)

        for i in range(totalDrivers):
            leaderboard[i].update_time("+0.000")

        # ============================
        # CHANGE CAR FOCUS AND DRIVER WIDGET
        # TODO
        # if focusedCar != ac.getFocusedCar():
        #     ac.focusCar(focusedCar)

        driverWidget.show(focusedCar)

    # 3 times per second
    if timer1 > 0.3:

        # ============================
        # POSITION UPDATE
        for i in range(totalDrivers):
            pos = ac.getCarRealTimeLeaderboardPosition(i)
            if ac.isConnected(i) == 0: # mark unconnected drivers
                leaderboard[pos].mark_out()
                continue
            else:
                leaderboard[pos].out = False # needed to distinguish
            leaderboard[pos].update_name(i)
            if pos != driverPositions[i][0]: # there was an overtake
                driverPositions[i][1] = OVERTAKE_POSITION_LABEL_TIMER # set timer
                if pos < driverPositions[i][0]:
                    leaderboard[pos].mark_green_position()
                elif pos > driverPositions[i][0]:
                    leaderboard[pos].mark_red_position()
            elif driverPositions[i][1] <= 0:
                leaderboard[pos].mark_white_position()
            else:
                driverPositions[i][1] -= timer1
            driverPositions[i][0] = pos

        timer1 = 0
        
def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                ac.console("%s: Error getting image size %s" % (APP_NAME, fname))
                return
            width, height = struct.unpack('>ii', head[16:24])
        return width, height

def time_to_string(t, include_ms=True):
	try:
		hours, x = divmod(int(t), 3600000)
		mins, x = divmod(x, 60000)
		secs, ms = divmod(x, 1000)
		if not include_ms:
			return '%d:%02d' % (mins, secs)
		return '%d.%03d' % (secs, ms) if mins == 0 else '%d:%02d.%03d' % (mins, secs, ms)
	except Exception:
		return '--:--.---'

def on_click(*args, row=None):
    global focusedCar
    focusedCar = row
