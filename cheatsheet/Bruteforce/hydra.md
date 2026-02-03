# hydra

% hydra, bruteforce, ssh, ftp, http

## hydra - single username service bruteforce (ssh, ftp, etc)
#plateform/linux #target/remote #cat/ATTACK/BRUTEFORCE

```bash
hydra -l <Username> -P `fzf-wordlists` <protocol>://<IP> -s <Port>
```