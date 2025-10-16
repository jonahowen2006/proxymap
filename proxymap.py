import requests
import sys
import argparse
import re
import threading
import time
import itertools

def main():
    parser = argparse.ArgumentParser(description="ProxyMap is a light-weight network scanner designed to work through basic HTTP proxies that lack Layer 3 support," \
    " where traditional tools like Nmap fail due to their reliance on raw socket access.",
    usage="""proxymap.py [-h] --proxy <proxy-url>:<port (default 80)> --url <target-url> --ports <ports/port-range>
example: python proxymap.py --proxy http://192.168.54.49:3128 --url http://example.com --ports 80,8080,800
    """)

    parser.add_argument("--proxy", 
                        help="Specify the target proxy.", required=True)
    
    parser.add_argument("--url", 
                        help="Specify the target host to scan.", required=True)
    
    parser.add_argument("--ports", 
                        help="Specify the ports you want to scan.", required=True, type=str)

    args = parser.parse_args()
    print("== ProxyMap v1.2 - 2025 - Jonah Owen ==")

    def animation(message, done):
            for c in itertools.cycle([
                '\033[0;34m\033[1m[=   ]\033[0m', 
                '\033[0;34m\033[1m[-=  ]\033[0m', 
                '\033[0;34m\033[1m[ -= ]\033[0m', 
                '\033[0;34m\033[1m[  -=]\033[0m',
                '\033[0;34m\033[1m[   =]\033[0m',
                '\033[0;34m\033[1m[  =-]\033[0m',
                '\033[0;34m\033[1m[ =- ]\033[0m',
                '\033[0;34m\033[1m[=-  ]\033[0m' 
                ]):
                    if done.is_set():
                        break
                    sys.stdout.write(f"\r{message} " + c)
                    sys.stdout.flush()
                    time.sleep(0.1)
            sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")

    def createproxy(proxy_url):
        done = threading.Event()
        t = threading.Thread(target=animation, args=("[+] Attempting connection to proxy", done))
        t.start()

        proxy = {"http":args.proxy}
        try: 
            requests.head("http://google.com", proxies=proxy, timeout=10)
        except:
            done.set()
            t.join()
            print("\n[+] Attempting connection to proxy")
            raise SystemExit("[-] Unable to reach the proxy, try: http://<proxy ip>:<port>")
        else:
            done.set()
            t.join()
            print("\n[+] Attempting connection to proxy")
            print("[+] Connection success\n")
            return {"http":args.proxy}

    def formatports(ports):
        if re.match(r"^(?:(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)-(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))$", ports):
            portsplit = ports.split("-")
            return list(range(int(portsplit[0]), int(portsplit[1])+1))
        if re.match(r"^(?:(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)(?:,(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))*)$", ports):
            return ports.split(',')
        if re.match(r"^(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]?\d{1,4}|0)$", ports):
            return ports
        else:
            raise SystemExit("[-] Invalid port format, try p-p | p,p,p,p | p")

    def scan(proxy_url, target_url, ports, max_workers=700):
        done = threading.Event()
        t = threading.Thread(target=animation, args=("[+] Running scan ", done))
        t.start()
        resultslist = []

        import concurrent.futures

        def _probe(p):
            try:
                resp = requests.head(f'{target_url}:{int(p)}', proxies=proxy_url, timeout=5)
                if resp.status_code == 200:
                    return f"http://{target_url}:{int(p)} | Status Code [{resp.status_code}]"
            except requests.RequestException:
                return None
            return None

        ports = list(ports) 
        workers = max_workers

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as exe:
            for res in exe.map(_probe, ports):
                if res:
                    sys.stdout.write("\r" + " " * (30) + "\r")
                    print(f"\033[32m[+]\033[0m Hit! | {res}")
                    resultslist.append(res)
        done.set()
        t.join()
        return resultslist

    portlist = formatports(args.ports.strip())
    proxy = createproxy(args.proxy)
    results = scan(proxy, args.url, portlist)
    if results:
        print(f"\nScan complete! [{len(results)}] port(s) online, thank you for using ProxyMap")
        for result in results:
            print(result)
    else:
        print("Scan complete! No active ports discovered")
        

main()
