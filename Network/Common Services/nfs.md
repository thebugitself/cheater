# nfs

% nfs, showmount, 2049
#plateform/linux  #target/remote  #protocol/nfs #port/2049

## nfs - showmount
#cat/RECON 
```
showmount -e <IP>
```

## nfs - nmap showmount
#cat/RECON 
```
nmap -sV --script=nfs-showmount <IP>
```

## nfs - mount
#cat/ATTACK/CONNECT 
```
mount -t nfs <IP>:<shared_folder> <mount_point> -o nolock
```

## nfs - mount with v2 (no authenrt=)
#cat/ATTACK/CONNECT 
```
mount -t nfs -o vers=2 <IP>:<shared_folder> <mount_point> -o nolock
```