# capcheck
Audit Azure endpoints for MFA conditional access policy bypasses with a valid username and password. Use the built in options and brute force everything (loud), or specify a specific combination of user agent, client ID, and endpoint you suspect will bypass MFA. This tool will print the scope of any tokens obtained at the end of the run. Only for non-federated logins atm.

```
options:
  -h, --help            Show this help message and exit.
  -u, --username USERNAME
                        The username for authentication.
  -U, --userlist USERNAME_LIST
                        A file containing a list of usernames. Useful when common passwords are used more than once across users in the tenant.
  -p, --password PASSWORD
                        The password for authentication.
  -a, --useragent USERAGENT
                        Define a user agent to try. Default is iPhone.
  -c, --clientid CLIENTID
                        Define a client id to try. Default is aadps.
  -e, --endpoint ENDPOINT
                        The endpoint to spray. Deafult is MS Graph.
  -ab, --useragent-brute
                        Perform user agent brute forcing with built in list.
  -cb, --clientid-brute
                        Perform client id brute forcing with built in list.
  -eb, --endpoint-brute
                        Perform endpoint brute forcing with built in list.
  --brute-all           Perform user agent, endpoint, and client ID brute forcing with built in lists. *WARNING* - lots of requests..
  --list-useragents     List the built in user agents.
  --list-endpoints      List the built in endpoints.
  --list-clientids      List the built in client ids.
  --list-all            List all the built in user agents, endpoints, and client ids.
  --proxy PROXY         Proxy to use, ex: http://127.0.0.1:8080

examples:
# List built in parameters.
python3 capcheck.py --list-all

# Sign into intune using the MS intune company portal client id and windows desktop user agent. Use the built in numbers or specify the value directly.
python3 capcheck.py -u user@client.com -p password -c 59 -e 21 -a 5
python3 capcheck.py -u user@client.com -p password -c '9ba1a5c7-f17a-4de9-a1f1-6178c8d51223' -e 'https://msmamservice.api.application' -a 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'

# Brute force various built in parameters.
python3 capcheck.py -u user@client.com -p password --useragent-brute
python3 capcheck.py -u user@client.com -p password --clientid-brute
python3 capcheck.py -u user@client.com -p password --endpoint-brute

# Brute force everything, proxy the requests.
python3 capcheck.py -u user@client.com -p password --brute-all --proxy http://127.0.0.1:8080
```

## Examples
Check MFA enforcement across Azure endpoints with the built in values:  
![image](https://github.com/user-attachments/assets/e0a0517d-2d8c-4587-b9cb-fd4788c80434)  

Specify a custom client ID, user agent, and endpoint:  
![image](https://github.com/user-attachments/assets/006d5e37-374a-46c4-9df2-39be16637e9b)  

## Credits
carlospolop - https://github.com/carlospolop/AzureAppsSweep  
dafthack - https://github.com/dafthack/MFASweep

## TODO
- Take files in as input  
- Support federated logins
- Jitter / delay 
