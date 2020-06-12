
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

    TEAM_COLORS = None
    TEAM_NAME = None

    ROLEX_LOGO = "apps/python/%s/ui/rolex.png" % APP_NAME
    DRIVER_WIDGET_BACKGROUND = "apps/python/%s/ui/driver_widget_background.png" % APP_NAME

    # CONSTANTS
    OVERTAKE_POSITION_LABEL_TIMER = 3 # seconds


try:
    if not FC.TEAM_COLORS:
        FC.TEAM_COLORS = {}
        FC.TEAM_NAME = {}
        with open("apps/python/%s/teams.txt" % APP_NAME) as fp:
            for line in fp:
                line = line.split(":")
                FC.TEAM_COLORS[line[-1][:-1]] = "apps/python/%s/ui/tags/tag_%s.png" % (APP_NAME, line[1])
                FC.TEAM_NAME[line[-1][:-1]] = line[0]
except FileNotFoundError:
    pass