import sys
import re
import os

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
LEADERBOARD_BACKGROUND = "apps/python/%s/ui/normalized/background.png" % APP_NAME
LEADERBOARD_BASE_RACE = "apps/python/%s/ui/normalized/race_base.png" % APP_NAME 
LEADERBOARD_BASE_QUALI = "apps/python/%s/ui/normalized/quali_base.png" % APP_NAME 

try:
    TEAM_COLORS = {}
    with open("apps/python/%s/teams.txt" % APP_NAME) as fp:
        for line in fp:
            line = line.split(":")
            TEAM_COLORS[line[-1][:-1]] = "apps/python/%s/ui/normalized/tags/tag_%s.png" % (APP_NAME, line[0])
except FileNotFoundError:
    TEAM_COLORS = None


# TIMERS
timer0, timer1 = 0, 0
    
# VARIABLES
totalDrivers = 0
driverTimes = None

appWindow = None
# LABELS
leaderboard = None
lapCountTimerLabel = None

def acMain(ac_version):
    # VARIABLES
    global totalDrivers
    global driverTimes

    global appWindow
    # LABELS
    global leaderboard
    global lapCountTimerLabel

    totalDrivers = ac.getCarsCount()
    driverTimes = [0 for i in range(totalDrivers)]

    ac.initFont(0, FONT_NAME, 0, 0)

    appWindow = ac.newApp(APP_NAME)
    ac.setTitle(appWindow, "")
    ac.drawBorder(appWindow, 0)
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setSize(appWindow, 200, 400)
    ac.setBackgroundOpacity(appWindow, 0)

    leaderboardBaseLabel = ac.addLabel(appWindow, "")
    ac.setPosition(leaderboardBaseLabel, 0, 0)
    w, h = get_image_size(LEADERBOARD_BASE_RACE)
    ac.setSize(leaderboardBaseLabel, w, h)
    ac.setBackgroundTexture(leaderboardBaseLabel, LEADERBOARD_BASE_RACE)

    leaderboardBackgroundLabel = ac.addLabel(appWindow, "")
    ac.setPosition(leaderboardBackgroundLabel, 0, h)
    ac.setSize(leaderboardBackgroundLabel, w, totalDrivers*LeaderboardRow.ROW_HEIGHT)
    ac.setBackgroundTexture(leaderboardBackgroundLabel, LEADERBOARD_BACKGROUND);

    lapCountTimerLabel = ac.addLabel(appWindow, "")
    ac.setPosition(lapCountTimerLabel, 74, 48)
    ac.setFontSize(lapCountTimerLabel, 20)
    ac.setCustomFont(lapCountTimerLabel, FONT_NAME, 0, 1)
    ac.setFontAlignment(lapCountTimerLabel, "center")
    ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)

    leaderboard = [None] * totalDrivers
    for i in range(totalDrivers):
        leaderboard[i] = LeaderboardRow()
        leaderboard[i].make_row(i, ac.getDriverName(i))

    return APP_NAME

class LeaderboardRow:
    X_BASE = 5
    Y_BASE = 84
    ROW_HEIGHT = 37
    def __init__(self):
        self.positionLabel = None
        self.teamLabel = None
        self.nameLabel = None
        self.pitLabel = None
        self.intervalLabel = None

        self.driverName = None
        self.interval = 0
    
    def make_row(self, id, name):
        px, py = LeaderboardRow.X_BASE, LeaderboardRow.Y_BASE + LeaderboardRow.ROW_HEIGHT * id # position of the names

        self.positionLabel = ac.addLabel(appWindow, "")
        ac.setPosition(self.positionLabel, px-4, py-6)
        ac.setSize(self.positionLabel, 38, 38)
        ac.setBackgroundTexture(self.positionLabel, LEADERBOARD_POSITION_LABEL[id+1]);

        self.driverName = name
        self.nameLabel = ac.addLabel(appWindow, name[:3].upper())
        ac.setPosition(self.nameLabel, px + 65, py)
        ac.setFontSize(self.nameLabel, 18)
        ac.setCustomFont(self.nameLabel, FONT_NAME, 0, 1)
        ac.setFontColor(self.nameLabel, 0.86, 0.86, 0.86, 1)
        ac.setFontAlignment(self.nameLabel, "left")

        if TEAM_COLORS:
            try:
                self.teamLabel = ac.addLabel(appWindow, "")
                ac.setPosition(self.teamLabel, px + 43, py + 2)
                ac.setSize(self.teamLabel, 5, 18)
                ac.setBackgroundTexture(self.teamLabel, TEAM_COLORS[name]);
            except KeyError:
                ac.console("%s:Name Missing in teams.txt %s" % (APP_NAME, name))
    
    def update_name(self, name):
        self.driverName = name
        ac.setText(self.nameLabel, name[:3].upper())
        try:
            ac.setBackgroundTexture(self.teamLabel, TEAM_COLORS[name]);
        except KeyError:
            ac.console("%s:Name Missing in teams.txt %s" % (APP_NAME, name))


# ============================================================================
#                                   UPDATE
# ============================================================================

def acUpdate(deltaT):
    # TIMERS
    global timer0, timer1
    
    # VARIABLES
    global totalDrivers

    global appWindow
    # LABELS
    global leaderboard
    global lapCountTimerLabel

    timer0 += deltaT
    timer1 += deltaT
  
    # Once per second
    if timer0 > 1:
        timer0 = 0
        ac.setBackgroundOpacity(appWindow, 0)

        # ============================
        # SERVER LAP
        lc = max((ac.getCarState(i, acsys.CS.LapCount) for i in range(totalDrivers))) + 1
        if lc >= info.graphics.numberOfLaps:
            ac.setText(lapCountTimerLabel, "FINAL LAP")
            ac.setFontColor(lapCountTimerLabel, 1,0,0,1)
        else:
            ac.setText(lapCountTimerLabel, "%d / %d" % (lc, info.graphics.numberOfLaps))
            ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)
        
    # 5 times per second
    if timer1 > 0.2:
        timer1 = 0

        # ============================
        # POSITION UPDATE
        for i in range(totalDrivers):
            pos = ac.getCarRealTimeLeaderboardPosition(i)
            leaderboard[pos].update_name(ac.getDriverName(i))

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