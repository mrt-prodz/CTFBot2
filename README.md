# CTFBot2
 
#### IRC Bot listing upcoming online CTF from ctftime.org API

This is another version of a small IRC bot listing upcoming CTF from ctftime.org and some resources related to them.

## Dependencies:

[PrettyTable](https://pypi.python.org/pypi/PrettyTable): A simple Python library for easily displaying tabular data in a visually appealing ASCII table format.

[pytz](https://pypi.python.org/pypi/pytz): World timezone definitions, modern and historical

[requests](https://pypi.python.org/pypi/requests/2.9.1): Python HTTP for Humans

[duckduckgo](https://pypi.python.org/pypi/duckduckgo/0.1) Library for querying the Duck Duck Go API

## Features:

* List upcoming online CTFs from ctftime.org using their API
* Join multiple servers/channels
* Small list of resources related to computer security
* Easy to add remove features through modules

## List of commands:

### Default bot trigger character is @

### Available commands:
```
@help                                                             
+-------+------------------------+-------------------------------+
| USER  | TRIGGER                | DESCRIPTION                   |
+-------+------------------------+-------------------------------+
| admin | @disable [module name] | disable module                |
| admin | @enable [module name]  | enable module                 |
| admin | @reload                | reload modules and/or add new |
| guest | @help [module name]    | display module help           |
| guest | @modules               | display modules               |
+-------+------------------------+-------------------------------+
```

### Access admin functions/modules (auth through private message):
```
/msg ctfbot @auth admin
[+] access granted
```

You have to configure the admin sha256(password+salt) per channel in ctfbot.py

Password must match hashlib.sha256('password'+'salt'.encode()).hexdigest()

Some modules can be accessed only by an admin such as raw.
```
   user | @raw PRIVMSG #ctfbot :raw message
+ctfbot | raw message
```

Unauthorized users will get the following message:
```
[!] only authorized users can run this command
```


### Getting help of a specific module:
```
@help ctftime
+----------+--------------------------------+
| ARGUMENT | DESCRIPTION                    |
| list     | list upcoming ctf              |
| show #   | show ctf info with id number # |
+----------+--------------------------------+
```

Alternative way to get help:
```
@ctftime help
@ctftime
```

### Listing available modules:
```
@modules                                                          
+-----+----------+-----------+-----------------------------------+
|     | MODULE   | TRIGGER   | DESCRIPTION                       |
+-----+----------+-----------+-----------------------------------+
| [+] | ctftime  | @ctftime  | CTFTime calendar                  |
| [+] | dump     | @dump     | List of CTF dump (binaries etc..) |
| [+] | learning | @learning | List of learning materials        |
| [+] | utc      | @utc      | Display current UTC time          |
| [+] | vulniso  | @vulniso  | List of vulnerable ISO            |
| [+] | wargames | @wargames | List of online wargames           |
| [+] | writeups | @writeups | List of CTF writeups              |
+-----+----------+-----------+-----------------------------------+
```

### List upcoming ctftime.org CTF:
```
@ctftime list
+-----+-----------------------------+-------+--------+ 
|  ID | TITLE                       | START | FINISH | 
+-----+-----------------------------+-------+--------+ 
| 312 | TU CTF 2016                 | 05/13 | 05/15  | 
| 295 | HSCTF 3                     | 05/14 | 05/21  | 
| 323 | PHDays CTF 2016             | 05/17 | 05/18  | 
| 308 | CONFidence CTF 2016         | 05/19 | 05/20  | 
| 320 | DEF CON CTF Qualifier 20... | 05/21 | 05/23  | 
| 314 | BackdoorCTF 2016            | 05/21 | 05/22  | 
| 305 | TJCTF 2016                  | 05/28 | 05/31  | 
| 321 | Belluminar 2016             | 06/01 | 06/02  | 
| 322 | ALICTF 2016                 | 06/04 | 06/06  | 
+-----+-----------------------------+-------+--------+ 
```

### Display CTF description using its ID:
```
@ctftime show 320
+--------+--------------------------------+
|   NAME | DEF CON CTF Qualifier 2016     |
|  START | 2016-05-21 00:00:00            |
| FINISH | 2016-05-23 00:00:00            |
| RATING | 0.0                            |
| FORMAT | Jeopardy                       |
|    URL | https://2016.legitbs.net/      |
|        | https://ctftime.org/event/320/ |
+--------+--------------------------------+
```

## Reference:
...
