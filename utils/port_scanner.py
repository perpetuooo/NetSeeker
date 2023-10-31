import sys
import time
import nmap
from rich import print
from rich.table import Table
from concurrent.futures import ThreadPoolExecutor

def NmapPortScanner(target, start, end, threads):

    def scanner(port):
        try:
            result = nm.scan(str(target), str(port))

            port_status = (result['scan'][target]['tcp'][port]['state'])
            port_state = (result['scan'][target]['tcp'][port]['state'])
            port_service = (result['scan'][target]['tcp'][port]['name'])

            if port_status == "open":
                table.add_row(str(port), port_state, port_service)

        except Exception as e:
            print(f"[bold red][!] ERROR: {str(e)}[/bold red]")
            sys.exit(1)
        
        except KeyboardInterrupt:
            sys.exit()


    print(f"[bold yellow][-] Scanning ports {start} to {end} on {target}...[/bold yellow]\n")

    nm = nmap.PortScanner()

    table = Table("Port", "State", "Service")
    port_range = range(start, end + 1)
    s = time.process_time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(scanner, port_range)


    if table.row_count == 0:
        print(f"[bold red][!] No open ports on {target}.[/bold red]")

    else:
        e = time.time()
        print(table)
        print(f"\n[+] Time elapsed: {(e - s)}\n")



if __name__ == '__main__':
    pass