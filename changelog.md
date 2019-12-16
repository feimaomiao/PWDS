# Change Logs #
- - - -
#### 2019/12/15 04:25 ####
1 Changed License.md to my actual name    

2 Added [wait for input] into funcs.py  
now it imports a class and prints the color imported  

3 Added new file userClass.py
pwd.py imports a class from userClass.py
neater codes  

4 Added pwd.py previous class structure into userClass.py
pwd.py now only includes prompt and calling class
neater codes, easier references  
- - - -
#### 2019/12/16 01:48 ####
1 New procedure in login function
instantQuit skips userInterface.checkbackup() function and enhances performance
2 Altered pwd.py login process
if newuser: {initialise...login}else: {login}-->if newuser: {initialise} {login} 
3 Added error handling 'instantQuit' in pwd.py  
4 New error handling prevents possible flaw while importing backups.  