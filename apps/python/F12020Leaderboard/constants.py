import ac

APP_NAME = "F12020Leaderboard"

class FC:
    APP_NAME = APP_NAME
    FONT_NAME = "Orbitron"

    # IMAGES

    # POSITION NUMBERS
    LEADERBOARD_POSITION_LABEL = ["apps/python/%s/ui/positions/%d.png" % (APP_NAME, n) for n in range(20)]
    LEADERBOARD_POSITION_RED_LABEL = ["apps/python/%s/ui/positions/%d_red.png" % (APP_NAME, n) for n in range(20)]
    LEADERBOARD_POSITION_GREEN_LABEL = ["apps/python/%s/ui/positions/%d_green.png" % (APP_NAME, n) for n in range(20)]

    # LEADERBOARD BACKGROUNDS
    LEADERBOARD_BACKGROUND = "apps/python/%s/ui/background.png" % APP_NAME
    LEADERBOARD_BASE_RACE = "apps/python/%s/ui/race_base.png" % APP_NAME 
    LEADERBOARD_BASE_QUALI = "apps/python/%s/ui/quali_base.png" % APP_NAME 
    LEADERBOARD_INFO_BACKGROUNG = "apps/python/%s/ui/background_info.png" % APP_NAME

    # FASTEST LAP
    LEADERBOARD_FASTEST_LAP =  "apps/python/%s/ui/fastest_lap.png" % APP_NAME
    FASTEST_LAP_BANNER =  "apps/python/%s/ui/fastest_lap_banner.png" % APP_NAME

    # DRIVER WIDGET BACKGROUND
    DRIVER_WIDGET_BACKGROUND = "apps/python/%s/ui/driver_widget_background.png" % APP_NAME
    DRIVER_WIDGET_BACKGROUND_ALTERNATE = "apps/python/%s/ui/driver_widget_background_alternate.png" % APP_NAME
    DRIVER_WIDGET_EXTENDED_BACKGROUND = "apps/python/%s/ui/driver_widget_extended_background.png" % APP_NAME

    # FLAGS
    YELLOW_FLAG = "apps/python/%s/ui/yellow_flag.png" % APP_NAME
    YELLOW_FLAG_SECTOR1 = "apps/python/%s/ui/yellow_flag_s1.png" % APP_NAME
    YELLOW_FLAG_SECTOR2 = "apps/python/%s/ui/yellow_flag_s2.png" % APP_NAME
    YELLOW_FLAG_SECTOR3 = "apps/python/%s/ui/yellow_flag_s3.png" % APP_NAME
    GREEN_FLAG = "apps/python/%s/ui/green_flag.png" % APP_NAME
    RACE_FLAG = "apps/python/%s/ui/race_flag.png" % APP_NAME

    # POSITION CHANGED INDICATOR
    POSITION_GAINED = "apps/python/%s/ui/position_gained.png" % APP_NAME
    POSITION_LOST = "apps/python/%s/ui/position_lost.png" % APP_NAME
    POSITION_MAINTAINED = "apps/python/%s/ui/position_maintained.png" % APP_NAME

    # MISCELANEOUS
    ROLEX_LOGO = "apps/python/%s/ui/rolex.png" % APP_NAME

    TYRE_BASE_NAME = "apps/python/%s/ui/tyres/" % APP_NAME

    # REPLAY DIRECTORY
    REPLAY_DIR = "apps/python/%s/replays/" % APP_NAME

    # CONSTANTS
    OVERTAKE_POSITION_LABEL_TIMER = 3 # seconds
    FASTEST_LAP_DISPLAY_TIME = 8
    FASTEST_LAP_STARTING_LAP = 2
    TRACK_SECTION_LENGTH = 110

    TEAM_COLORS = None
    TEAM_NAME = None
    DRIVER_NUMBER = None
    NUMBER_TAGS = None

try:
    if not FC.TEAM_COLORS:
        FC.TEAM_COLORS = {}
        FC.TEAM_NAME = {}
        FC.DRIVER_NUMBER = {}
        FC.NUMBER_TAGS = {}
        with open("apps/python/%s/teams.ini" % APP_NAME) as fp:
            for line in fp:
                line = line.split(":")
                name = line[-1][:-1]
                FC.TEAM_NAME[name] = line[0]
                FC.TEAM_COLORS[name] = "apps/python/%s/ui/teams/%s.png" % (APP_NAME, line[1])
                FC.DRIVER_NUMBER[name] = line[2]
                FC.NUMBER_TAGS[name] = "apps/python/%s/ui/numbers/%s.png" % (APP_NAME, line[2])
except FileNotFoundError:
    ac.log("File teams.ini not found.")