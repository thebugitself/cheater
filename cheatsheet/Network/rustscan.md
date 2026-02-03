# rustscan

% rustscan, port scanning, network, services

## rustscan - scan port only
#plateform/linux #target/remote #cat/RECON
```bash
rustscan -a <IP> --ulimit 5000 --range 1-65535 -- -oN rustscan.txt
```

## rustscan - scan port with scripts
#plateform/linux #target/remote #cat/RECON
```bash
rustscan -a <IP> --ulimit 5000 --range 1-65535 -- -sVC -oN rustscan_script.txt
```