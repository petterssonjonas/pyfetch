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
import os, re, subprocess, socket, time, psutil, pyfetchconf

"""
Check out tabulate (pretty print 2d lists as tables)
and colorama
tqdm: progress bars

https://towardsdatascience.com/7-cool-python-tricks-that-you-probably-didnt-know-634ae56112be


Function to choose outputs, check how many there are and make BLOCKS print the same number for the zip. Or just zip func for ASCII art? Add * ~ | or whatever in front of lines?



"""


# make if needed import thing
# if configured import pytz

# Raspian returns linux2. wtf. Any other distros that returns smt else?
if os.sys.platform != "linux":
    print("Mac is bad for you.")
    exit()


# Declare colors. Put in config?
# Cursive isnt supported on all terminals by default. Might have to compile
# terminfo with support for it.
# Shouldnt be a problem. Maybe prints background or underlined, idk.
# Want to use ligatures, but few ppl have the fonts and terminfo for it.
clear = "\033[0m"
cursive = "\033[3m"
color_arch = "\033[38;2;0;119;169m"
# Shorten for readability
q = cursive + color_arch
w = clear  # needed?
# Convert to ascii. No i dont wanna use colored or colorful or whatever.
# color_gentoo = "#40375C"
# color_ubuntu = "#E6491E"
# color_fedora = "#234071"
# color_manjaro = "#00BF60"
# color_mint = "#80CF46"
# color_redhat = "#F32F10"
# theme_gruvbox
# theme_solarized
# notheme?

UNITS = [
    q + "k",
    q + "M",
    q + "G",
    q + "T",
    q + "P",
]


# Make a process runner
# def runner():
#    with os.system("lspci") as f:
#        find = int(f.readline().split)
#        return find

# Nice short way of getting human readable units from the bytes given by psutil.
# Kinda proud of this one... Change 1024 to 1000 if you are so inclined.
def human_size(s):
    for u in UNITS:
        s = s / 1024
        if s < 1024:
            return "{0:.0f}{1}".format(s, u) + "B"


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


# def cpu_name():
#     c = cpuinfo.get_cpu_info()["brand"].split(" ")
#     n = c[2], c[4], c[5]
#     e = str(" ".join(n))
#     return e


# def scan_lines_equal_to(string, fp):
#     for line in fp:
#     if line == string:
#     yield line
#
#
# def cpu_name():
#     with open("/proc/cpuinfo", "r") as fp:
#     for line in scan_lines_equal_to("model name", fp):
#     return line


def cpu_name():
    lscpu = subprocess.check_output("lscpu", shell=True).strip().decode()
    for line in lscpu.split("\n"):
        if "Model name" in line:
            m = re.sub(".*model name.*:", "", line, 1).split()
            e = m[4], m[6], m[7]
            o = str(" ".join(e))
            return o


def kernel():
    k = os.uname().release
    return k


def get_packages():
    p = os.popen("pacman -Q | wc -l").read().rstrip("\n")
    return p


# Other "popular" ways return terminfo. This is better.
# Gotta look at the os.env-code...
def terminal():
    t = os.environ.get("TERMINAL")
    return t


def shell():
    s = os.environ.get("SHELL").split("/")[-1]
    return s


# Maybe rewrite this to use uname.uptime or some other way of getting y,m,w,d,h,m
# /proc/uptime returns seconds. if u want sec add "%02d" and (sec) to return
# This makes cython convert/compile fail, smt about float. fix later.
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


# pci registry
def gpu_name():
    gpu = ""
    lspci = subprocess.check_output("lspci", shell=True).strip().decode()
    for line in lspci.split("\n"):
        if "VGA" in line:
            vga = re.sub(".*.VGA.*.*: ", "", line, 1)
            if "NVIDIA" in vga:
                g = re.sub("NVIDIA\sCorporation\s\w[a-zA-Z]\d*\s\W", "", vga, 1)
                gpu = re.sub("(])\W\W(rev a\d\W)", "", g, 1)
            if "AMD" in vga:
                gpu = "go green"
    return gpu


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
    t = psutil.sensors_temperatures()
    return "Not implemented"


# Out and text needs to be the same line count. make smt for this?
OUT = """
\033[3;37m{hostname}                                           
\033[3m{datetime}                                              
\033[3m\033[38;2;0;119;169mKernel:\033[0m   {kernel}           
\033[3m\033[38;2;0;119;169mUptime:\033[0m   {uptime}           
\033[3m\033[38;2;0;119;169mPackages:\033[0m {get_packages}     
\033[3m\033[38;2;0;119;169mTerminal:\033[0m {terminal}         
\033[3m\033[38;2;0;119;169mShell:\033[0m    {shell}            
\033[3m\033[38;2;0;119;169mCPU:\033[0m      {cpu_name}         
\033[3m\033[38;2;0;119;169mCPU Load:\033[0m {cpu_use}{loadavg} 
\033[3m\033[38;2;0;119;169mGPU:\033[0m      {gpu_name}         
\033[3m\033[38;2;0;119;169mRam:\033[0m      {ram}              
\033[3m\033[38;2;0;119;169mDiskspace:\033[0m                   
\033[3m\033[38;2;0;119;169mRoot:\033[0m     {diskspace_root}   
\033[3m\033[38;2;0;119;169mHome:\033[0m     {diskspace_home}   
\033[3m\033[38;2;0;119;169mSSD:\033[0m      {diskspace_custom1}
\033[3m\033[38;2;0;119;169mHDD:\033[0m      {diskspace_custom2}
\033[3m\033[38;2;0;119;169mCPU Temp:\033[0m {cpu_temp}         
\033[3m\033[38;2;0;119;169mCPU Fan:\033[0m  {cpu_fan}          


"""

# OUT.count("\n")) # Counts newlines in OUT

ART = pyfetchconf.LOGO

def add_glam():
    for line in OUT.count("\n"):
        print("*")
    return line


TEXT = OUT.format(
    datetime=datetime(),
    hostname=host_name(),
    kernel=kernel(),
    uptime=uptime(),
    get_packages=get_packages(),
    terminal=terminal(),
    shell=shell(),
    cpu_name=cpu_name(),
    cpu_use=cpu_use(),
    loadavg=loadavg(),
    gpu_name=gpu_name(),
    ram=ram(),
    diskspace_root=diskspace_root(),
    diskspace_home=diskspace_home(),
    diskspace_custom1=diskspace_custom1(),
    diskspace_custom2=diskspace_custom2(),
    cpu_temp=cpu_temp(),
    cpu_fan=cpu_fan(),
)

# Is this the best way of doing this?

def zip_art_text():
    BLOCKS = [ART, TEXT]
    block_split = [b.split("\n") for b in BLOCKS]
    zipped = zip(*block_split)
    for elements in zipped:
        print("".join(elements))


if pyfetchconf.LOGO == 0:
    print(TEXT)
else:
    zip_art_text()


