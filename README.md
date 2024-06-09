# Starter PHP Docker

## Start on windows:
`docker compose  -f docker-compose.yml up`

## Start on apple chip
`docker compose  -f docker-compose.yml -f docker-compose-m1.yml up`

## Generate SSL certificates
```
cd docker/ssl

mkcert -install
mkcert -install
mkcert localhost 127.0.0.1 ::1
```


###  Install mkcert
#### OSX
```
brew install mkcert
brew install nss # if you use Firefox
```

#### Linux
```
sudo apt install libnss3-tools
# -or-
sudo yum install nss-tools
# -or-
sudo pacman -S nss
# -or-
sudo zypper install mozilla-nss-tools
```

#### Windows
```
scoop bucket add extras
scoop install mkcert
```

----------
### References
- https://github.com/mlocati/docker-php-extension-installer
- https://iammohaiminul.medium.com/run-php-application-using-docker-with-apache-and-ssl-certificates-327a8ee2056b
- https://github.com/FiloSottile/mkcert#installation
