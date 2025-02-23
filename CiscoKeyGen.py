#! /usr/bin/python3
import os
import socket
import hashlib
import struct

# get the host id and host name to calculate the hostkey
hostid = os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey = int(hostid, 16)

for x in hostname:
    ioukey = ioukey + ord(x)

print("hostid=" + hostid + ", hostname=" + hostname + ", ioukey=" + hex(ioukey)[2:])

# Create the license using md5sum
iouPad1 = b'\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
iouPad2 = b'\x80' + 39 * b'\0'

md5input = iouPad1 + iouPad2 + struct.pack('!L', ioukey) + iouPad1
iouLicense = hashlib.md5(md5input).hexdigest()[:16]

# add license info to $HOME/.iourc
print("\n*********************************************************************")
print("Create the license file $HOME/.iourc with this command:")
print(" echo -e '[license]\\n" + hostname + " = " + iouLicense + ";'" + " | tee $HOME/.iourc ")
print("\nThe command adds the following text to $HOME/.iourc:")
print("[license]\n" + hostname + " = " + iouLicense + ";")

# disable phone home feature
print("\n*********************************************************************")
print("Disable the phone home feature with this command:")
print(" grep -q -F '127.0.0.1 xml.cisco.com' /etc/hosts || echo '127.0.0.1 xml.cisco.com' | sudo tee -a /etc/hosts")
print("\nThe command adds the following text to /etc/hosts:")
print("127.0.0.1 xml.cisco.com")
print("\n*********************************************************************")
