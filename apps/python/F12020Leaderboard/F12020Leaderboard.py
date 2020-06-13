import sys
import os
import time

import ac
import acsys


import ctypes
from ctypes import wintypes

from sim_info_lib.sim_info import info

from constants import FC

from utils import get_image_size, time_to_string
from DriverWidget import DriverWidget
from LeaderboardRow import LeaderboardRow
from FastestLapBanner import FastestLapBanner

# TIMERS
timer0, timer1, timer2 = 0, 0, 0
 
# VARIABLES
totalDrivers = 0
drivers = None
fastest_lap = 99999999

race_started = False
replay_started = False

# REPLAY FILE
replay_file = None

# WINDOWS
leaderboardWindow = None
driverWidget = None
fastest_lap_banner = None

# LABELS
leaderboard = None
lapCountTimerLabel = None

class Driver: # class to hold driver information
    def __init__(self, id, n_splits):
        self.id = id
        self.position = 200
        self.starting_position = -1
        self.timer = 0
        self.current_split = -1
        self.n_splits = int(n_splits)
        self.split_times = [0 for i in range(int(n_splits))] # make this dependant of the track
        self.pits = 0
        self.pit_time = 0
        self.tyre = ""
        self.timeDiff = 0

    def get_split_id(self, spline):
        return int(spline//(1/self.n_splits))

def acMain(ac_version):
    # VARIABLES
    global totalDrivers
    global drivers

    global leaderboardWindow, driverWidget, fastest_lap_banner
    # LABELS
    global leaderboard
    global lapCountTimerLabel

    totalDrivers = ac.getCarsCount()
    n_splits = ac.getTrackLength(0) / FC.TRACK_SECTION_LENGTH
    drivers = [Driver(i, n_splits) for i in range(totalDrivers)] # driver positions and update times
    
    ac.initFont(0, FC.FONT_NAME, 0, 0)

    leaderboardWindow = ac.newApp(FC.APP_NAME)
    ac.setTitle(leaderboardWindow, "")
    ac.drawBorder(leaderboardWindow, 0)
    ac.setIconPosition(leaderboardWindow, 0, -10000)
    ac.setSize(leaderboardWindow, 200, 200)
    ac.setBackgroundOpacity(leaderboardWindow, 0)

    driverWidget = DriverWidget(FC.APP_NAME+"_DriverWidget")

    # ===============================
    # Leaderboard Background
    leaderboardBaseLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(leaderboardBaseLabel, 0, 0)
    w, h = get_image_size(FC.LEADERBOARD_BASE_RACE)
    ac.setSize(leaderboardBaseLabel, w, h)
    ac.setBackgroundTexture(leaderboardBaseLabel, FC.LEADERBOARD_BASE_RACE)

    leaderboardBackgroundLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(leaderboardBackgroundLabel, 0, h)
    ac.setSize(leaderboardBackgroundLabel, w, totalDrivers*LeaderboardRow.ROW_HEIGHT + 2)
    ac.setBackgroundTexture(leaderboardBackgroundLabel, FC.LEADERBOARD_BACKGROUND);

    # ===============================
    # Lap Counter / Time 
    lapCountTimerLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(lapCountTimerLabel, 74, 48)
    ac.setFontSize(lapCountTimerLabel, 22)
    ac.setCustomFont(lapCountTimerLabel, FC.FONT_NAME, 0, 1)
    ac.setFontAlignment(lapCountTimerLabel, "center")
    ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)

    # ===============================
    # Info Background
    infoBackgroundLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(infoBackgroundLabel, w, h)
    ac.setSize(infoBackgroundLabel, 110, totalDrivers*LeaderboardRow.ROW_HEIGHT + 2)
    ac.setBackgroundTexture(infoBackgroundLabel, FC.LEADERBOARD_INFO_BACKGROUNG)

    # ===============================
    # FastestLap Banner
    fastest_lap_banner = FastestLapBanner(FC.APP_NAME+"_FastestLap_Banner")
    fastest_lap_banner.hide()

    leaderboard = [None] * totalDrivers
    for i in range(totalDrivers):
        leaderboard[i] = LeaderboardRow(leaderboardWindow, i)

    return FC.APP_NAME

# ============================================================================
#                                   UPDATE
# ============================================================================

def acUpdate(deltaT):
    # TIMERS
    global timer0, timer1, timer2
    
    # VARIABLES
    global totalDrivers
    global drivers
    global fastest_lap

    global race_started, replay_started

    global replay_file

    # Widgets
    global leaderboardWindow, driverWidget

    # LABELS
    global leaderboard
    global lapCountTimerLabel

    # ============================
    # UPDATE TIMERS
    timer0 += deltaT
    timer1 += deltaT
    timer2 += deltaT
    # ============================

    # ================================================================
    #                            RACES
    # ================================================================
    if info.graphics.session == 2:

        # Once per second
        if timer0 > 1:
            timer0 = 0
            ac.setBackgroundOpacity(leaderboardWindow, 0)
            ac.setBackgroundOpacity(driverWidget.window, 0)
            ac.setBackgroundOpacity(fastest_lap_banner.window, 0)

            # ============================
            # SERVER LAP
            lc = max((ac.getCarState(i, acsys.CS.LapCount) for i in range(totalDrivers))) + 1
            if lc >= info.graphics.numberOfLaps:
                ac.setText(lapCountTimerLabel, "FINAL LAP")
                ac.setFontColor(lapCountTimerLabel, 1,0,0,1)
            else:
                ac.setText(lapCountTimerLabel, "%d / %d" % (lc, info.graphics.numberOfLaps))
                ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)

            # ===========================
            # CALCULATE TIME DIFERENCES
            dPosition = sorted(drivers, key=lambda x: x.position)
            for i in range(1, len(dPosition)):
                driver_ahead, driver = dPosition[i-1], dPosition[i]
                timeDiff = driver.split_times[driver.current_split - 1] - driver_ahead.split_times[driver.current_split - 1]
                if timeDiff < 0: continue # ignore these times, happens on overtakes
                driver.timeDiff = timeDiff
                if driver.position > totalDrivers: continue # might try to update befor it is possible
                leaderboard[driver.position].update_time("+" + time_to_string(timeDiff*1000))
            leaderboard[0].update_time("Interval") # Force it

            # ============================
            # MARK FASTEST LAP
            if lc > FC.FASTEST_LAP_STARTING_LAP:
                fastest_driver = None
                for d in drivers:
                    lap = ac.getCarState(d.id, acsys.CS.BestLap)
                    if lap != 0 and lap < fastest_lap:
                        fastest_lap = lap
                        fastest_lap_banner.show(lap, ac.getDriverName(d.id))
                        fastest_driver = d
                        LeaderboardRow.FASTEST_LAP_ID = d.id;
                for row in leaderboard:
                    row.mark_fastest_lap()

            # ============================
            # PITS MARKER
            for row in leaderboard:
                if ac.isCarInPitline(row.driverId) == 1:
                    row.mark_enter_pits()
                    drivers[row.driverId].tyre = ac.getCarTyreCompound(row.driverId) # maybe will change tyre
                else:
                    row.mark_left_pits()
                if time.time() - drivers[row.driverId].pit_time > 20 and ac.isCarInPit(row.driverId):
                    drivers[row.driverId].pits += 1
                    drivers[row.driverId].pit_time = time.time()

            # ============================
            # CHANGE CAR FOCUS AND DRIVER WIDGET
            id = ac.getFocusedCar()
            if drivers[id].position <= totalDrivers: # in case it wasnt updated yet
                driverWidget.show(id, drivers[id].position, drivers[id].starting_position, drivers[id].tyre, drivers[id].pits)

            # ========================================================
            # SAVE DRIVER STATUS IN A FILE TO LOAD ON REPLAY
            if replay_file:
                write_driver_info(replay_file, info.graphics.iCurrentTime, drivers)
            # ========================================================

        # 3 times per second
        if timer1 > 0.3:
            if not race_started:
                if info.graphics.iCurrentTime > 0:
                    race_started = True
                    for d in drivers:
                        d.starting_position = ac.getCarLeaderboardPosition(d.id)
                        d.tyre = ac.getCarTyreCompound(d.id)
                    replay_file = setup_replay_file(drivers) # save starting info on the drivers

            # ============================
            # POSITION UPDATE
            for i in range(totalDrivers):
                pos = ac.getCarRealTimeLeaderboardPosition(i)
                if ac.isConnected(i) == 0: # mark unconnected drivers
                    leaderboard[pos].mark_out()
                else:
                    leaderboard[pos].mark_in()
                    leaderboard[pos].update_name(i)

                # OVERTAKE
                if pos != drivers[i].position: # there was an overtake
                    drivers[i].timer = FC.OVERTAKE_POSITION_LABEL_TIMER # set timer
                    if pos < drivers[i].position:
                        leaderboard[pos].mark_green_position()
                    elif pos > drivers[i].position:
                        leaderboard[pos].mark_red_position()
                elif drivers[i].timer <= 0:
                    leaderboard[pos].mark_white_position()
                else:
                    drivers[i].timer -= timer1
                drivers[i].position = pos
                # END OVERTAKE

            # ============================
            # FASTEST LAP BANNER TIMER
            if fastest_lap_banner.timer > 0:
                fastest_lap_banner.timer -= timer1
                fastest_lap_banner.hide()

            timer1 = 0

        # 10 times per second
        if timer2 > 0.1:
            timer2 = 0

            # =============================
            # SAVE SPLIT TIMES
            for d in drivers:
                if ac.isConnected(d.id) == 0: continue
                current_split = d.get_split_id(ac.getCarState(d.id, acsys.CS.NormalizedSplinePosition))
                if d.current_split != current_split: # save split time at each split of the track
                    d.split_times[current_split-1] = time.time()
                    d.current_split = current_split

    # ================================================================
    #                            QUALIFY
    # ================================================================
    elif info.graphics.session == 1:
        # Once per second
        if timer0 > 1:
            timer0 = 0
            ac.setBackgroundOpacity(leaderboardWindow, 0)
            ac.setBackgroundOpacity(driverWidget.window, 0)
            ac.setBackgroundOpacity(fastest_lap_banner.window, 0)

    # ================================================================
    #                            REPLAYS
    # ================================================================
    elif info.graphics.status == 1:
        # Once per second
        if timer0 > 1:
            timer0 = 0
            ac.setBackgroundOpacity(leaderboardWindow, 0)
            ac.setBackgroundOpacity(driverWidget.window, 0)
            ac.setBackgroundOpacity(fastest_lap_banner.window, 0)

            id = ac.getFocusedCar()
            drivers[id].position = 1
            driverWidget.show(id, drivers[id].position, drivers[id].starting_position, drivers[id].tyre, drivers[id].pits)

        if timer1 > 0.3:
            if not replay_started:
                if info.graphics.iCurrentTime > 0:
                    replay_file = open_replay_file_read()
                    replay_started = True
                    for d in drivers:
                        d.starting_position = ac.getCarLeaderboardPosition(d.id)
                        d.tyre = ac.getCarTyreCompound(d.id)

        
def acShutdown():
    global replay_file
    if replay_file:
        replay_file.close()

def reset_variables():
    pass

def write_driver_info(replay_file, time, drivers):
    data = "%d " % time
    for d in drivers:
        data += "[%d;%f;%s;%d] " % (d.position, d.timeDiff, d.tyre, d.pits)
    replay_file.write(data+'\n')
    pass

def setup_replay_file(drivers):
    replay_file = open(FC.REPLAY_DIR + "replayFile.txt", "w")
    data = "START: "
    for d in drivers:
        data += "[%d;%s] " % (d.starting_position, d.tyre)
    replay_file.write(data+'\n')
    return replay_file

def load_replay_file():
    try:
        return open(FC.REPLAY_DIR + "replayFile.txt", "r")
    except FileNotFoundError:
        ac.log("Replay File not found.")