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

def find_the_config_file() -> str:
    # scan the current directory for the ns_ipv4 file
    filename_p: Pattern = re.compile('^ns_ipv4(\\.txt)?$')

    with os.scandir('.') as it:
        for entry in it:
            if filename_p.match(entry.name):
                return entry.name
    return ''

def parse_the_config_file(cfg_file:str) -> set[str]:
    line: str = ''
    name_servers: set[str] = set()
    comment_p: Pattern = re.compile('#.*')
    blank_p: Pattern = re.compile('\\s')
    ipv4_p: Pattern = re.compile('([0-9]{1,3}\\.){3}([0-9]{1,3})')

    with open(cfg_file, "r") as file:
        line = file.readline()
        while line:
            # skip blank lines and comments
            if comment_p.match(line) or blank_p.match(line):
                line = file.readline()
                continue
            m = ipv4_p.match(line)
            if m:
                # add a valid IPv4 address
                name_servers.add(m.group())
                line = file.readline()
    return name_servers

def get_subnets_from_db(ipv4_addrs: set[str]) -> set[str]:
    subnets: set[str] = set()

    # use the IPv4 addresse to obtain the information from ICANN
    for ipv4_addr in ipv4_addrs:
        r = requests.get(f'https://rdap.arin.net/registry/ip/{ipv4_addr}')
        r_json = r.json()
        subnet: str = ''
        for cidr in r_json["cidr0_cidrs"]:
            subnet = str(cidr["v4prefix"]) + '/' + str(cidr["length"])
            subnets.add(subnet)
    return subnets

def main(domain_name: str) -> None:
    name_servers: set[str] = set()
    resolved_names: set[str] = set()
    ns_file: str = find_the_config_file()

    if ns_file:
        name_servers = parse_the_config_file(ns_file)
    else:
        # default nameserver if file doesn't exist
        name_servers.add('8.8.8.8')

    for ns in name_servers:
        answer = dns.resolver.resolve_at(ns, domain_name, "A")
        for _ in answer:
            resolved_names.add(_.to_text())

    # print the result
    for _ in get_subnets_from_db(resolved_names):
        print(_)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('The name of the server is required.\nExiting...')
        sys.exit(1)
    main(sys.argv[1])
