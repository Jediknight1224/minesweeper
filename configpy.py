import os, configparser

def saveConfig(*args):
    rows, cols, mines, custom_sizes = args
    config = configparser.ConfigParser()
    config.add_section("game")
    config.set("game", "rows", str(rows))
    config.set("game", "cols", str(cols))
    config.set("game", "mines", str(mines))
    config.add_section("sizes")
    config.set("sizes", "amount", str(min(5, len(custom_sizes))))
    for x in range(0,min(5,len(custom_sizes))):
        config.set("sizes", "row"+str(x), str(custom_sizes[x][0]))
        config.set("sizes", "cols"+str(x), str(custom_sizes[x][1]))
        config.set("sizes", "mines"+str(x), str(custom_sizes[x][2]))

    with open("config.ini", "w") as file:
        config.write(file)

def loadConfig(custom_sizes):
    config = configparser.ConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        custom_sizes.append((config.getint("sizes", "row"+str(x)), config.getint("sizes", "cols"+str(x)), config.getint("sizes", "mines"+str(x))))
    return rows, cols, mines
