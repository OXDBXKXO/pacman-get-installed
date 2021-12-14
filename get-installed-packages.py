#!/usr/bin/python

import os, re

# check if script is run as root
uid = os.getuid()

if uid != 0:
    print("Script must be run with sudo!")
    exit(1)

programs = []

with open("/var/log/pacman.log", 'r') as f:
    logs = f.readlines()

    for log in logs:
        log = log.strip()

        installed = re.search(r"installed ([^\s]+?)\s\(", log)
        if installed is not None and installed.group(1) not in programs:
            programs.append(installed.group(1))

        removed = re.search(r"removed ([^\s]+?)\s\(", log)
        if removed is not None:
            try:
                programs.remove(removed.group(1))
            except:
                pass

    f.close()

with open("installed.txt", 'w') as f:
    programs.sort()
    f.write('\n'.join(programs))
    f.close()