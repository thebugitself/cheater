# Enumeration

## dirb - basic directory search
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
dirb <PROTOCOL>://<IP>/ `fzf-wordlists`
dirb <PROTOCOL>://<IP>/
```

## dirsearch - basic directory search
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
dirsearch -u <Protocol>://<IP> -w `fzf-wordlists`
```

## subfinder - subdomain finder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
subfinder -d <Domain> -all > sub_subfinder.txt
```

## amass - subdomain finder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
amass enum -passive -d <Domain> -o sub_amass.txt
```

## assetfinder - subdomain finder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
assetfinder --subs-only <Domain> > sub_assetfinder.txt
```

## katana - url crawling
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
katana -u <Domain> -o crawl.txt
```

## arjun - parameter finder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
arjun -u <Domain> -m <Method>
```

## waybackurls - web archives url finder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
echo "<Domain>" | waybackurls > wayback_output.txt
```

## gau - web archives url finder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
gau --o gau_output.txt <Domain>
```

## nuclei - vuln scanning
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
nuclei -target <Domain>
```

## paramspider - file domain list
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
paramspider -l <File>
```

## paramspider - with domain
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
paramspider -d <Domain> -s
```

## paramspider - with domain and placeholder
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
paramspider -d <Domain> -p '<Placeholder>'
```

## httpx - got alive url
#plateform/linux #target/remote #port/80-443 #protocol/http #cat/ATTACK/WEB
```bash
cat <File> | httpx > alive_url.txt
```