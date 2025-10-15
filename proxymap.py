import requests
import sys
import argparse
import re

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
    print("[+] Attempting connection to proxy")
 

    def createproxy(proxy_url):
        proxy = {"http":args.proxy}
        try: 
            requests.get("http://google.com", proxies=proxy, timeout=30)
        except:
            raise SystemExit("[-] Unable to reach the proxy, try: http://<proxy ip>:<port>")
        else:
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
            raise SystemExit("[-] Unable to reach the proxy, try: http://<proxy ip>:<port>")

    def scan(proxy_url, target_url, ports):
        resultslist = []
        for p in ports:
            try:
                response = requests.get(f'{target_url}:{int(p)}', proxies=proxy_url, timeout=...)
                if response.status_code == 404:
                    continue
                else:
                    print(f"[+] Hit! | http://{target_url}:{int(p)}")
                    resultslist.append(f"[+] http://{target_url}:{int(p)}")
            except:
                print("An error occured during the scan.")
        return resultslist
    
    proxy = createproxy(args.proxy)
    portlist = formatports(args.ports.strip())
    results = scan(proxy, args.url, portlist)
    if results:
        print(f"Scan complete! [{len(results)}] ports online, thank you for using ProxyMap")
        for result in results:
            print(result)
    else:
        print("Scan complete! No active ports discovered")

main()