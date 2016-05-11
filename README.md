#CTFBot2
 
####IRC Bot listing upcoming online CTF from ctftime.org API

This is another version of a small IRC bot listing upcoming CTF from ctftime.org and some resources related to them.

##Dependencies:

coming soon..

##Features:

* List upcoming online CTFs from ctftime.org using their API
* Join multiple servers/channels
* Small list of resources related to computer security
* Easy to add remove features through modules

##List of commands:

#Default bot trigger character is @

#Listing available modules:

@modules                                                          
+-----+----------+-----------+-----------------------------------+
|     | MODULE   | TRIGGER   | DESCRIPTION                       |
+-----+----------+-----------+-----------------------------------+
| [+] | ctftime  | @ctftime  | CTFTime calendar                  |
| [+] | dump     | @dump     | List of CTF dump (binaries etc..) |
| [+] | learning | @learning | List of learning materials        |
| [+] | utc      | @utc	     | Display current UTC time          |
| [+] | vulniso  | @vulniso  | List of vulnerable ISO            |
| [+] | wargames | @wargames | List of online wargames           |
| [+] | writeups | @writeups | List of CTF writeups              |
+-----+----------+-----------+-----------------------------------+

#List upcoming ctftime.org CTF:

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

#Display CTF description using its ID:

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


##Reference:
...
