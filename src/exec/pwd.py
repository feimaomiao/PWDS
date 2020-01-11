# usr/bin/python3
import sqlite3, os, random, time, sys, hashlib, shutil, readchar, pyperclip
from .funcs import *
from .userClass import userInterface
from datetime import datetime, timedelta
from getpass import getpass

global colors

# Assign colors to colors --> Default is true
colors = buildColors(True)

def checkdir(): 

	# Clear screen
	os.system('CLS') if os.name == 'nt' else os.system('clear')

	text = 'Connecting to folder' 

	# Checks if ~/.password is a dir
	if not os.path.isdir(os.path.expanduser('~/.password')) or not os.path.isdir(os.path.expanduser('~/Library/.pbu')):
		text = 'Creating folder' 

		# Creates .password folder in checkdir folder is hidden
		os.mkdir(os.path.expanduser('~/.password')) if not os.path.isdir(os.path.expanduser('~/.password')) else None
		os.mkdir(os.path.expanduser('~/Library/.pbu'))

	print(colors.blue('Initialising user workspace:') ,colors.lightgrey(text))
	time.sleep(random.random())
	emptyline()

def uifunc(user):
	colors = buildColors(user.preferences.get('customColor'))
	print(colors.darkgrey('building colors in user interface finished')) if user.verbose else None
	funcs= {
	user.actions['help']			: lambda: user.help(),
	user.actions['get']				: lambda: user.get(),
	user.actions['new']				: lambda: user.new(),
	user.actions['change password']	: lambda: user.changePassword(),
	user.actions['quit']			: lambda: user.quit(),
	user.actions['delete']			: lambda: user.delete(),
	user.actions['change command'] 	: lambda: user.changeCommand(),
	user.actions['exportpwd']		: lambda: user.exportPassword(),
	user.actions['exportlog']		: lambda: user.exportLog(),
	user.actions['backup now']		: lambda: user.backup(),
	user.actions['import file']		: lambda: user.importFile(),
	user.actions['user preferences']: lambda: user.changePreferences(),
	}
	print(colors.darkgrey('Building actions finished')) if user.verbose else None
	user.log('User interface')
	emptyline() if not user.verbose else None
	while True:
		act = input(colors.yellow('Please enter the action you would like to proceed'))
		if act in funcs.keys():
			print(colors.darkgrey('Called function successfully')) if user.verbose else None
			funcs.get(act)()
			emptyline() if not user.verbose else None
		else:
			print(colors.darkgrey('No action inputted')) if user.verbose else None
			user.log('No action returned')
			user.help()
			emptyline() if not user.verbose else None
	return None

def linktodb():

	# Asks for name
	userName = input('Please enter your username:\n').lower()

	# possible outputs if hashfile is checked
	regFile = os.path.join(os.path.expanduser('~/.password'), '%s.db' % ('.' + userName))

	hashedName = hashlib.pbkdf2_hmac('sha224', userName.encode('utf-32'), b'08944de8a152170e823f865c7a41d75c', 500000).hex()
	hashedFile = os.path.join(os.path.expanduser('~/.password'), '.%s.db' % hashedName)

	# cheks if the user is a new user-->if file exists in folder
	newUser = not(os.path.isfile(regFile) or os.path.isfile(hashedFile))

	# gets actual user filepath -->Could be hashed or just hidden
	actualUserName = hashedName if os.path.isfile(hashedFile) else userName

	# Asks for password. Password will not be shown
	passwd = getpass(prompt='Please enter your password\n')

	passwd = str(hashlib.pbkdf2_hmac('sha512', str(passwd).encode('utf-32'),
	 ''.join(sorted(passwd)).encode('utf-32'),
	  300000).hex()) + str(hashlib.pbkdf2_hmac('sha512',
	   str(passwd).encode('utf-32'), ''.join(sorted(passwd, reverse=True)).encode('utf-32'), 300000).hex())

	emptyline()

	# shows hides user file
	user = userInterface(actualUserName, passwd)


	# Default empty, cannot be changed as user preferences have not been built yet.

	try:

		# Returning users will skip initialise part. 
		if newUser:
			user.initialiseNewUser()

		# Returning user will be directed immediately to login page
		user.login()

		# Runs UI function
		uifunc(user)
 
	except WrongPassWordError:
		raise 
	except normalQuit:
		emptyline() if not user.verbose else None
		# user calls function 'quit'
		user.log('User quits (\'Command =Quit\')')
		user.checkBackup() if user.preferences.get('createBackupFile') else None
		raise 
		# user enters key binding ctrl+c
	except KeyboardInterrupt:
		emptyline() if not user.verbose else None
		user.log('User quits (\'KeyboardInterrupt\')')
		user.checkBackup() if user.preferences.get('createBackupFile') else None
		raise normalQuit
	else:
		emptyline() if not user.verbose else None
		# Ran into error, should not happen
		print(colors.red('You ran into an error. Please re-run the previous action with option"verbose" set to true and report an issue!\nThanks!'))
		time.sleep(10)
		raise normalQuit
	finally:
		# saves file
		user.file.commit()

		# closes cursor and file
		user.cursor.close()
		user.file.close()


def main():
	# Checks if directory exists and initialises the screen
	checkdir()
	try:
		# links to database, logs in 
		linktodb()
	except WrongPassWordError:
		print(colors.red('WrongPassWordError:'),colors.green('This is not the right password! Please try again!'))
	except normalQuit:
		print(colors.green('Thank you for using!'), colors.lightblue('\nSee you next time!'))
		print(colors.lightcyan('''
			═✿✿✿═════✿✿═════✿✿═════✿✿✿═
			════════════ ('\\../') ═════════════
			════════════ (◕.◕) ═════════════
			════════════ (,,)(,,) ═════════════
			.▀█▀.█▄█.█▀█.█▄.█.█▄▀　█▄█.█▀█.█─█
			─.█.─█▀█.█▀█.█.▀█.█▀▄　─█.─█▄█.█▄█

			'''))
	finally:
		quit()