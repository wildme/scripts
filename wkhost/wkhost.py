#!/usr/bin/env python3
"""
Wake up a host by its MAC address.
"""
import sys
import os
import time
import re
from typing import Pattern
from wakeonlan import send_magic_packet

mac_addr: str = ''
ip_addr: str = ''
os_startup_time_in_sec: int = 5
ping_count: int = 2

def parse_config_file() -> None:
    line: str = ''
    m_str: str = ''
    cnt_p: Pattern = re.compile('[0-9]+')
    comment_p: Pattern = re.compile('^#.*$')
    blank_p: Pattern = re.compile('^\\s$')
    ipv4_p: Pattern = re.compile('([0-9]{1,3}\\.){3}([0-9]{1,3})')
    mac_p: Pattern = re.compile('([a-f0-9]{2}[-:]){5}[a-f0-9]{2}')

    with open('wkconf.txt', 'r') as file:
        line = file.readline()
        while line:
            # skip blank lines and comments
            if comment_p.match(line) or blank_p.match(line):
                line = file.readline()
                continue
            if line.startswith("OS_STARTUP_TIME_IN_SEC"):
                m_str = cnt_p.search(line)
                global os_startup_time_in_sec
                os_startup_time_in_sec = int(m_str.group())
                line = file.readline()
            if line.startswith("PING_COUNT"):
                m_str = cnt_p.search(line)
                global ping_count
                ping_count = int(m_str.group())
                line = file.readline()
            if line.startswith("IP_ADDR"):
                m_str = ipv4_p.search(line)
                global ip_addr
                ip_addr = m_str.group()
                line = file.readline()
            if line.startswith("MAC_ADDR"):
                m_str = mac_p.search(line)
                global mac_addr
                mac_addr = m_str.group()
                line = file.readline()

def update_countdown(cnt: int) -> None:
    sys.stdout.write('\b \b' * len(str(eval('cnt + 1'))))
    sys.stdout.write(str(cnt))
    sys.stdout.flush()
        
def main() -> None:
    host_status: str = "Offline"
    os_name: str = os.name
    global os_startup_time_in_sec
    global ping_count
    global ip_addr
    global mac_addr
        
    send_magic_packet(mac_addr)
    print("Sending a magic packet...")
    print("Waiting for system startup: %s" % (os_startup_time_in_sec,), end='', flush=True)
        
    for _ in range(os_startup_time_in_sec):
        if os_startup_time_in_sec > 0:
            time.sleep(1)
            os_startup_time_in_sec -= 1
        update_countdown(os_startup_time_in_sec)
    
    print("\bDone")
    print("Host status: ", end='', flush=True)

    if os_name == 'nt':
        ping_result = os.system(f'ping -4 -n {ping_count} {ip_addr} 1> nul')
    if os_name == 'posix':
        ping_result = os.system(f'ping -4 -c {ping_count} {ip_addr} > /dev/null')

    if ping_result == 0:
        host_status = "Online"
    print(host_status)
    input("Press Enter to exit...")
        
if __name__ == '__main__':
    parse_config_file()
    input_err_msg: str = """
        wkconf.txt. AVAILABLE PARAMETERS:
        MAC_ADDR - the MAC address of the host
        IP_ADDR - the IP address of the host
        PING_COUNT - number of ECHO_REQUEST packets to send (Default: 2)
        OS_STARTUP_TIME_IN_SEC - system startup time in sec (Default: 10)
        """

    if not mac_addr or not ip_addr:
        print("ERROR: MAC-address or IP-address is missing!")
        print(input_err_msg)
        time.sleep(2)
        sys.exit(1)
    main()
