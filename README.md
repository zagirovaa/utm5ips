# utm5ips
Search for free ip addresses in NetUp UTM5 billing system

```

usage: utm5ips.py [-h] [-m {gui,con}] [-a]

The script searches for free ip addresses in NetUp UTM5 billing system.

optional arguments:
  -h, --help    show this help message and exit
  -m {gui,con}  choose application mode
  -a            list all available ip addresses

```
### Installation
- Download application from GitHub  
  ``` git clone git@github.com:ZagirovAA/utm5ips.git  ```

- Go to the downloaded folder  
  ``` cd utm5ips ```

- Install all required dependencies  
  ``` python3 install -r requirements.txt ```

- Make changes to config file **config.ini**
  - add credentials to **database** section
  - add subnet(s) to **subnets** section
  - add excluded addresses to **exceptions** section

- Start the application  
  - in console mode  
    ``` python3 utm5ips.pyw -m con ```
  - in graphical mode (default mode)  
    ``` python3 utm5ips.pyw ```
  
  - showing all free ips from each subnet (available for both modes above)  
    ``` python3 utm5ips.pyw -m con -a ```  
    ``` python3 utm5ips.pyw -a ```
