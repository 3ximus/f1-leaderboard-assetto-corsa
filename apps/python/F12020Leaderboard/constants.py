
APP_NAME = "F12020Leaderboard"

class FC:
    APP_NAME = APP_NAME
    FONT_NAME = "Orbitron"

    # IMAGES
    LEADERBOARD_POSITION_LABEL = ["apps/python/%s/ui/positions/%d.png" % (APP_NAME, n) for n in range(20)]
    LEADERBOARD_POSITION_RED_LABEL = ["apps/python/%s/ui/positions/%d_red.png" % (APP_NAME, n) for n in range(20)]
    LEADERBOARD_POSITION_GREEN_LABEL = ["apps/python/%s/ui/positions/%d_green.png" % (APP_NAME, n) for n in range(20)]

    LEADERBOARD_BACKGROUND = "apps/python/%s/ui/background.png" % APP_NAME
    LEADERBOARD_BASE_RACE = "apps/python/%s/ui/race_base.png" % APP_NAME 
    LEADERBOARD_BASE_QUALI = "apps/python/%s/ui/quali_base.png" % APP_NAME 

    LEADERBOARD_INFO_BACKGROUNG = "apps/python/%s/ui/background_info.png" % APP_NAME

    LEADERBOARD_FASTEST_LAP =  "apps/python/%s/ui/fastest_lap.png" % APP_NAME
    FASTEST_LAP_BANNER =  "apps/python/%s/ui/fastest_lap_banner.png" % APP_NAME

    TEAM_COLORS = None
    TEAM_NAME = None

    ROLEX_LOGO = "apps/python/%s/ui/rolex.png" % APP_NAME
    DRIVER_WIDGET_BACKGROUND = "apps/python/%s/ui/driver_widget_background.png" % APP_NAME
    DRIVER_WIDGET_BACKGROUND_ALTERNATE = "apps/python/%s/ui/driver_widget_background_alternate.png" % APP_NAME
    DRIVER_WIDGET_EXTENDED_BACKGROUND = "apps/python/%s/ui/driver_widget_extended_background.png" % APP_NAME

    TYRE_BASE_NAME = "apps/python/%s/ui/tyres/" % APP_NAME

    POSITION_GAINED = "apps/python/%s/ui/position_gained.png" % APP_NAME
    POSITION_LOST = "apps/python/%s/ui/position_lost.png" % APP_NAME
    POSITION_MAINTAINED = "apps/python/%s/ui/position_maintained.png" % APP_NAME

    # CONSTANTS
    OVERTAKE_POSITION_LABEL_TIMER = 3 # seconds
    FASTEST_LAP_DISPLAY_TIME = 8
    FASTEST_LAP_STARTING_LAP = 1 # TODO CHANGE THIS AFTER TESTING


try:
    if not FC.TEAM_COLORS:
        FC.TEAM_COLORS = {}
        FC.TEAM_NAME = {}
        FC.DRIVER_NUMBER = {}
        with open("apps/python/%s/teams.ini" % APP_NAME) as fp:
            for line in fp:
                line = line.split(":")
                FC.TEAM_COLORS[line[-1][:-1]] = "apps/python/%s/ui/teams/%s.png" % (APP_NAME, line[1])
                FC.TEAM_NAME[line[-1][:-1]] = line[0]
                FC.DRIVER_NUMBER[line[-1][:-1]] = line[2]
except FileNotFoundError:
    pass