'''
Author: Paulo Neto 
File: PortSanner.py

Description:
Scanner of ports 
'''
import argparse 
import socket 
import pyfiglet
import os 
from colorama import init , Fore, Back, Style
from threading import Thread, Lock
from queue import Queue

def cls() -> None:
    os.system('cls')

# some colors 
init()
GREEN = Fore.GREEN 
RESET = Fore.RESET 
GRAY  = Fore.LIGHTBLACK_EX
CYAN  = Fore.CYAN

# number of threads, fell free to tunee this parameter as you wish
N_THREADS = 200 
# thread queue 
q = Queue()
print_lock = Lock()

open_ports = [] 

def cls():
    os.system('cls')

def port_scan(port):
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"{GRAY}{host:15}:{port:5} is closed {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open {RESET}")
            open_ports.append(port)
    finally:
        s.close()

def scan_thread():
    global q
    while True:
        # get the port number from the queue
        worker = q.get()
        port_scan(worker)
        # tells the queue that the scanning for that port
        # is done 
        q.task_done()

def main(host, ports):
    global q 
    for t in range(N_THREADS):
        # for each thread, start it 
        t = Thread(target=scan_thread)
        # when we set daemon to truem that thread will end when the main thread ends
        t.daemon = True
        # start the daemon thread 
        t.start()
    for worker in ports: 
        # for each port, put that por into the queue 
        # to start scanning 
        q.put(worker)
    # wait the threeads (port scanners) to finish 
    q.join()

if __name__== '__main__':
    # parse some parameters passed 
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default=1-65535, help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [p for p in range(start_port, end_port)]

    cls()

    ascii_banner = pyfiglet.figlet_format('Port Scanner')
    print(f'{CYAN}{ascii_banner}{RESET}')
    print(f'\n{CYAN}Scanning {host} ...{RESET}\n')

    main(host, ports)
    print(f'\n{CYAN}Open ports are :  {open_ports} {RESET}')
    print('=======================================')
   
    
 
