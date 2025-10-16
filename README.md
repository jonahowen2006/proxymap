### Proxymap
Originally built for the "Squid" proving grounds lab, Proxymap is a lightweight port scanner that abuses open HTTP proxies to check internal ports via the application layer, without relying on raw socket access like tools such as nmap do.

![Alt Text](images/example.gif)

```
options:
  -h, --help     show this help message and exit
  --proxy PROXY  Specify the target proxy.
  --url URL      Specify the target host to scan.
  --ports PORTS  Specify the ports you want to scan.
```

This tool was built for ethical hacking purposes only.
