import sys
from time import perf_counter

import ipwhois
from scapy.all import sr1
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import TCP, UDP, ICMP, IP, RandShort
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest

from src.modules.console.ArgParser import ArgParser


def get_args():
    """ Get arguments from command line """
    arg_parser = ArgParser(sys.argv[1:])
    try:
        args = arg_parser.parse()
    except ValueError as e:
        print(str(e))
        sys.exit()
    return args


def trace_route(args):
    """ Trace route """
    if args.protocol == 'udp':
        transport = UDP(dport=args.port) / \
                    DNS(rd=1, qd=DNSQR(qname='python.org'))
    elif args.protocol == 'tcp':
        transport = TCP(dport=args.port)
    elif args.protocol == 'icmp':
        if ':' in args.ip:
            transport = ICMPv6EchoRequest()
        else:
            transport = ICMP()
    AS = "[AS]" if args.verbose else ""

    print(
        f"traceroute to {args.ip} ({args.ip}), {args.number} hops max, {args.protocol} port {args.port}")
    print(f"{'NUM':<6} {'IP':<18} {'[TIME,ms]':<10} {AS:<10}")

    for ttl in range(1, args.number + 1):
        if ':' in args.ip:
            packet = IPv6(dst=args.ip, hlim=ttl, id=RandShort()) / transport
        else:
            packet = IP(dst=args.ip, ttl=ttl, id=RandShort()) / transport
        start_time = perf_counter()
        reply = sr1(packet, timeout=args.timeout, verbose=0)
        total_time = str(round((perf_counter() - start_time) * 1000, 3)) + "ms"
        if not reply:
            print(f"{ttl:<6} *")
        else:
            if args.verbose:
                whois = ipwhois.IPWhois(reply.src).lookup_whois()[
                    'asn'] if ttl != 1 else 'local'
                print(f"{ttl:<6} {reply.src:<18} {total_time:<10} {whois}")
            else:
                print(f"{ttl:<6} {reply.src:<18} {total_time:<10}")
            if reply.src == args.ip:
                break


def main():
    """ Main function """
    args = get_args()
    trace_route(args)


if __name__ == '__main__':
    try:
        main()
    except PermissionError:
        print('Permission denied, please use sudo')
    except KeyboardInterrupt:
        print('Interrupted by user')
        sys.exit()
