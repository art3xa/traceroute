# TraceRoute

Traceroute with the ability to send packets via ICMP, TCP or UDP, timeout
support and ASN lookup

# Usage

Install requirements:
`pip install -r requirements.txt`

Run:
`python traceroute.py [OPTIONS] IP_ADDRESS {tcp|udp|icmp}`

# Options

Options `[OPTIONS]` must be the following:

`-t, --timeout` — response timeout (2s by default)

`-v, --verbose` — verbose mode - display the autonomous system number for each
ip address

`-p, --port` — tcp/udp port (33434 by default)

`-n, --number` — max number of requests (30 by default)

# Examples

`python traceroute.py -p 53 1.1.1.1 tcp`

`python traceroute.py -p 53 8.8.8.8 udp -v`

`python traceroute.py -p 53 1.1.1.1 tcp -v -t 5 -n 60`

## Functionality

- Base traceroute functionality
- TCP, UDP and ICMP support
- IPv6 support
- Verbose mode - output of the autonomous system number for each address using
  the Whois protocol.

# Requirements

- Python 3.8+
- ipwhois~=1.2.0
- scapy~=2.4.5

