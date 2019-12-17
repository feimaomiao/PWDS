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
