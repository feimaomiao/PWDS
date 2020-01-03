# usr/bin/python3
import sqlite3, os, random, time, sys, hashlib, shutil, readchar, pyperclip
from funcs import *
from userClass import userInterface
from datetime import datetime, timedelta

global colors

# Assign colors to colors --> Default is true
colors = buildColors(True)

def checkdir(): 

	# Clear screen
	os.system('clear')

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
	user.actions['change command'] 	: lambda: user.changePassword(),
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
		else:
			print(colors.darkgrey('No action inputted')) if user.verbose else None
			user.log('No action returned')
			user.help()
			waitForInput(colors)
			emptyline() if not user.verbose else None
			


def linktodb():

	# Asks for name
	userName = input('Please enter your username:\n').lower()
	emptyline()

	# possible outputs if hashfile is checked
	regFile = os.path.join(os.path.expanduser('~/.password'), '%s.db' % ('.' + userName))

	hashedName = hashlib.pbkdf2_hmac('sha224', userName.encode('utf-32'), b'08944de8a152170e823f865c7a41d75c', 500000).hex()
	hashedFile = os.path.join(os.path.expanduser('~/.password'), '.%s.db' % hashedName)

	# cheks if the user is a new user-->if file exists in folder
	newUser = not(os.path.isfile(regFile) or os.path.isfile(hashedFile))

	# gets actual user filepath -->Could be hashed or just hidden
	actualUserName = hashedName if os.path.isfile(hashedFile) else userName

	# Asks for password. Password will not be shown
	passwd = input('Please enter your password:\n') 

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
		# user.delete()
		# user.new()
		# user.new()
		# user.get()
		# user.changePassword()
		# user.backup()
		# user.changeCommand()
		# user.checkBackup()
		# user.exportPassword()
		# user.exportLog()
		# user.importFile()
		# user.changePreferences() d
		# [print('{0:40}{1:40}\n'.format(str(x), str(value))) for x, value in user.actions.items()]
		print(user.actions)
		user.backup()
		# while True:
		uifunc(user)
 
		user.quit()
	except WrongPassWordError:
		raise 
	except normalQuit:
		# user calls function 'quit'
		user.log('User quits (\'Command =Quit\')')
		user.checkBackup() if user.preferences.get('createBackupFile') else None
		raise 
		# user enters key binding ctrl+c
	except KeyboardInterrupt:
		print('\n\n\n\n\n\n\n\n')
		user.log('User quits (\'KeyboardInterrupt\')')
		raise normalQuit
		user.checkBackup() if user.preferences.get('createBackupFile') else None
	except instantQuit:
		raise normalQuit
	else:
		raise normalQuit
	finally:
		emptyline() if not user.verbose else None

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
		quit()

main()