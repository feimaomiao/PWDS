# PWDS #
- - - -
## What is PWDS ##
* PWDS is a local, light weight command line encrypted password storage system with different actions and preferences avaliable 
* The entire program started with a little summer project and I never thought it would develop into a large-scale project :smiling_imp:
* The whole program is built on python3
- - - -
## How does it work ##
* PWDS creates a database and allows you to change different attributes of it.
* Regular backup will be done.
* Cleverly uses clear screen function so that your passwords will not be kept on the terminal screen
* Even if you mess up, there will be a backup to save your day! Import backups are now avaliable!  
- - - -  
## Possible problems you may encounter ##  
### WrongPasswordError ###  
* As its name suggests, you probably entered the wrong password. 
* As for extra security, we do not allow 'try agains' ~~we are just being mean~~  
* The occurance of wrong password entering will not affect your database! However, we will record every single attempt to login if 'Log login' preference is set to true


- - - -
## Exports ##
* Sounds strange but we do let you export your saved password and logs in both encrypted and non-encrypted form.  
Avaliable output format includes:  

.txt|.csv|.json| .db  
---- | ----| ---- | ----
Plain text file | Comma Seperated Values file | JavaScript Object Notation | SQL Database File  
- - - -
##  How can I install? ##
For unix machines you can use   
`chmod +x PWDS`  
`./PWDS`  
If you want to build from source you can also do the following:  
clone this website  
cd into the git directory  
run python command `python3 zipfile -m src -p "/usr/bin/env/python3"`  
You can also do this:
cd into git directory
`python3 src`
- - - -
## Functions ##
`new`: inputs password into database. The password will have a key(used to find the exact password) and the password itself  
`get`: gets password from database, outputs it on screen and copies it to pasteboard. Avaliable options: * --> outouts all saved password keys  
`help`: prints all current action keywords onto screen
`change password`: Changes user password  
`quit`: saves file and quits program. Another way to quit is to press `Ctrl+C` to end the current progress  
`delete`: deletes entry in database. You can choose to delete by index or name  
`change command`: Changes user command keywords  
`exportpws`: exports password to desinated directory. Options: Encrypt(Can only be set in preferences)  
`exportlog`: export user logs  
`backup now`: creates a copy of the current database and makes a backup.  
`import file`: Imports the most current backup file.  
`user preferences`: Gives options to alter the user preferences.  
 - - - -
## Preferences ##
`verbose`: prints every procedure. Not good for security as all passwords will not be deleted after outputting  
`copyAfterGet`: copies password to clipboard after `get` function  
`askToQuit`: Prompts you before `quit` function  
`customColor`: colors will all be mono if this preference is set to `False`. Different color can be printed if this preference is set to True!   
`logLogin`: Logs every login into log file. can be used to trace wrong password attempts!  
`encExpDb`: encrypts Export database. Decrypts password before export if this preference is set to `False`  
`useDefLoc`: Use default export location. Will prompt for a location everytime if set to `False`  
`exportType`: Allows different output formats.  
`defExpLoc`: default export location. Default = `~/Documents`
`createBcF`: create a backup file.
`backupFileTime`: A regular backup time  
`backupLoction`: where backup files are stored. Default: `~/Library/.pbu`  
`hashBackupFile`: hashes a backup folder  
`hashUserFile`: User filenames are hashed  
`createRandF`: Creates random files and puts it in the same folder. Can't easily distinguish which one is your file!!
- - - -
## Ran into a problem? ##
Please put in an issue! I will try my best to fix it!  
- - - -
###### A command line password starage system, PWDS
###### ©2020 Matthew Lam
###### Licensed under the MIT License




 