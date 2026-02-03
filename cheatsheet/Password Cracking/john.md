# john

% john, office, password cracking, hash cracking

## john - office cracking
#plateform/linux #target/local #cat/PASSWORD-CRACKING

```bash
office2john.py <file> > <file>.hashes
john --wordlist=`fzf-wordlists` <file>.hashes
```