#!/usr/bin/env python
# -*- coding: utf-8 -*-
#              _____    _       _
#  _ __  _   _|  ___|__| |_ ___| |__
# | '_ \| | | | |_ / _ \ __/ __| '_ \   https://gitlab.com/fuzebox/pyfetch
# | |_) | |_| |  _|  __/ || (__| | | |
# | .__/ \__, |_|  \___|\__\___|_| |_|
# |_|    |___/ Yet another Linux system information fetcher.
#              Inspired by Neofetch (Bash), pfetch (bash), screenfetch (Bash),
#              paleofetch (C), pyFetch (py, by bn0x unmentained), pyfetch (py, pip
#              -package-fetcher).
#              pyFetch is meant to be more configurable than most others.
#              As a every time i open a terminal execution i would recomend using
#              Paleofetch, it is extremly fast.
#
# Trying to use as few modules as possible.
# Could go without subprocess but it is the recommended and fastest
# way of getting what we need. I should time the diff...
# os.uname().nodename truncates hostname to 8 characters on some systems
# so importing socket to get around that.
import os, subprocess, socket, time, psutil

# make if needed import thing
# if configured import pytz

# Raspian returns linux2. wtf. Any other distros that returns smt else?
if os.sys.platform != "linux":
    print("Mac is bad for you.")
    exit()


# Declare colors. Put in config?
clear = "\033[0m"
cursive = "\033[3m"
color_arch = "\033[38;2;0;119;169m"
# Shorten for readability
q = cursive + color_arch
w = clear
# Convert to ascii. No i dont wanna use colored or colorful or whatever.
# color_gentoo = "#40375C"
# color_ubuntu = "#E6491E"
# color_fedora = "#234071"
# color_manjaro = "#00BF60"
# color_mint = "#80CF46"
# color_redhat = "#F32F10"
# theme_gruvbox
# theme_solarized

# Man Black code formatting is annoying sometimes. Still best methinks.
UNITS = [
    q + "kB",
    q + "MB",
    q + "GB",
    q + "TB",
    q + "PB",
]

# Nice short way of getting human readable units from the bytes given by psutil.
# Kinda proud of this one... Change 1024 to 1000 if you are so inclined.
def human_size(s):
    for u in UNITS:
        s = s / 1024
        if s < 1024:
            return "{0:.0f}{1}".format(s, u)

# Gather some defs into one


# socket.gethostname is recomended. wish i didnt have to import it.
# os.uname().nodename truncates hostname to 8 characters on some systems
def host_name():
    userathost = "\033[3;37m" + os.getlogin(), "\033[3;37m" + socket.gethostname()
    return "\033[3m\033[38;2;0;119;169m@".join(userathost)


# Simple way of getting system time.
def datetime():
    t = time.localtime()
    t = time.strftime("%a %b %d %Y, \033[3;37m\033[38;2;0;119;169m%H:%M:%S", t)
    return t


# If you want to define a timezone you can use this instead. import pytz too.
# def timezone():
#     timezone = pytz.timezone(TIMEZONE)
#     timehere = datetime.now(timezone)
#     time = timehere.strftime("%a %b %d %Y, \033[3;37m\033[38;2;0;119;169m%H:%M:%S")
#     return timezone

# Make a process runner
# def runner():
#    with os.system("lspci") as f:
#        find = int(f.readline().split)
#        return find


def cpu_name():
    #    with open ("/proc/cpuinfo", "r") as f:
    #        find = int(f.readline().split)
    return "Not implemented"


def kernel():
    k = os.uname().release
    return k


def get_packages():
    return "Not implemented"


def terminal():
    t = os.environ.get("TERMINAL")
    return t


def shell():
    s = os.environ.get("SHELL").split("/")[-1]
    return s


# Maybe rewrite this to use uname.uptime or some other way of getting y,m,w,d,h,m
# /proc/uptime returns seconds. if u want sec add "%02d" and (sec) to return
def uptime():
    with open("/proc/uptime", "r") as f:
        sec = float(f.readline().split()[0])
        min, sec = divmod(sec, 60)
        hour, min = divmod(min, 60)
    return (
        "%d\033[3m\033[38;2;0;119;169mh\033[0m %02d\033[3m\033[38;2;0;119;169mmin"
        % (hour, min)
    )


# Is this needed? Load avg is probably more usable. Read up on what psutil percent returns.
def cpu_use():
    c = psutil.cpu_percent()
    return str(c) + "\033[3m\033[38;2;0;119;169m%\033[0m "


# Pretty this up. colors? better way? os.uname(?) can return week etc
def loadavg():
    s = os.getloadavg()
    l = []
    l = str(s[0]), str(s[1]), str(s[2])
    return "1 min avg: " + l[0]  # + " 5m: " + l[1] + " 15m: " + l[2]


def ram():
    r = psutil.virtual_memory()
    return (
        str(r.percent)
        + "\033[3m\033[38;2;0;119;169m%\033[0m of "
        + human_size(r.total)
        + " "
    )


def gpu_name():
    return "Not Implemented"


# make mount points reader or smt. Or be lazy and just make config for points.
def diskspace_root():
    d = psutil.disk_usage("/")
    return (
        str(d.percent)
        + "\033[3m\033[38;2;0;119;169m%\033[0m of "
        + human_size(d.total)
        + " "
    )


def diskspace_home():
    d = psutil.disk_usage("/home")
    return (
        str(d.percent)
        + "\033[3m\033[38;2;0;119;169m%\033[0m of "
        + human_size(d.total)
        + " "
    )


def diskspace_custom1():
    d = psutil.disk_usage("/media/ssd1")
    return (
        str(d.percent)
        + "\033[3m\033[38;2;0;119;169m%\033[0m of "
        + human_size(d.total)
        + " "
    )


def diskspace_custom2():
    d = psutil.disk_usage("/media/hdd")
    return (
        str(d.percent)
        + "\033[3m\033[38;2;0;119;169m%\033[0m of "
        + human_size(d.total)
        + " "
    )


def cpu_temp():
    return "Not implemented"


def cpu_fan():
    return "Not implemented"


# Out and text needs to be the same line count. make smt for this?
OUT = """
\033[3;37m{hostname}\033[0m
\033[3m{datetime}\033[0m
\033[3m\033[38;2;0;119;169mKernel:\033[0m   {kernel}
\033[3m\033[38;2;0;119;169mUptime:\033[0m   {uptime}
\033[3m\033[38;2;0;119;169mTerminal:\033[0m {terminal}
\033[3m\033[38;2;0;119;169mShell:\033[0m    {shell}
\033[3m\033[38;2;0;119;169mCPU Load:\033[0m {cpu_use}{loadavg}
\033[3m\033[38;2;0;119;169mRam:\033[0m      {ram}
\033[3m\033[38;2;0;119;169mDiskspace:\033[0m
\033[3m\033[38;2;0;119;169mRoot:\033[0m     {diskspace_root}
\033[3m\033[38;2;0;119;169mHome:\033[0m     {diskspace_home}
\033[3m\033[38;2;0;119;169mSSD:\033[0m      {diskspace_custom1}
\033[3m\033[38;2;0;119;169mHDD:\033[0m      {diskspace_custom2}




"""

"""
\033[3m\033[38;2;0;119;169mCPU:\033[0m      {cpu_name}
\033[3m\033[38;2;0;119;169mTemp and fans:\033[0m
\033[3m\033[38;2;0;119;169mCPU Temp:\033[0m {cpu_temp}
\033[3m\033[38;2;0;119;169mCPU Fan:\033[0m  {cpu_fan}
"""

LOGO = """
\033[3m\033[38;2;0;119;169m               #               \033[0m
\033[3m\033[38;2;0;119;169m              ###              \033[0m
\033[3m\033[38;2;0;119;169m             #####             \033[0m
\033[3m\033[38;2;0;119;169m             ######            \033[0m
\033[3m\033[38;2;0;119;169m            ; #####;           \033[0m
\033[3m\033[38;2;0;119;169m           +##.#####           \033[0m
\033[3m\033[38;2;0;119;169m          +##########          \033[0m
\033[3m\033[38;2;0;119;169m         #############;        \033[0m
\033[3m\033[38;2;0;119;169m        ###############+       \033[0m
\033[3m\033[38;2;0;119;169m       #######   #######       \033[0m
\033[3m\033[38;2;0;119;169m     .######;     ;###;`'.     \033[0m
\033[3m\033[38;2;0;119;169m    .#######;     ;#####.      \033[0m
\033[3m\033[38;2;0;119;169m    #########.   .########`    \033[0m
\033[3m\033[38;2;0;119;169m   ######'           '######   \033[0m
\033[3m\033[38;2;0;119;169m  ;####                 ####;  \033[0m
\033[3m\033[38;2;0;119;169m  ##'                     '##  \033[0m
\033[3m\033[38;2;0;119;169m #'                         `# \033[0m
"""

TEXT = OUT.format(
    datetime=datetime(),
    hostname=host_name(),
    kernel=kernel(),
    uptime=uptime(),
    terminal=terminal(),
    shell=shell(),
    cpu_name=cpu_name(),
    cpu_use=cpu_use(),
    loadavg=loadavg(),
    ram=ram(),
    diskspace_root=diskspace_root(),
    diskspace_home=diskspace_home(),
    diskspace_custom1=diskspace_custom1(),
    diskspace_custom2=diskspace_custom2(),
    cpu_temp=cpu_temp(),
    cpu_fan=cpu_fan(),
)

# Is this the best way of doing this?
BLOCKS = [LOGO, TEXT]
block_split = [b.split("\n") for b in BLOCKS]
zipped = zip(*block_split)

for elems in zipped:
    print("".join(elems))
