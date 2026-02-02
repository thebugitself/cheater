# nmap

% nmap, network, enumeration, ports, services

## nmap - scan port only
#plateform/linux #target/remote #cat/RECON

```bash
nmap -p- --min-rate=4000 <IP> -oN nmap.txt -vv
```

## nmap - scan port with script
#plateform/linux #target/remote #cat/RECON

```bash
nmap -p- -sVC --min-rate=4000 <IP> -oN nmap.txt -vv
```