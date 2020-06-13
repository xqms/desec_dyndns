#!/usr/bin/python3

import urllib.request
import socket
import requests

DOMAIN = 'DOMAIN_HERE'
USER = 'USER_HERE' # usually same as DOMAIN
TOKEN = 'TOKEN_HERE' # dns update token

with urllib.request.urlopen('https://checkipv6.dedyn.io/') as f:
    ipv6_addr = f.read().decode('utf8')

with urllib.request.urlopen('https://checkipv4.dedyn.io/') as f:
    ipv4_addr = f.read().decode('utf8')

try:
    ipv4_info = socket.getaddrinfo(DOMAIN, 80, socket.AF_INET, socket.SOCK_STREAM)
    if len(ipv4_info) == 0:
        raise RuntimeError(f"Could not resolve IPv4 address of {DOMAIN}")

    ipv4_resolve = ipv4_info[0][4][0]
except socket.gaierror as e:
    print(f'WARNING: No current IPv4 address for domain {DOMAIN}')
    print(f'Error message follows:\n{e}')
    ipv4_resolve = None

try:
    ipv6_info = socket.getaddrinfo(DOMAIN, 80, socket.AF_INET6, socket.SOCK_STREAM)
    if len(ipv6_info) == 0:
        raise RuntimeError(f"Could not resolve IPv6 address of {DOMAIN}")

    ipv6_resolve = ipv6_info[0][4][0]
except socket.gaierror as e:
    print(f'WARNING: No current IPv6 address for domain {DOMAIN}')
    print(f'Error message follows:\n{e}')
    ipv6_resolve = None

if ipv4_resolve != ipv4_addr or ipv6_resolve != ipv6_addr:
    print(f'Current public IPs: {ipv4_addr}, {ipv6_addr}')
    print(f'Current DNS resolution: {ipv4_resolve}, {ipv6_resolve}')
    url = f'https://update.dedyn.io/?myipv4={ipv4_addr}&myipv6={ipv6_addr}'
    print(f'Updating with {url}')
    response = requests.get(
            url,
            auth=requests.auth.HTTPBasicAuth(USER, TOKEN)
    )
    if response.status_code != 200:
        raise RuntimeError(f'Got response error {response.status_code} and content:\n{response.text}')

