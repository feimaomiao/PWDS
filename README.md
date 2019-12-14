# PWDS #
- - - -
## What is PWDS ##
* PWDS is a local, command line encrypted password storage system with different actions and prefernces avaliable 
* The entire program started with a little summer project and I never thought it would develop into a large-scale project :smiling_imp:
* The whole program is built on python3
- - - -
##How does it work##
* PWDS creates a database and allows you to change different attributes of it.
* Regular backup will be done.
* Cleverly uses clear screen function so that your passwords will not be kept on the terminal screen
* Even if you mess up, there will be a backup to save your day! Import backups are now avaliable!
- - - -
##Possible problems you may encounter##
###WrongPasswordError###
* As its name suggests, you probably entered the wrong password. 
* As for extra security, we do not allow 'try agains' ~~we are just being mean~~
* The occurance of wrong password entering will not affect your database! However, we will record every single attempt to login if 'Log login' preference is set to true

###EncryptionError###
* As of today (12/14/2019), we only have 128 characters avaliable for password.
* Any character used outside of these 128 characters will not be encrypted and will raise encryption error

- - - -
##Exports##
* Sounds strange but we do let you export your saved password and logs in both encrypted and non-encrypted form.
* Avaliable output format includes:
Plain text file(.txt) | Comma Seperated Values file (.csv) | JavaScript Object Notation (.json) | SQL Database File (.db)
---------------------- ------------------------------------ ------------------------------------ ------------------------
- - - -
