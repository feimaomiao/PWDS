# usr/bin/python3
import sqlite3, os, random, time, sys, hashlib, shutil, readchar, pyperclip
from funcs import *
from userClass import userInterface
from datetime import datetime, timedelta

global colors

# Assign colors to colors --> Default is true
colors = buildColors(True)

# Functions in userInterface


	# def UI(self):
	# 	userAction = input(colors.lightblue('Please enter what do you want to do:\n'))
	# 	emptyline() if not self.verbose else None
	# 	if userAction not in self.actions.keys():
	# 		print(colors.red(userAction), colors.yellow('is not in your list of commands!\nPlease refer to the chart below for your actions!'))
	# 		self.help()
	# 		emptyline() if not self.verbose else None
	# 		self.UI()
	# 	else:
	# 		action = self.actions.get(userAction)
	# 		print(action)

def checkdir(): 

	# Clear screen
	os.system('clear')

	text = 'Connecting to folder' 

	# Checks if ~/.password is a dir
	if not os.path.isdir(os.path.expanduser('~/.password')) or not os.path.isdir(os.path.expanduser('~/Library/.pbu')):
		text = 'Creating folder' 

		# Creates .password folder in checkdir folder is hidden
		os.mkdir(os.path.expanduser('~/.password')) if not os.path.isdir(os.expanduser('~/.password')) else None
		os.mkdir(os.path.expanduser('~/Library/.pbu'))

	print(colors.blue('Initialising user workspace:') ,colors.lightgrey(text))
	time.sleep(random.random())
	emptyline()

def linktodb():

	# Asks for name
	userName = input('Please enter your username:\n') 
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
		# user.new()
		# user.get()
		# user.changePassword()
		# user.backup()
		# user.changeCommand()
		# user.checkBackup()
		# user.exportPassword()
		# user.exportLog()
		# user.importFile()
		# user.delete()
		user.changePreferences()
		# [print('{0:40}{1:40}\n'.format(str(x), str(value))) for x, value in user.actions.items()]
		time.sleep(100000)
		# user.quit()
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