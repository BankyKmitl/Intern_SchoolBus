#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import os
import sys
import time
import datetime
import pyshark
import subprocess
import MySQLdb
from bluepy import btle


if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.getValueText(9) is not None:
            if 'TAG' in dev.getValueText(9):
                if isNewDev:
                    status = "new"
                elif isNewData:
                    if self.opts.new:
                        return
                    status = "update"
                else:
                    if not self.opts.all:
                        return
                    status = "old"

                if dev.rssi < self.opts.sensitivity:
                    return

                print(datetime.datetime.now().strftime("%A, %d %B %Y %I:%M%p") + ' | Device : %s (%s), %d dBm' %
                      (ANSI_WHITE + dev.addr + ANSI_OFF,
                       dev.getValueText(9),
                       dev.rssi))
                if not dev.scanData:
                    print('\t(no data)')
                print
            else:
                return


def connect(devices):
    print(ANSI_YELLOW + "Connecting to Devices..." + ANSI_OFF)

    for d in devices:
        if d.getValueText(9) == 'iTAG':
            if d.connectable:
                print("    Connecting to", ANSI_WHITE + d.addr + ANSI_OFF + ":")
                dev = btle.Peripheral(d)
                time.sleep(1)
                dev.disconnect()
                time.sleep(2)


def scan():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--hci', action='store', type=int, default=0,
                        help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=60,
                        help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Display duplicate adv responses, by  default show new + updated')
    parser.add_argument('-n', '--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity')
    arg = parser.parse_args(sys.argv[1:])

    btle.Debugging = arg.verbose

    #get Raspberry Pi Mac Address
    bus_rpi_mac = subprocess.check_output(
        ["cat", "/sys/class/bluetooth/hci0/address"])
    bus_rpi_mac = bus_rpi_mac[:-1]

    #connect to Mysql Database
    db = MySQLdb.connect(host="52.77.27.5",
                         port=12345,
                         user="schoolbus",
                         passwd="password4schoolbus",
                         db="schoolbus")
    cursor = db.cursor()

    while True:

        print("\n" + ANSI_RED + "Scanning for devices..." + ANSI_OFF)
        scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))
        devices = scanner.scan(arg.timeout)

        itag_amount = 0

        for d in devices:
            if d.getValueText(9) is not None:
                if 'TAG' in d.getValueText(9):
                    itag_amount += 1
                    cursor.execute("INSERT INTO school_bus_scan_data (rpi_mac, itag_mac,time, rssi) VALUES (%s,%s,%s,%s)", (
                        bus_rpi_mac, d.addr, datetime.datetime.now(), d.rssi))
                    print('insert complete')
        db.commit()

        print('Device Found : %s \n', itag_amount)

        if arg.discover:
            connect(devices)


if __name__ == '__main__':
    scan()
