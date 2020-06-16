import sys
import os
import time
import bisect

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


MAX_LAP_TIME = 999999999

# TIMERS
timer0, timer1, timer2 = 0, 0, 0

 
# VARIABLES
totalDrivers = 0
drivers = None
fastest_lap = MAX_LAP_TIME

race_started = False
replay_started = False
quali_started = False

leaderboard_displayed = False

qualify_session_time = 0

# REPLAY FILE
replay_file = None
replay_data = None

# WINDOWS
leaderboardWindow = None
driverWidget = None
fastest_lap_banner = None

# LABELS
leaderboard = None
lapCountTimerLabel = None
leaderboardBaseLabel = None
leaderboardInfoBackgroundLabel = None
leaderboardBackgroundLabel = None

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
        self.out = False
        self.current_lap = 0
        self.best_lap = MAX_LAP_TIME

    def get_split_id(self, spline):
        return int(spline//(1/self.n_splits))

def acMain(ac_version):
    # VARIABLES
    global totalDrivers
    global drivers

    global leaderboardWindow, driverWidget, fastest_lap_banner
    # LABELS
    global leaderboard
    global lapCountTimerLabel, leaderboardBaseLabel, leaderboardInfoBackgroundLabel, leaderboardBackgroundLabel

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
    leaderboardInfoBackgroundLabel = ac.addLabel(leaderboardWindow, "")
    ac.setPosition(leaderboardInfoBackgroundLabel, w, h)
    ac.setSize(leaderboardInfoBackgroundLabel, 110, totalDrivers*LeaderboardRow.ROW_HEIGHT + 2)
    ac.setBackgroundTexture(leaderboardInfoBackgroundLabel, FC.LEADERBOARD_INFO_BACKGROUNG)

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

    global race_started, replay_started, quali_started

    global qualify_session_time

    global replay_file
    global replay_data

    # Widgets
    global leaderboardWindow, driverWidget

    # LABELS
    global leaderboard
    global lapCountTimerLabel, leaderboardBaseLabel, leaderboardInfoBackgroundLabel, leaderboardBackgroundLabel

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

        # 3 times per second
        if timer1 > 0.3:
            # CHECK RACE RESTART
            if race_started and info.graphics.completedLaps == 0 and info.graphics.iCurrentTime == 0:
                race_started = False

            # CHECK RACE START
            if not race_started and info.graphics.iCurrentTime > 0:
                # RESET THINGS
                fastest_lap = MAX_LAP_TIME
                LeaderboardRow.FASTEST_LAP_ID = -1
                # in case we are coming from a qualify
                ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)
                ac.setBackgroundTexture(leaderboardBaseLabel, FC.LEADERBOARD_BASE_RACE)

                race_started = True
                quali_started = False
                for d in drivers:
                    d.starting_position = ac.getCarLeaderboardPosition(d.id)
                    d.tyre = ac.getCarTyreCompound(d.id)
                    d.pits = 0
                replay_file = setup_replay_file(drivers, info.graphics.numberOfLaps) # save starting info on the drivers

            # ============================
            # POSITION UPDATE
            for i in range(totalDrivers):
                pos = ac.getCarRealTimeLeaderboardPosition(i)
                connected = ac.isConnected(i)
                if connected == 0 and not drivers[i].out: # mark unconnected drivers
                    leaderboard[pos].mark_out()
                    drivers[i].out = True
                elif connected == 1 and drivers[i].out:
                    leaderboard[pos].mark_in()
                    drivers[i].out = False
                if connected == 1:
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

        # Once per second
        if timer0 > 1:
            timer0 = 0
            ac.setBackgroundOpacity(leaderboardWindow, 0)
            ac.setBackgroundOpacity(driverWidget.window, 0)
            ac.setBackgroundOpacity(fastest_lap_banner.window, 0)

            # ============================
            # SERVER LAP
            for i in range(totalDrivers):
                drivers[i].current_lap = ac.getCarState(i, acsys.CS.LapCount)
            lc = max((drivers[i].current_lap for i in range(totalDrivers))) + 1
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
                if driver.position > totalDrivers: continue # might try to update before it is possible
                driver.timeDiff = timeDiff
                leaderboard[driver.position].update_time("+" + time_to_string(timeDiff*1000))
            leaderboard[0].update_time("Interval") # Force it

            # ============================
            # MARK FASTEST LAP
            if lc > FC.FASTEST_LAP_STARTING_LAP:
                for d in drivers:
                    lap = ac.getCarState(d.id, acsys.CS.BestLap)
                    if lap != 0 and lap < fastest_lap:
                        fastest_lap = lap
                        fastest_lap_banner.show(lap, ac.getDriverName(d.id))
                        LeaderboardRow.FASTEST_LAP_ID = d.id
                        if replay_file:
                            write_fastest_lap(replay_file, info.graphics.completedLaps, info.graphics.iCurrentTime, d, fastest_lap)
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
            if race_started:
                id = ac.getFocusedCar()
                if drivers[id].position <= totalDrivers: # in case it wasnt updated yet
                    driverWidget.show(id, drivers[id].position, drivers[id].starting_position, drivers[id].tyre, drivers[id].pits)
            else:
                driverWidget.hide()

            # ========================================================
            # SAVE DRIVER STATUS IN A FILE TO LOAD ON REPLAY
            if replay_file:
                write_driver_info(replay_file, info.graphics.completedLaps, info.graphics.iCurrentTime, drivers)
            # ========================================================


    # ================================================================
    #                            QUALIFY
    # ================================================================
    elif info.graphics.session == 1:

        # 3 times per second
        if timer1 > 0.3:
            # =============================================
            # QUALIFY RESTART
            if quali_started and qualify_session_time - info.graphics.sessionTimeLeft < 1:
                quali_started = False

            # =============================================
            # QUALIFY START
            if not quali_started:
                show_leaderboard()
                ac.setBackgroundTexture(leaderboardBaseLabel, FC.LEADERBOARD_BASE_QUALI)
                ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)
                qualify_session_time = info.graphics.sessionTimeLeft
                fastest_lap = MAX_LAP_TIME
                LeaderboardRow.FASTEST_LAP_ID = -1
                quali_started = True
                race_started = False

            # =============================================
            # SAVE BEST LAPS FOR EACH DRIVER
            for i in range(totalDrivers):
                lap = ac.getCarState(i, acsys.CS.BestLap)
                if lap != 0:
                    drivers[i].best_lap = lap
                if lap != 0 and lap < fastest_lap:
                    fastest_lap = lap
                    fastest_lap_banner.show(lap, ac.getDriverName(i))

            # =============================================
            # MANAGE LEADERBOARD
            dPosition = sorted(drivers, key=lambda x: x.best_lap)
            for i in range(totalDrivers):
                # MARK IN/OUT DRIVERS
                connected = ac.isConnected(i)
                if connected == 0 and not dPosition[i].out: # mark unconnected drivers
                    leaderboard[i].mark_out()
                    dPosition[i].out = True
                elif connected == 1 and dPosition[i].out:
                    leaderboard[i].mark_in()
                    dPosition[i].out = False
                if connected == 1:
                    leaderboard[i].update_name(dPosition[i].id)
                    if dPosition[i].best_lap == MAX_LAP_TIME:
                        leaderboard[i].update_time("NO TIME")
                    elif i == 0:
                        leaderboard[i].update_time(time_to_string(dPosition[i].best_lap))
                    else:
                        timeDiff = dPosition[i].best_lap - dPosition[0].best_lap
                        leaderboard[i].update_time("+" + time_to_string(timeDiff))

                # OVERTAKES
                if i != dPosition[i].position: # there was an overtake on this driver
                    dPosition[i].timer = FC.OVERTAKE_POSITION_LABEL_TIMER
                    if i < dPosition[i].position:
                        leaderboard[i].mark_green_position()
                    elif i > dPosition[i].position:
                        leaderboard[i].mark_red_position()
                elif dPosition[i].timer <= 0:
                    leaderboard[i].mark_white_position()
                else:
                    dPosition[i].timer -= timer1
                dPosition[i].position = i
                # END OVERTAKE

            # ============================
            # FASTEST LAP BANNER TIMER
            if fastest_lap_banner.timer > 0:
                fastest_lap_banner.timer -= timer1
                fastest_lap_banner.hide()
            
            timer1 = 0

        # Once per second
        if timer0 > 1:
            timer0 = 0
            ac.setBackgroundOpacity(leaderboardWindow, 0)
            ac.setBackgroundOpacity(driverWidget.window, 0)
            ac.setBackgroundOpacity(fastest_lap_banner.window, 0)

            if quali_started:
                ac.console(str(info.graphics.sessionTimeLeft))
                ac.setText(lapCountTimerLabel, time_to_string(info.graphics.sessionTimeLeft)[:-4])
                if info.graphics.sessionTimeLeft < qualify_session_time / 5:
                    ac.setFontColor(lapCountTimerLabel, 1,0,0,1)

            driverWidget.hide()


    # ================================================================
    #                            REPLAYS
    # ================================================================
    elif info.graphics.status == 1:

        # three times per second
        if timer1 > 0.3:
            if not replay_started:
                if info.graphics.iCurrentTime > 0:
                    replay_data = load_replay_file(drivers)
                    replay_started = True

            # ============================
            # FASTEST LAP BANNER TIMER
            if fastest_lap_banner.timer > 0:
                fastest_lap_banner.timer -= timer1
                fastest_lap_banner.hide()

            # ============================
            # GET DATA FOR THIS UPDATE
            if replay_data:
                new_positions = lookup_data(info.graphics.completedLaps, info.graphics.iCurrentTime, replay_data, drivers)

                # ============================
                # POSITION UPDATE
                for i in range(totalDrivers):
                    pos = new_positions[i]
                    if drivers[i].out: # mark unconnected drivers
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
            
            timer1 = 0

        # Once per second
        if timer0 > 1:
            timer0 = 0
            ac.setBackgroundOpacity(leaderboardWindow, 0)
            ac.setBackgroundOpacity(driverWidget.window, 0)
            ac.setBackgroundOpacity(fastest_lap_banner.window, 0)

            # ============================
            # SERVER LAP
            if replay_data:
                lc = max((drivers[i].current_lap for i in range(totalDrivers))) + 1
                if lc >= replay_data['nLaps']:
                    ac.setText(lapCountTimerLabel, "FINAL LAP")
                    ac.setFontColor(lapCountTimerLabel, 1,0,0,1)
                else:
                    ac.setText(lapCountTimerLabel, "%d / %d" % (lc, replay_data['nLaps']))
                    ac.setFontColor(lapCountTimerLabel, 0.86, 0.86, 0.86, 1)

            # ============================
            # PITS MARKER
            for row in leaderboard:
                if ac.isCarInPitline(row.driverId) == 1:
                    row.mark_enter_pits()
                else:
                    row.mark_left_pits()

            # ============================
            # DRIVER WIDGET UPDATE
            if replay_started:
                id = ac.getFocusedCar()
                driverWidget.show(id, drivers[id].position, drivers[id].starting_position, drivers[id].tyre, drivers[id].pits)
            else:
                driverWidget.hide()

            # ============================
            # UPDATE TIMES
            if replay_data:
                for row in leaderboard:
                    row.update_time("+" + time_to_string(drivers[row.driverId].timeDiff*1000))
                    if row.row == 0:
                        row.update_time("Interval") # Force it

    # END UPDATE

def acShutdown():
    global replay_file
    if replay_file:
        replay_file.close()

def hide_leaderboard():
    global leaderboard_displayed
    global leaderboard
    global lapCountTimerLabel, leaderboardBaseLabel, leaderboardInfoBackgroundLabel, leaderboardBackgroundLabel
    if not leaderboard_displayed: return

def show_leaderboard():
    global leaderboard_displayed
    global leaderboard
    global lapCountTimerLabel, leaderboardBaseLabel, leaderboardInfoBackgroundLabel, leaderboardBackgroundLabel
    if leaderboard_displayed: return

def write_driver_info(replay_file, laps, time, drivers):
    data = "U %d %d " % (laps, time)
    for d in drivers:
        data += "%d;%f;%s;%d;%d;%d " % (d.position, d.timeDiff, d.tyre, d.pits, int(d.out), d.current_lap)
    replay_file.write(data+'\n')

def write_fastest_lap(replay_file, laps, time, driver, fastest_lap):
    replay_file.write("FL %d;%d %d;%f\n" % (laps, time, driver.id, fastest_lap))

def setup_replay_file(drivers, nLaps):
    replay_file = open(FC.REPLAY_DIR + "replayFile.txt", "w")
    data = "START %d %d " % (len(drivers), nLaps)
    for d in drivers:
        data += "%d;%s " % (d.starting_position, d.tyre)
    replay_file.write(data+'\n')
    return replay_file

def load_replay_file(drivers):
    try:
        with open(FC.REPLAY_DIR + "replayFile.txt", "r") as rf:
            data = {}
            line = next(rf).split()
            if line[0] != "START":
                ac.log("Replay file doesnt start with 'START' tag.")
                return
            totalDrivers = int(line[1])
            data['totalDrivers'] = totalDrivers
            data['nLaps'] = int(line[2])
            for i in range(3, 3+totalDrivers):
                line[i] = line[i].split(';')
                drivers[i-3].starting_position = int(line[i][0])
                drivers[i-3].tyre = line[i][1]
            for line in rf:
                line = line.split()
                if line[0] == "U": # normal update
                    update = [float(line[2])]
                    for i in range(3, 3+totalDrivers):
                        line[i] = line[i].split(';')
                        update.append([int(line[i][0]), float(line[i][1]), line[i][2], int(line[i][3]), bool(int(line[i][4])), int(line[i][5])])
                    if int(line[1]) not in data:
                        data[int(line[1])] = []
                    data[int(line[1])].append(update)
                elif line[0] == "FL": # TODO fastest lap
                    pass
                else:
                    ac.log("Replay file has wrong tag '%s'." % line[0])
                    return
            return data

    except FileNotFoundError:
        ac.log("Replay File not found.")

def lookup_data(lap, time, replay_data, drivers):
    it = bisect.bisect_left(replay_data[lap], [time])
    if it > len(replay_data[lap]): return
    data = replay_data[lap][it]
    for i in range(len(drivers)):
        drivers[i].timeDiff = data[i+1][1]
        drivers[i].tyre = data[i+1][2]
        drivers[i].pits = data[i+1][3]
        drivers[i].out = data[i+1][4]
        drivers[i].current_lap = data[i+1][5]
    return [data[i+1][0] for i in range(len(drivers))] # return new positions

