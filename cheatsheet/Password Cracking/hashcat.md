# hashcat

% hashcat, password cracking, cracking, passwords, hashes

## hashcat - basic cracking (auto detect hash type)
#plateform/linux #target/local #cat/PASSWORD-CRACKING

```bash
hashcat <hash-file> `fzf-wordlists`
```

## hashcat - custom hash type cracking
#plateform/linux #target/local #cat/PASSWORD-CRACKING

```bash
hashcat `<hash-file> -m <hash-type> `fzf-wordlists`
```

## hashcat - identify hash type
#plateform/linux #target/local #cat/PASSWORD-CRACKING

```bash
hashcat --identify <hash-file>
```