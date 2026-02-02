# ffuf

% web fuzzing, directory brute forcing, subdomain brute forcing, parameter fuzzing, vhost fuzzing

## ffuf - directory brute forcing
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB

```bash
ffuf -w `fzf-wordlists` -u http://<IP>/FUZZ
```

## ffuf - vhost brute forcing
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
DOMAIN=<Domain>
ffuf -w `fzf-wordlists` -H "Host: FUZZ.$DOMAIN" -u "http://$DOMAIN/"
```