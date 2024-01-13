from typer import Typer, Argument, Option
from typing_extensions import Annotated

from modules import traceroute
from modules import port_scanner
from modules import network_scanner
from modules import arp_spoofer

app = Typer(rich_markup_mode="rich")


@app.command("traceroute")
def tracert(target: Annotated[str, Argument(help="Target IP/domain.")] = "",
            timeout: Annotated[int, Option(help="Timeout for receiving packets.")] = 5):
    """Trace the path of IP packets with its location."""
    traceroute.TracerouteWithMap(target, timeout)


@app.command("port-scanner")
def threaded_port_scanner(ip: Annotated[str, Argument(help="Target IP/domain.")] = '127.0.0.1',
                          ports: Annotated[str, Argument(help="Desired port range to scan (use start-end).")] = '1-1024', 
                          threads: Annotated[int, Option(help="Threads amount for the scanner process.")] = 20,
                          args: Annotated[str, Option(help="Other arguments for the scanner")] = ''):
    """Scan the given ports of the target address."""
    port_scanner.NmapPortScanner(ip, ports, threads, args)


@app.command("host-discovery")
def host_discovery(ip: Annotated[str, Argument(help="Target IP range (ex: 192.168.1.1/24).")] = "",
                   args: Annotated[str, Option(help="Other arguments for the scanner.")] = "-sn",
                   timing: Annotated[int, Option(help="[b]0[/b] (slower scans but harder to be detected) to [b]5[/b] (faster scans but very agressive).")] = 3):
    """Discover all devices on the local network."""
    network_scanner.NmapNetScanner(ip, timing, args)


@app.command("arp-spoofer")
def arp_poisoning(target: Annotated[str, Argument(help="Target IP.")] = "",
                  host: Annotated[str, Argument(help="Target host.")] = "",
                  timing: Annotated[int, Option(help="Timing between sending packets.")] = 2,
                  verbose: Annotated[bool, Option(help="Verbose flag.")] = 'False'):
    """Not working yet."""
    arp_spoofer.ScapyArpSpoofer(target, host, timing, verbose)



if __name__ == "__main__":
    app()

