import re
import typer
from rich import print
from typing_extensions import Annotated

from modules import traceroute
from modules import port_scanner
from modules import network_scanner
from modules import arp_spoofer

app = typer.Typer(rich_markup_mode="rich")


@app.command("traceroute")
def tracert(target: Annotated[str, typer.Argument(help="Target IP/domain.")] = '8.8.8.8',
             timeout: Annotated[int, typer.Option(help="Timeout for receiving packets.")] = 5):
    """ """
    traceroute.SocketTraceroute(target, timeout)


@app.command("port-scanner")
def threaded_port_scanner(ip: Annotated[str, typer.Argument(help="Target IP/domain.")] = '127.0.0.1',
                           args: Annotated[str, typer.Option(help="Arguments for the scanner")] = '',
                            ports: Annotated[str, typer.Option(help="Desired port range to scan.")] = '1-1024', 
                             threads: Annotated[int, typer.Option(help="Threads amount for the scanner process.")] = 20):
    """Scan the given ports of the target address."""
    ports_pattern = r'(\d+)[-,.;](\d+)'
    match = re.search(ports_pattern, ports)

    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        port_scanner.NmapPortScanner(ip, start, end, threads, args)

    else:
        raise ValueError("[!] Invalid port range, use 'start-end' or 'start,end'.")


@app.command("host-discovery")
def host_discovery(ip: Annotated[str, typer.Argument(help="Target IP range (ex: 192.168.1.1/24).", show_default=False)] = '192.168.1.1/24',
                    timing: Annotated[int, typer.Option(help="Scan parameters, from [b]0[/b] (slower but harder to be detected) to [b]5[/b] (fastest and most agressive).")] = 3,
                     args: Annotated[str, typer.Option(help="Other arguments for the scanner.")] = ""):
    """Discover all devices on the local network."""
    network_scanner.NmapNetScanner(ip, timing, args)


@app.command("arp-spoofer")
def arp_spoofer(target: Annotated[str, typer.Argument(help="")] = '192.168.1.1',
                 host: Annotated[str, typer.Argument(help="")] = '192.168.1.1',
                  verbose: Annotated[bool, typer.Option(help="")] = 'False'):
    """Not working yet."""
    arp_spoofer(target, host, verbose)



if __name__ == "__main__":
    app()
