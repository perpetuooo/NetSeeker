import typer
from typing_extensions import Annotated

from modules import traceroute
from modules import port_scanner
from modules import network_scanner
from modules import arp_spoofer

app = typer.Typer(rich_markup_mode="rich")


@app.command("traceroute")
def tracert(target: Annotated[str, typer.Argument(help="Target IP/domain.", show_default=False)],
             timeout: Annotated[int, typer.Option(help="Timeout for receiving packets.")] = 5):
    """Trace the path of IP packets with its location."""
    traceroute.TracerouteWithMap(target, timeout)


@app.command("port-scanner")
def threaded_port_scanner(ip: Annotated[str, typer.Argument(help="Target IP/domain (loopback for default).", show_default=False)] = '127.0.0.1',
                           ports: Annotated[str, typer.Option(help="Desired port range to scan (ex: 1-1024).", show_default=False)] = '1-1024', 
                            threads: Annotated[int, typer.Option(help="Threads amount for the scanner process.")] = 20,
                             args: Annotated[str, typer.Option(help="Other arguments for the scanner", show_default=False)] = ''):
    """Scan the given ports of the target address."""
    port_scanner.NmapPortScanner(ip, ports, threads, args)


@app.command("host-discovery")
def host_discovery(ip: Annotated[str, typer.Argument(help="Target IP range (ex: 192.168.1.1/24).", show_default=False)],
                    args: Annotated[str, typer.Option(help="Other arguments for the scanner.")] = "-sn",
                     timing: Annotated[int, typer.Option(help="[b]0[/b] (slower scans but harder to be detected) to [b]5[/b] (faster scans but very agressive).")] = 3):
    """Discover all devices on the local network."""
    network_scanner.NmapNetScanner(ip, timing, args)


@app.command("arp-spoofer")
def arp_poisoning(target: Annotated[str, typer.Argument(help="Target IP.", show_default=False)],
                   host: Annotated[str, typer.Argument(help="Target host (default gateway for default).", show_default=False)] = "",
                    timing: Annotated[int, typer.Option(help="Timing between sending packets.", show_default=False)] = 2,
                     verbose: Annotated[bool, typer.Option(help="Verbose flag.", show_default=False)] = 'False'):
    """Not working yet."""
    arp_spoofer.ScapyArpSpoofer(target, host, timing, verbose)



if __name__ == "__main__":
    app()
