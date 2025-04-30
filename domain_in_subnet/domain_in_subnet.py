#!/usr/bin/env python3
"""
This script prints the subnets which the specified domain sits in.
The first argument to this script must be a FQDN of the server.
"""

from typing import Pattern
import dns.resolver
import requests
import re
import sys
import os

def domain_in_subnet(domain_name: str) -> None:
    ns_file: str = ''
    name_servers: set[str] = set()
    resolved_names: set[str] = set()
    subnets: set[str] = set()

    filename_p: Pattern = re.compile('^ns_ipv4(\\.txt)?$')
    comment_p: Pattern = re.compile('^#.*$')
    blank_p: Pattern = re.compile('^\\s$')
    ipv4_p: Pattern = \
            re.compile('^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}')
    
    # scan the current directory for the ns_ipv4 file
    with os.scandir('.') as it:
        for entry in it:
            if filename_p.match(entry.name):
                ns_file = entry.name
                break

    if ns_file:
        line: str = ''
        with open(ns_file, "r") as file:
            line = file.readline()
            while line:
                if comment_p.match(line) or blank_p.match(line): # skip blank lines and comments
                    line = file.readline()
                    continue
                m = ipv4_p.match(line)
                if m:
                    name_servers.add(m.group()) # add a valid IPv4 address
                    line = file.readline()
    else:
        name_servers.add('8.8.8.8') # default nameserver if the file not found

    for ns in name_servers:
        answer = dns.resolver.resolve_at(ns, domain_name, "A")
        for _ in answer:
            resolved_names.add(_.to_text())

    # use the IPv4 addresse to obtain the information from ICANN
    for ipv4_addr in resolved_names:
        r = requests.get(f'https://rdap.arin.net/registry/ip/{ipv4_addr}')
        r_json = r.json()
        subnet: str = ''
        for cidr in r_json["cidr0_cidrs"]:
            subnet = str(cidr["v4prefix"]) + '/' + str(cidr["length"])
            subnets.add(subnet)

    # print the result
    for _ in subnets:
        print(_)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('The name of the server is required.\nExiting...')
        sys.exit(1)
    domain_in_subnet(sys.argv[1])
