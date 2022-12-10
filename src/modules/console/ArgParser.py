import ipaddress
import socket
from argparse import ArgumentParser

from src.modules.console.DataArguments import DataArguments


class ArgParser:
    """ Argument Parser"""

    def __init__(self, args):
        self._parser = ArgumentParser(prog="TraceRoute",
                                      description="TraceRoute",
                                      )
        self._args = args
        self._add_arguments()

    def _add_arguments(self):
        """
        Add arguments to the parser
        """
        self._parser.add_argument("ip", type=str,  # required=True,
                                  help="IP address")
        self._parser.add_argument("protocol", type=str, metavar='protocol',
                                  default=['tcp', 'udp', 'icmp'],
                                  help="tcp/udp/icmp protocol")
        self._parser.add_argument("-t", "--timeout", dest="timeout",
                                  type=float, default=2.0,
                                  help="response timeout (2s by default)")
        self._parser.add_argument("-p", "--port", type=int, default=33434,
                                  dest="port",
                                  help="tcp/udp port (33434 by default)")
        self._parser.add_argument("-v", "--verbose", action="store_true",
                                  help="verbose mode - display the autonomous system number for each ip address")
        self._parser.add_argument("-n", "--number", default=30, type=int,
                                  dest="number",
                                  help="max number of requests (30 by default)")

    def is_correct_ip(self, ip: str):
        """ Checking the correctness of the IP address """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

        # try:
        #     correct_ip = ipaddress.ip_address(ip)
        # except ValueError:
        #     print('Invalid IP')
        #     sys.exit(-1)

    def is_correct_protocol(self, protocol: str):
        """ Checking the correctness of the protocol """
        return protocol in ['tcp', 'udp', 'icmp']

    def is_correct_timeout(self, timeout: float):
        """ Checking the correctness of the timeout """
        return timeout > 0

    def is_correct_port(self, port: int, protocol: str):
        """ Checking the correctness of the port """
        if protocol == 'icmp':
            return True
        return 0 <= port <= 65535

    def parse(self):
        """
        Parse arguments
        """
        args = self._parser.parse_args(self._args)
        if not self.is_correct_ip(args.ip):
            raise ValueError(f'IP address {args.ip} is not correct.')

        if not self.is_correct_protocol(args.protocol):
            raise ValueError(
                f'Protocol {args.protocol} is not correct. Protocol should be one of: tcp, udp, icmp.')

        if not self.is_correct_timeout(args.timeout):
            raise ValueError(
                f'Timeout {args.timeout} is not correct. Timeout should be positive.')

        if not self.is_correct_port(args.port, args.protocol):
            raise ValueError(
                f'Port {args.port} is not correct. Port should be in range (0, 65535).')

        if ':' not in args.ip:
            args.ip = socket.gethostbyname(args.ip)

        return DataArguments(args.ip, args.protocol, args.timeout,
                             args.verbose, args.port, args.number)
