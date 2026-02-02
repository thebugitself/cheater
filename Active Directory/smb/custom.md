# custom

% smb, active directory, enumeration, exploitation

## nxc_custom_param - custom smb parameter
#plateform/linux #target/remote #port/445 #protocol/smb #cat/CUSTOM

```bash
nxc smb <IP> -u <Username> <Creds_Options> <Password> --smb-timeout=10 <Custom_Parameter>
```