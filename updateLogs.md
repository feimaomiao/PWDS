# Change Logs #
- - - -
### 2019/12/15 04:25 ###
#### Changed License.md to my actual name ####

#### Added [wait for input] into funcs.py  ####
now it imports a class and prints the color imported  

#### Added new file userClass.py ####
pwd.py imports a class from userClass.py
neater codes  

#### Added pwd.py previous class structure into userClass.py ####
pwd.py now only includes prompt and calling class
neater codes, easier references  
- - - -
### 2019/12/16 01:48 ###
#### New procedure in login function ####
instantQuit skips userInterface.checkbackup() function and enhances performance  
#### Altered pwd.py login process ####
if newuser: {initialise...login}else: {login}-->if newuser: {initialise} {login}  
#### Added error handling 'instantQuit' in pwd.py  ####
New error handling prevents possible flaw while importing backups.  
- - - -
### 2019/12/16 08:49 ###
#### introduce delete function ####
Deletes item from database `still in development`
- - - -  
### 2019/12/16 11:50 ###
#### Changed encryption method #### 
Password is now hashed and hexified before encrypting to prevent injection attacks  
improved 'Delete' function `still in development`
- - - -
### 2019/12/16 15:24 ###
#### Finished function delete ####
Finally. Introducing function 'delete' from database
slight alteration in var types
- - - -
### 2019/12/16 16:33 ###
#### Edited encryption ####
Changed password hashing from 'sha256' to 'sha512'
- - - -
### 2019/12/16 22:11 ###
#### A reform in database storage ####
All 'key' values inside the database is now slightly encrypted //symmetrical  
logs are includeed  
#### Encryption of keys
password hashing now uses `sha512(password) + sha512(''.join(sorted(password, reversed=True)))`  
longer password allows higher security  
- - - -
### 2019/12/17 16:30 ###
#### New encryption method ####
Today was a busy day (even though I have my finals right now)  
Found a major flaw in 'enc.py' causing encryption problems, completely redesigned the encrypting alogrithm
_Now supports any character!!_  
#### More hashing ####
Anything that includes the process of using your password now uses hashed password (of course)  
No functionality addition  
- - - -
### 2019/12/20 12:07 ###
It's been a few days since I last commited cus I have my finals  
just finished my finals so the update should be faster and its holiday I mean...  
#### Modified user preference function ####
Still working on it. String formatting is kind of killing me but I should be able to figure it out soon
Output looks fine
The past few days I changed the 'colors' returning method, making it a bit faster I believe  
#### Fixed encryption method! ####
I also fixed the 'last character problem' in enc.py, eliminating possible errors.
### 2019/12/24 00:10 ###
- - - -
Whoa it's been a few days since my last push.  
Spent my weekend going around killing time...did't work a whole lot on it lol  
Added many many more functionality to option `verbose` 
New file alterPrefs. Used to change preferences `still in development`  
- - - -
### 2019/12/28 18:03 ###
Merry christmas everyone!  
Sorry for late update cus the last few days were really busy and only minor changes could be done  
alterPrefs is close to finishing. Then I have to figure out how to implement some of the preferences `still in development`  
Renamed `bin` to `exec`
- - - -
### 2019/12/29 03:57 ###
Finished functionality of change preference function
Alterprefs is finished!!!!`done`  
still need more comments to make code easier to read `still in deveopment`  
New file `random.json` to import random to `funcs.py`  
Changed `backup` function for the `userPrefs` function
- - - -
### 2019/12/29/13:17 ###
Done sleeping. 
Added requirements.txt
modified gitignore