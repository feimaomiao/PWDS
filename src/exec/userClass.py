import sqlite3, os, random, time, sys, hashlib, shutil, readchar, pyperclip
from .alterPrefs import preferences as alterPreferences, usrp
from datetime import datetime, timedelta
from .funcs import *
from .enc import encrypt as enc, decrypt as dec, encsp

# user class. All actions are done under a class structure.
class userInterface():

	# __init__ builds the variables in class userInterface
	def __init__(self,filename, password):
		# build and/or connects the user database file
		self.file = sqlite3.connect(os.path.expanduser('~/.password/')+ '.%s.db' %filename)

		# creates cursor object for user database 
		self.cursor = self.file.cursor()

		# user password
		self.__password = password

		# user actions and preferences will be filled in later
		self.actions = {}
		self.preferences = {}

		# Default verbose is False
		self.verbose = False

		# Get username
		self.userName = filename
		
		del(password)

	def __repr__(self):
		return str(self.userName)

	# builds the user actions and preferences
	def buildActionsPreferences(self):

		# builds user preferences
		for prefs in self.cursor.execute('''SELECT * FROM userPreferences''').fetchall():

			#get true/false/defined value
			self.preferences.update({prefs[0]: bool(int(prefs[3])) if prefs[3] in ['0','1', 0, 1] else prefs[3]}) 

		# Assign to verbose
		self.verbose = self.preferences.get('verbose')
		self.actions = {}
		# builds user actions
		self.actions = {v: encsp(k, self.__password) for v, k in dict(self.cursor.execute('SELECT * FROM commands').fetchall()).items()}
		# Set colors after building user preferences
		global colors
		colors = buildColors(self.preferences.get('customColor'))
		print(colors.darkgrey('building colors')) if self.verbose else None
		print(colors.darkgrey('Building preferences...Done\nGetting user commands')) if self.verbose else None
		print(colors.darkgrey('getting preferences was successful')) if self.verbose else None
		self.file.commit()
		print(colors.darkgrey('Saving file and commiting user interface')) if self.verbose else None
		emptyline() if not self.verbose else None
		return None

	def initialiseNewUser(self):
		global colors
		colors = buildColors(True)
		def requestforinput(item, usedlist): 

			# Does not allow duplicatews
			i = input(colors.lightcyan('Please enter the command you want for the action %s\n' % colors.green(item)))

			# return values if sequences has been entered before 
			if i in usedlist:
				print(colors.orange('%s has been used.' % i),colors.lightred('\nPlease use another one instead!'))
				print(colors.lightblue('Your current list is %s' % str(usedlist)))
				waitForInput(colors)
				# emptyline is default set to true
				emptyline() 
				# Recursive func if user repeatedly inputs used functions
				return requestforinput(item, usedlist) 
			# returns value if values have not been used before  
			return i

		# create password table
		self.cursor.execute('''CREATE TABLE password(id INT, key TEXT, password TEXT)''')

		# create user command table
		self.cursor.execute('''CREATE TABLE commands(globalcmd TEXT, usrcmd TEXT)''')

		# create log table
		self.cursor.execute('''CREATE TABLE log(logtime TEXT, log TEXT)''')

		# create prerferences table
		self.cursor.execute('''CREATE TABLE userPreferences(
			sysdefname TEXT,description TEXT, type TEXT, Value TEXT, 'Default' TEXT, possible TEXT)''')
		self.log('Created file')

		self.cursor.executemany(
			'''INSERT INTO userPreferences VALUES(?,?,?,?,?,?)''', 
			# list of preferences avaliable
			[

			# System preferences in UI
			('verbose','Shows everything', 'bool', False, False, 'True,False'), 
			('copyAfterGet','Copy password after output', 'bool',True, True, 'True,False'),
			('askToQuit','Ask before quit','bool',False, False, 'True,False'),
			('customColor','Use custom color', 'bool',True, True, 'True,False'),
			('logLogin','Record Logins','bool',True,True, 'True,False'),

			# Exports preferences
			('encExpDb','Export files are encrypted','bool',True, True, 'True,False'),
			('useDefLoc','Use default export location','bool',True, True, 'True,False'),
			('exportType','Export type','str in list','db','db ', 'csv,db,json,txt'),
			('defExpLoc','Default export location', 'location','~/Documents','~/Documents', 'Any folder'),

			# Backup preferences
			('createBcF','backup','bool',True, True, 'True,False'),
			('backupFileTime','Backup Passwords time','str in list','d','d','h,d,w,2w,m,2m,6m,y,off'),
			('backupLocation','The location of back-up','location','~/Library/.pbu', '~/Library/.pbu','Any folder'),
			('hashBackupFile','Hashing the Backup File', 'bool', True,True, 'True,False'),

			# Extrasecure 
			('hashUserFile', 'Hash User File Name', 'bool', False,False, 'True,False'),
			('createRandF','Creates random nonsense files', 'bool',False, False, 'True,False')
			])

		# Save master password
		self.cursor.execute('''INSERT INTO password VALUES (0,'master',?)''', (
			# hashing
			hashlib.pbkdf2_hmac(
			# security level sha-512
			'sha512',
			# user inputted password-->binary values encoded in utf-32
			self.__password.encode('utf-32'),
			# salt is generated by encrypting the user's password
			''.join(sorted(self.__password)).encode('utf-32'),
			# times
			750000).hex(),))


		# different shortcuts avaliable
		actions = ['get','new','change password','generate','quit','delete','change command','exportpwd','exportlog','import file','user preferences',
		'backup now'] 
		
		# built in function for 'Help'
		defactions = ['??'] 

		# Enters default function--> Help
		self.cursor.execute('''INSERT INTO commands VALUES (?,?)''', ('help',encsp('??', self.__password)))

		for items in actions: 
			# inputs user-defined passwords
			ucmd = requestforinput(items, defactions)
			defactions.append(ucmd)

			# saves user defined actions
			self.cursor.execute('''INSERT INTO commands VALUES(?,?)''', (items, encsp(ucmd, self.__password))) 
			emptyline() if not self.verbose else None

		# Logs command input

		# Saves file
		self.file.commit()

		# build backup file
		os.mkdir(os.path.join(os.path.expanduser('~/Library'),'.pbu','.'+ hashlib.pbkdf2_hmac('sha224', self.userName.encode('utf-32'),
		 b'e302b662ae87d6facf8879dc1dabc573', 500000).hex()))

		self.buildActionsPreferences()

		self.log('Preferences set')
		self.log('Stored master password')
		self.log('User commands inputted')
		self.log('Backup file built')
		self.file.commit()

	def login(self):
		try:
			self.buildActionsPreferences()
			# Compares hashes
			hexHash = hashlib.pbkdf2_hmac('sha512',self.__password.encode('utf-32'),''.join(sorted(self.__password)).encode('utf-32'),750000).hex()
			if self.cursor.execute('''SELECT password FROM password WHERE id = 0''').fetchone()[0] == hexHash :
				print(colors.darkgrey('Login success!')) if self.verbose else None
				self.log('Logged in') if bool(int(self.preferences.get('logLogin'))) else None
			else:
				self.log('Failed attempt') if bool(int(self.preferences.get('logLogin'))) else None
				raise WrongPassWordError
				print(colors.darkgrey('Wrong password. Raise WrongPasswordError')) if self.verbose else None

		# WrongPasswordError is raised if user entered a wrong password 
		except WrongPassWordError:
			print(colors.darkgrey('Module level error raised. Raise error in __main__')) if self.verbose else None
			raise
		emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None

	def log(self, action):
		print(colors.darkgrey(f'Logging {action} into log file')) if self.verbose else None
		# Logs exact time and Action
		self.cursor.execute('''INSERT INTO log VALUES(?,?)''',
			(encsp(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S:{}".format(str(datetime.now().microsecond)[:-3]))),
			 self.__password),encsp(action, self.__password)))
		# saves file 
		self.file.commit()

	def get(self):
		self.log('Called function get')
		# Ask for user input
		getValue = input(colors.lightblue('Please enter what do you want to get\n'))
		emptyline() if not self.verbose else None
		print(colors.darkgrey('Loading from database and looking for entries with Key %s' % getValue)) if self.verbose else None

		# Get all values -> Select * From Password
		if getValue == '*':
			self.log('Requested for all key, output printed')
			print(colors.darkgrey('Generating key sequences from database')) if self.verbose else None
			print(colors.orange('The list of your keys are:'))

			print(colors.darkgrey('Getting key from '))
			# only print the key (search query) of all. Prevents data beach
			for k in [encsp(i[1], self.__password) for i in self.cursor.execute('SELECT * FROM password').fetchall()[1:]]:
				print(colors.orange(k))

			waitForInput(colors)
			emptyline() if not self.verbose else None

			# save file
			self.file.commit()
			print(colors.darkgrey('All values outputted. Calling recursive function.')) if self.verbose else None
			return self.get()

		if getValue == 'master':
			# user tries to get login password, returns fail 
			print(colors.darkgrey('User requesting for master key\ndDecrypt error raised\nReturns back to get branch\nRe-raising  to user level')) if self.verbose else None
			print(colors.red('Warning:'),colors.lightred('"Master"'),colors.blue('password is hashed and cannot be retrieved. Sorry!'))
			waitForInput(colors)

			# Logs user error
			self.log('Requested for master password, Error raised.')
			emptyline() if not self.verbose else None

		else:	
			# Else --> Get value from key
			# Fetchone reduces an extra tuple and increases running time

			getResult = self.cursor.execute('SELECT * FROM password WHERE key =(?)', (encsp(getValue, self.__password),)).fetchone()
			# If key exists -->
			if getResult is not None:
				print(colors.darkgrey('Value has been retrieved from database\nDecrytping password')) if self.verbose else None
				# Logs user have requeted for a valid result
				self.log('Searched for %s, valid output printed' % getValue)

				# Format to 20 px
				print(colors.cyan('{0:20}'.format(encsp(getResult[1], self.__password))),
				 '|', colors.lightgreen('{0:60}'.format(dec(getResult[2], self.__password))))

				# Check if user preferences set to copy
				copy = self.preferences.get('copyAfterGet')

				# Copies outputted password
				if copy:
					print('Copying password to clipboard') if self.verbose else None

					# Pyperclip syntax to copy password
					pyperclip.copy(dec(getResult[2], self.__password))

					# Tell the user password has been copied
					print(colors.lightgrey('Your password has been copied!'))

					self.log('Copied password')

				waitForInput(colors)

				emptyline() if not self.verbose else None

			# Search query not valid
			else:
				print(colors.darkgrey('Database cannot find key matching value %s' % getValue)) if self.verbose else None
				print(colors.lightred('This is not a valid value in your table! Please choose again!'))

				# logs invalid
				self.log('Searched for %s, invalid result' %getValue)
				waitForInput(colors)
				emptyline() if not self.verbose else None
				# Saves file as we are not gonna hit :saveFile line
				self.file.commit()
				print('Returning to beginning of function $get') if self.verbose else None
				# Goes back to beginning of get()
				self.get()


		# Saves log
		self.file.commit()
		emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def new(self):
		self.log('Called function new')
		# Inserts new key into database
		print(colors.darkgrey('Grabbing current keys from database')) if self.verbose else None
		currentKeys = [encsp(x[1], self.__password) for x in self.cursor.execute('SELECT * FROM password').fetchall()]
		# Asks for key value
		newInputKey = input(colors.cyan('Please enter what do you want to enter:\n'))
		print(colors.darkgrey('Looking through current keys')) if self.verbose else None

		if newInputKey in currentKeys:
			print('%s is found in current Keys') if self.verbose else None
			# New key is already used
			self.log('Used value is re-inputted[new], no value is updated')
			print(colors.red('{} has been used! Please use a distinct key instead!'.format(newInputKey)))
			waitForInput(colors)
			emptyline() if not self.verbose else None
			print(colors.darkgrey('Going back to $new function')) if self.verbose else None
			return self.new()

		generateKeyword = self.actions['generate']
		print(colors.darkgrey('Getting generate keyword from preference database')) if self.verbose else None

		# Asks for new password

		print(colors.red('Please enter the new password:'),colors.green('\nYou can enter your generate keyword'),
		 colors.yellow(generateKeyword), colors.green('to generate one.'))
		newPassword = input()


		if newPassword == generateKeyword:
			print(colors.darkgrey('Generating key\nCalling $random')) if self.verbose else None
			print('Generate')
			# generates password
			newPassword = randomPwd()
			print(colors.darkgrey('Random password is generated\ncopying new password to clipboard')) if self.verbose else None
			# Copies password
			pyperclip.copy(newPassword)
			self.log('A new password is generated')
			print(colors.orange('This password has been copied'))

		emptyline() if not self.verbose else None

		print(colors.darkgrey('Generating index for this password')) if self.verbose else None
		# Gets current max index-> figures out the index value of this password
		currentIndex = max(int(x[0]) for x in self.cursor.execute('''SELECT * FROM password''').fetchall()) + 1

		print(colors.darkgrey('Encrypting password...')) if self.verbose else None
		# Encrypts the password
		encryptedPassword = enc(newPassword, self.__password)

		print(colors.darkgrey('Inserting password into database')) if self.verbose else None
		# Saves password into database with key and index
		self.cursor.execute('''INSERT INTO password VALUES(?,?,?)''', (currentIndex, encsp(newInputKey, self.__password), encryptedPassword))

		# Logs the saved password
		self.log('Inserted new password %s' % newInputKey)

		print(colors.darkgrey('Deleting unencrypted password string')) if self.verbose else None
		# Deletes variables to prevent data breach
		del(encryptedPassword, newInputKey,newPassword)
		print(colors.yellow('Success!'))
		waitForInput(colors)
		emptyline() if not self.verbose else None

		print('Saving file') if self.verbose else None
		# Saves file--> Log and password
		self.file.commit()
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def changePassword(self):
		self.log('Called action changePassword')
		# Requests for password--> Requests for authenication
		oldPassword = input(colors.yellow('Please enter your old password\n'))

		# Requests for new password --> Used to encrypt user data
		newEncPassword = input(colors.red('Please enter your new password\n'))
		emptyline() if not self.verbose else None

		print(colors.darkgrey('Getting hashed password from database')) if self.verbose else None
		# select all password db in current password database
		curPwds = [x for x in self.cursor.execute('SELECT * FROM password').fetchall() if x[0] != 0]

		print(colors.darkgrey('Hashing old user password')) if self.verbose else None
		oldPassword = str(hashlib.pbkdf2_hmac('sha512', str(oldPassword).encode('utf-32'),
		''.join(sorted(oldPassword)).encode('utf-32'),
		300000).hex()) + str(hashlib.pbkdf2_hmac('sha512',
		str(oldPassword).encode('utf-32'), ''.join(sorted(oldPassword, reverse=True)).encode('utf-32'), 300000).hex())

		# Checks if password hash matches saved hash
		print(colors.darkgrey('Checking hashsum')) if self.verbose else None
		if not hashlib.pbkdf2_hmac(
			# security level sha-512
			'sha512',
			# user inputted password-->binary values encoded in utf-32
			self.__password.encode('utf-32'),
			# salt is generated by encrypting the user's password
			''.join(sorted(oldPassword)).encode('utf-32'),
			# times
			750000).hex() == self.cursor.execute(
			'SELECT password FROM password WHERE id = 0').fetchone()[0]:
			print(colors.darkgrey('Checksums don\'t match')) if self.verbose else None
			print(colors.red('WrongPasswordError:'), colors.green('You entered the wrong password! Please try again!'))
			waitForInput(colors)
			print(colors.darkgrey('Quitting $changepassword function')) if self.verbose else None
			return None

		print(colors.darkgrey('Hashsums match\nRemoving old passwords')) if self.verbose else None
		# deletes all from database 
		self.cursor.execute('DELETE FROM password')

		print(colors.darkgrey('Hashing new password')) if self.verbose else None
		# Inserts new passwords into database 
		newEncPassword = str(hashlib.pbkdf2_hmac('sha512', str(newEncPassword).encode('utf-32'),
		''.join(sorted(newEncPassword)).encode('utf-32'),
		300000).hex()) + str(hashlib.pbkdf2_hmac('sha512',
		str(newEncPassword).encode('utf-32'), ''.join(sorted(newEncPassword, reverse=True)).encode('utf-32'), 300000).hex())

		print(colors.darkgrey('Generating new passwords')) if self.verbose else None
		# Hashing new password
		newPwds = [(0, 'master',
		hashlib.pbkdf2_hmac('sha512',newEncPassword.encode('utf-32'),''.join(sorted(newEncPassword)).encode('utf-32'), 750000).hex())
		]
		print(colors.darkgrey('Encrypting new passwords')) if self.verbose else None
		totalPasswords = len(curPwds)
		for count, currentPwds in enumerate(curPwds):
			print(colors.darkgrey('Encryting new password %s in %s' %(str(count), str(totalPasswords)))) if self.verbose else None
			newPwds.append((currentPwds[0], encsp(encsp(currentPwds[1],self.__password),newEncPassword), enc(dec(currentPwds[2], self.__password), newEncPassword)))
		print(colors.darkgrey('Inserting new passwords into database')) if self.verbose else None
		self.cursor.executemany('INSERT INTO password VALUES(?,?,?)', newPwds)

		print(colors.darkgrey('Updating new password')) if self.verbose else None
		# Sets user password to the new password
		self.__password = newEncPassword

		# Updates logs by encsp
		newlogs = []
		print(colors.darkgrey('Collecting current logs')) if self.verbose else None
		for items in [(encsp(x[0], oldPassword), encsp(x[1], oldPassword)) for x in self.cursor.execute('SELECT * FROM log').fetchall()]:
			newlogs.append((encsp(items[0], newEncPassword), encsp(items[1], newEncPassword)))
		print(colors.darkgrey('Deleting old logs from database\nUpdating new logs')) if self.verbose else None
		self.cursor.execute('''DELETE FROM log''')
		self.cursor.executemany('''INSERT INTO log VALUES (?,?)''',newlogs)

		userCommands = []
		print(colors.darkgrey('Collecting current user commands')) if self.verbose else None

		# updatet commands by encso
		for items in [(x[0], encsp(x[1], oldPassword)) for x in self.cursor.execute('''SELECT * FROM commands''').fetchall()]:
			userCommands.append((items[0], encsp(items[1], newEncPassword)))


		print(colors.darkgrey('Deleting user commands from database\nUpdating user commands')) if self.verbose else None

		# Deletes commands from databases and inputs newly encrypted user commands
		self.cursor.execute('''DELETE FROM commands''')
		self.cursor.executemany('''INSERT INTO commands VALUES (?,?)''', userCommands)
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		emptyline() if not self.verbose else None

		return None

	def backup(self,oldbackupName=''):

		oldbackupName = self.userName if len(oldbackupName)==0 else oldbackupName
		# Save after log 
		self.log('CreatedBackup')
		print(colors.darkgrey('Backup created\nFile saved')) if self.verbose else None
		self.file.commit()

		print(colors.green('Backing up....'))

		# Generates backup db name
		now = time.time()

		print(colors.darkgrey('Getting current time success')) if self.verbose else None
		fileTime = str(time.localtime(now).tm_year).zfill(4) + str(time.localtime(now).tm_yday).zfill(3) + str(time.localtime(now).tm_hour).zfill(2)

		print(colors.darkgrey('Generating backup file name')) if self.verbose else None
		# Determines the backup db name by preferences
		backupName = hashlib.pbkdf2_hmac('sha224', 
						self.userName.encode('utf-32'), b'e302b662ae87d6facf8879dc1dabc573', 
						500000).hex() if self.preferences.get('hashBackupFile') else self.userName
		# Makes backup directory
		try:
			os.mkdir(os.path.join(os.path.expanduser(self.preferences.get('backupLocation')),'.'+backupName))
		except FileExistsError:
			pass

		print(colors.darkgrey('Creating backup file')) if self.verbose else None
		# joins path to determine file location
		backupFile = os.path.join(os.path.expanduser(self.preferences.get('backupLocation')),'.' + backupName,'.' +fileTime+'.db')


		print(colors.darkgrey('Copying file to backup folder')) if self.verbose else None
		# shutil.copy is willing to replace
		# Copies file to backup file
		shutil.copy2(os.path.join(os.path.expanduser('~/.password'), '.' + oldbackupName+'.db'), backupFile)
		print(colors.darkgrey('.....Success!'))
		# Logs backup
		self.log('Backup copied successfully')
		emptyline() if not self.verbose else None
		return None

	def checkBackup(self):
		print(colors.blue('Checking auto backup'))
		# logs checking backup
		self.log('Checking Backup')

		# time format relates to numbers
		timeD = {'h': 1,'d': 100,'w': 700,'2w': 1400,'m': 3000,'2m': 6000,'6m': 18000,'y' : 100000}

		print(colors.darkgrey('Connecting to user backup folder')) if self.verbose else None
		# gets the user backup file name
		backupName = hashlib.pbkdf2_hmac('sha224', 
						self.userName.encode('utf-32'), 
						b'e302b662ae87d6facf8879dc1dabc573', 
						500000).hex() if self.preferences.get('hashBackupFile') else self.userName

		# get the time of the latest backup
		try:
			print(colors.darkgrey('Getting user backup histories')) if self.verbose else None
			latestBackup = max([int(fName[1:-3]) for fName in [files for r, d,files in os.walk(os.path.join(
				os.path.expanduser(self.preferences.get('backupLocation')),'.'+ backupName))][0]])
		except ValueError:
			print(colors.darkgrey('No backup can be retrieved'))  if self.verbose else None
			self.backup() if user.preferences.get('createBcF') else None
			return None

		# Gets current time
		print(colors.darkgrey('Getting current time\nGenerating backup name')) if self.verbose else None
		now = time.time()
		currentTime = int(str(time.localtime(now).tm_year).zfill(4) +
		 str(time.localtime(now).tm_yday).zfill(3) + str(time.localtime(now).tm_hour).zfill(2))

		# Backs up if the difference is bigger than the time user needs to auto-backup
		print(colors.darkgrey('Comparing backup dates')) if self.verbose else None
		if ((currentTime - latestBackup) >= timeD.get(self.preferences.get('backupFileTime'))):
			print(colors.cyan('Backup needed'))
			self.backup()
			print(colors.lightgreen('Backup finished'))
		else:
			print(colors.cyan('No backup needed'))
			self.log('No auto backup needed') 
		print(colors.darkgrey('Backup checking finished')) if self.verbose else None
		print(colors.lightblue('Auto-backup check finished'))
		time.sleep(random.random())
		self.log('Auto backup check finished')
		return None

	def changeCommand(self):
		self.log('called function changeCommand')
		def requestforinput(item, usedlist): 

			# Does not allow duplicates
			i = input(colors.lightcyan('Please enter the command you want for the action %s\n' % colors.green(item)))

			print(colors.darkgrey('Checking if inpputted item has been used in current commands')) if self.verbose else None
			# return values if sequences has been entered before 
			if i in usedlist:

				print(colors.orange('%s has been used.' % i),colors.lightred('\nPlease use another one instead!'))
				print(colors.lightblue('Your current list is %s' % str(usedlist)))
				waitForInput(colors)
				emptyline() if not self.verbose else None
				# Recursive func if user repeatedly inputs used functions
				return requestforinput(item, usedlist) 
			# returns value if values have not been used before  
			print(colors.darkgrey('Command is not used. Usage accepted')) if self.verbose else None
			return i

		print(colors.darkgrey('Generating user possible actions')) if self.verbose else None
		# List of user actions possible
		userActions = [

		# Gets user password stored in database
		'get',

		# inputs new password
		'new',

		# Changes user password
		'change password',

		# generates a password of len(19)
		'generate',

		# quit program
		'quit',
		
		# Delete item from file
		'delete',
		
		# Change user commands
		'change command',
		
		# Export password database
		'exportpwd',
		
		# Export user log
		'exportlog',
		
		# Imports user file from backup
		'import file',
		
		# Set user preferences
		'user preferences',
		
		# User manual backup
		'backup now', 
		
		# Asks for help --> Show manual chart
		'help'

		] 

		print(colors.darkgrey('Deleting commands from database')) if self.verbose else None
		self.cursor.execute('DELETE FROM commands')

		# Builds new encrypted user actions
		usedActions = []
		for items in userActions: 
			print(colors.darkgrey('Requests for user input items %s' % items)) if self.verbose else None

			# inputs user-defined passwords
			userCommand = requestforinput(items, usedActions)
			print(colors.darkgrey('Command was usable')) if self.verbose else None
			usedActions.append(userCommand)

			print(colors.darkgrey('Insert command into database')) if self.verbose else None
			# saves user defined actions
			self.cursor.execute('''INSERT INTO commands VALUES(?,?)''', (items, encsp(userCommand, self.__password)))
			emptyline() if not self.verbose else None
		self.file.commit()

		# Commands have been changed, rebuild actions.
		self.buildActionsPreferences()
		emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def quit(self):
		self.log('Called quit')
		# Raises quit -->Goes to global scope before quits
		if self.preferences.get('askToQuit'):
			print(colors.darkgrey('askToQuit returns true')) if self.verbose else None
			print(colors.red('Are you sure to quit?[yn]'))
			q = readchar.readchar()
			if q != 'y':
				print(colors.darkgrey('Choice %s != "y"' %q)) if self.verbose else None
				return None
		print(colors.darkgrey('Raising normalQuit')) if self.verbose else None
		raise normalQuit

	def delete(self):
		self.log('Called function delete')
		print(colors.darkgrey('Getting current passwords')) if self.verbose else None
		# Get current passwords
		currentPwds = [(x[0], encsp(x[1],self.__password), x[2]) for x in self.cursor.execute('SELECT * FROM password').fetchall()[1:]]
		print(colors.darkgrey('Getting terminal size')) if self.verbose else None
		# Get terminal size
		currentTerminalSize = shutil.get_terminal_size().lines - 10
		currentTerminalClmn = shutil.get_terminal_size().columns
		i = 0
		print(colors.blue(f'This here are all your passwords. There are {len(currentPwds)} of them in total'))
		try:
			while i < len(currentPwds):
				print('{0:18}|{1:10}'.format(colors.yellow('index'), colors.green('key')))
				print(colors.lightgreen('-'*currentTerminalClmn))
				for m in range(currentTerminalSize):
					print('{index:18}|{key:10}'.format(index=colors.yellow(currentPwds[i][0]), key=colors.green(currentPwds[i][1])))
					i += 1
				waitForInput(colors)
				emptyline()
		except IndexError:
			print(colors.lightgreen('-'*currentTerminalClmn))
			print(colors.darkgrey('All passwords outputted')) if self.verbose else None
			waitForInput(colors)
			pass
		# Prints current password Index and Key

		correctInput = False
		# Allows error inputs, goes back to this line after error inputs
		while not correctInput:
			try:
				print(colors.orange('Which of these do you want to delete?\nSyntax:\n[Delete with index inputted]: "i 1"'))
				print(colors.orange('[Delete with key inputted]: "n gmail"\nPress "h" if you want to display all your passwords again.\n'))
				delete = input()
				# Ask for input
				action = str(delete.split()[0]).lower()
				fileToDel = str(' '.join(delete.split()[1:]))
				# split gives out a list, ''join() returns back a string
				if action == 'i':
					print(colors.darkgrey('Searching by index')) if self.verbose else None
					# Search by index
					fileToDel = currentPwds[int(fileToDel) - 1][0]
					correctInput = True
				elif action == 'n':
					print(colors.darkgrey('Search by key')) if self.verbose else None
					# search by name
					fileToDel = [str(x[0]) for x in currentPwds if str(x[1]) == str(fileToDel)][0]
					correctInput = True
				elif action == 'h':
					print(colors.darkgrey('Regenerating user databases')) if self.verbose else None
					# Requests to input again
					waitForInput(colors)
					emptyline()
					return self.delete()
				else:
					print(colors.darkgrey('Not a valid value inputted')) if self.verbose else None
					# User enters jibberish
					raise ValueError
			except (IndexError, ValueError) as err:
				print(colors.darkgrey('IndexError or ValueError is raised')) if self.verbose else None
				# Goes back to line right after while 
				print(colors.red('This is not a valid value in your database! Please try again'))
				waitForInput(colors)
				emptyline()
				correctInput = False
				continue
		print(colors.darkgrey('Getting user entry ')) if self.verbose else None
		file = self.cursor.execute('SELECT key FROM password WHERE id = (?)', (fileToDel,)).fetchone()[0]
		# get file name
		print(colors.red('Are you sure you want to delete %s\'s stored password?' % encsp(file, self.__password)))
		print(colors.red('The only way you would retrieve this password is from the most recent backup [yn]'))
		k = readchar.readchar()
		if k.lower() != 'y':
			print(colors.darkgrey('User input %s != y'% k)) if self.verbose else None
			print(colors.blue('Password not deleted'))
			waitForInput(colors)
			emptyline() if not self.verbose else None
			self.log('Password not deleted')
			print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
			return None

		print(colors.darkgrey('Deleting entry from database')) if self.verbose else None
		self.cursor.execute('''DELETE FROM password WHERE id = (?)''', (fileToDel,))
		# Delete from database
		print(colors.green(f'Password from {str(encsp(file, self.__password))} deleted'))
		self.log(f'Deleted password from{str(encsp(file, self.__password))}')
		# saves file
		self.file.commit()
		emptyline() if not self.verbose else None
		return None

	def help(self):
		self.log('Called function help')
		# Prints user help, lists all actions
		print(colors.darkgrey('Getting user current commmands')) if self.verbose else None
		for userActions in self.actions.items():

			# Formatted user actions
			print(colors.cyan('{0:16}'.format(userActions[0]))+'||', colors.lightgreen('{0:16}'.format(userActions[1])))
		waitForInput(colors)

		# Clears listed line , prevents data breach 
		emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def exportPassword(self):
		self.log('Called function exportPassword')
		print(colors.darkgrey('Getting export type from database\nGetting export location from database')) if self.verbose else None
		# Gets export file type
		exportType = self.preferences.get('exportType')
		# Gets export location
		exportLocation = self.getExportLocation(bool(self.preferences.get('useDefLoc')))
		print(colors.darkgrey('Getting current passwords')) if self.verbose else None
		# Exports as different file
		currentFiles = [(x[0], encsp(x[1], self.__password), x[2]) for x in self.cursor.execute('SELECT * FROM password').fetchall()]
		if os.path.isfile(os.path.join(exportLocation, self.userName + '.' + exportType)):
			print(colors.darkgrey('Export is found in export file'))
			# Export already exists
			print(colors.yellow('You already have an exported file in %s! Please try again!') % exportLocation) if self.verbose else None
			self.log('Export location has repeated file, password not exported')
			waitForInput(colors)
			emptyline() if not self.verbose else None
			return None
		print(colors.darkgrey('Saving file')) if self.verbose else None
		self.file.commit()
		print(colors.darkgrey('Responding to exportType')) if self.verbose else None
		if exportType == 'db':
			print(colors.darkgrey('Connecting to export file\nCreating cursor object')) if self.verbose else None
			# Database
			exportFile = sqlite3.connect(os.path.join(exportLocation ,self.userName + '.db'))
			# Creates export db file
			exportCursor = exportFile.cursor()
			exportFile.commit()
			print(colors.darkgrey('Creating database table')) if self.verbose else None
			exportCursor.execute('CREATE TABLE exportedPasswords (id char NOT NULL, key TEXT, password TEXT)')
			# Creates cursor and table
			self.log('Password Export Created')
			for entries in currentFiles:
				print(colors.darkgrey('Writing current data into database %s/%s'%(str(currentFiles.index(entries)), str(len(currentFiles))))) if self.verbose else None
				# Insert all entries into export database
				if entries[0] != 0:
					# Inserts values -- can be decryted
					if bool(self.preferences.get('encExpDb')): 
						exportCursor.execute('INSERT INTO exportedPasswords values (?,?,?)', (entries[0], encsp(entries[1], self.__password), entries[2]))
					else: 
						exportCursor.execute('INSERT INTO exportedPasswords values (?,?,?)', (entries[0], encsp(entries[1], self.__password),dec(entries[2], self.__password)))
				else:
					# Inserts values -- hashed and cannot be decrypted
					exportCursor.execute('INSERT INTO exportedPasswords values (?,?,?)',(entries[0], encsp(entries[1], self.__password), entries[2]))
			print(colors.darkgrey('Saving and closing file')) if self.verbose else None
			exportFile.commit()
			exportCursor.close()
			# Saves File and closes file

		else:
			print(colors.darkgrey('Creating backup file\nOpening file')) if self.verbose else None
			with open(os.path.join(exportLocation, self.userName + '.' + exportType), 'w') as exportFile:
				self.log('Password Export Created')
				if exportType == 'txt':
					print(colors.darkgrey('Initialising folder')) if self.verbose else None
					# Text file
					exportFile.write('{0:20} {1}'.format('Password key', 'Password'))
					# Creates header in txt file
					for entries in currentFiles:
						print(colors.darkgrey('Writing entries into file: {0}/{1}'.format(currentFiles.index(entries),
						len(currentFiles)))) if self.verbose else None
						if currentFiles[0] != entries:
							# Write - can be decrypted
							decOrNo = entries[2] if bool(self.preferences.get('encExpDb')) else dec(entries[2], self.__password)							
							exportFile.write('{0:20}:{1}\n'.format(encsp(entries[1], self.__password), decOrNo)) 
						
						else:
							# Write -Hashed
							exportFile.write('{0:20}:{1}\n'.format(encsp(entries[1], self.__password), entries[2]))
				
				elif exportType == 'csv':
					print(colors.darkgrey('importing python csv module')) if self.verbose else None
					# Cursor seperated files
					import csv
					# import the python in-built csv modle
					print(colors.darkgrey('Creating csv writer object\nInitialising folder')) if self.verbose else None
					csvWriter = csv.writer(exportFile)

					# Creates header in csv files
					csvWriter.writerow(['Password key', 'Password'])
					# Use standardized csv writer because ',' could appear in encrypted passwords
					for entries in currentFiles:
						print(colors.darkgrey('Writing entries into files: {0}/{1}'.format(currentFiles.index(entries),
							len(currentFiles)))) if self.verbose else None
						# Items saved
						if currentFiles[0] != entries:
							# Write - can be decrypted
							decOrNo = entries[2] if bool(self.preferences.get('encExpDb')) else dec(entries[2], self.__password)
							csvWriter.writerow([encsp(entries[1],self.__password), decOrNo])

						else:
							# Write - hashed cannot be decrypted
							csvWriter.writerow([encsp(entries[1], self.__password), entries[2]])

				elif exportType == 'json':
					print(colors.darkgrey('Importing python json module')) if self.verbose else None
					# I first disliked this but its actually fine -- json files. 12/12/19
					import json
					# import the in-built json module

					encList = {}
					# Json file only takes 'dict' type entries

					for entries in currentFiles:
						print(colors.darkgrey('Updating dictionary item: {0}/{1}'.format(currentFiles.index(entries),
						len(currentFiles)))) if self.verbose else None
						# Enters into dictionary first
						if currentFiles[0] != entries:
							# updates dictionary -- can be decrypted
							decOrNo = entries[2] if bool(self.preferences.get('encExpDb')) else dec(entries[2], self.__password)
							encList.update({encsp(entries[1], self.__password): decOrNo})

						else:
							# updates dictionary -- cannot be decrypted
							encList.update({encsp(entries[1], self.__password): entries[2]})

					print(colors.darkgrey('Dumping dictionary items into json file')) if self.verbose else None
					# Put into file
					json.dump(encList, exportFile)
		print(colors.darkgrey('All entries inputted into export files')) if self.verbose else None
		print(colors.red('DONE'))
		# Tells user action has been finished

		self.log('Export Password finished')
		print(colors.yellow('Export created'))
		waitForInput(colors)

		emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def getExportLocation(self, forceenter):
		# Gets user Export Location //From preferences
		print(colors.darkgrey('Getting user export locations')) if self.verbose else None
		exportLocation = ''
		if forceenter:
			print(colors.darkgrey('Using default export location')) if self.verbose else None
			exportLocation = os.path.expanduser(self.preferences.get('defExpLoc'))
		else:
			print(colors.darkgrey('Not using defualt export location.\nRequesting User input')) if self.verbose else None
			exportLocation = input(colors.red('Please enter your desired export location in command prompt syntax\n(e.g.: "~/Documents")\n>>>'))
		# Expands location if user uses command line prompt syntax
		print(colors.darkgrey('Getting current working directory\n{0}\nExpanding export location'.format(os.getcwd()))) if self.verbose else None
		exportLocation = os.path.expanduser(exportLocation)

		# Instances of error --> Not an actual location, Folder not accessible
		if not os.path.isdir(exportLocation):
			print(colors.darkgrey('Connecting file...failed\nReturn error:file does not exist')) if self.verbose else None
			# Not an actual location
			print(colors.lightred('%s is not a valid export location, please try again!' % exportLocation))
			waitForInput(colors)
			return(getExportLocation(self, False))

		elif not os.access(exportLocation, os.W_OK):
			print(colors.darkgrey(
				'Connecting file...Success!\nTrying to create file...Failed\nReturn error: dir not accessible')) if self.verbose else None
			# Folder not accessible
			print(colors.red('%s is not accessable by this python module. \nPlease either use another location or run this application with sudo!'))
			waitForInput(colors)
			return(getExportLocation(self, False))
		else:
			print(colors.darkgrey(
				'Connectinf file...Success!\nTrying to create file...Success!\nReturn Valid Dir')) if self.verbose else None
			emptyline if not self.verbose else None
			return exportLocation

	def exportLog(self):
		self.log('Called function exportLog')
		print(colors.darkgrey('Getting export file type')) if self.verbose else None
		# Exports user log
		exportType = self.preferences.get('exportType')

		print(colors.darkgrey('Getting current logs from database')) if self.verbose else None
		# Current logs
		cLogs = [(encsp(x[0], self.__password), encsp(x[1], self.__password)) for x in self.cursor.execute('SELECT * FROM log').fetchall()]

		print(colors.darkgrey('Getting export location')) if self.verbose else None
		# Gets users export location
		exportLocation = self.getExportLocation(bool(self.preferences.get('useDefLoc')))
		# get backup location
		print('Checking export file') if self.verbose else None
		if os.path.isfile(os.path.join(exportLocation, self.userName +'_LOGS'+ '.' + exportType)):
			print('Export file found') if self.verbose else None
			# Export already exists
			print(colors.yellow('You already have an exported file in %s! Please try again!') % exportLocation)
			self.log('Export location has repeated file, password not exported')
			waitForInput(colors)
			emptyline() if not self.verbose else None
			return None

		self.log('Asked for Log output request')

		if exportType == 'db':
			print(colors.darkgrey('Creating database file, connecting database and creating cursor object')) if self.verbose else None
			# Database
			exportFile = sqlite3.connect(os.path.join(exportLocation ,self.userName +'_LOGS'+ '.db'))
			self.log('Export Created')
			# Creates export db file
			exportCursor = exportFile.cursor()
			exportFile.commit()
			print(colors.darkgrey('Creating database table LOGS')) if self.verbose else None
			exportCursor.execute('CREATE TABLE logs (Timestamp TEXT NOT NULL, command TEXT)')
			# Creates cursor and table
			self.log('Logs exported')
			print(colors.darkgrey('Inserting log values into database')) if self.verbose else None
			exportCursor.executemany('INSERT INTO logs VALUES(?,?)', cLogs)
			print(colors.darkgrey('Saving export file and closing file')) if self.verbose else None
			exportFile.commit()
			exportCursor.close()
			# Saves File and closes file
		else:
			print(colors.darkgrey('Creating export file')) if self.verbose else None
			with open(os.path.join(exportLocation, self.userName +'_LOGS'+ '.' + exportType), 'w') as exportFile:
				self.log('Password Export Created')
				if exportType == 'txt':
					# Text file
					print(colors.darkgrey('File created.\nInitialising file')) if self.verbose else None
					exportFile.write('{0:30} {1}'.format('Timestamp', 'Action'))
					# Creates header in txt file
					for entries in cLogs:
						print(colors.darkgrey('Writing logs into output file: {}/{}'.format(cLogs.index(entries),
							len(cLogs)))) if self.verbose else None
						exportFile.write('{0:30}:{1}\n'.format(entries[0], entries[1]))
				
				elif exportType == 'csv':
					print(colors.darkgrey('Importing python csv module')) if self.verbose else None
					# Cursor seperated files
					import csv
					# import the python in-built csv modle
					print(colors.darkgrey('Connecting file\nInitialising file')) if self.verbose else None
					csvWriter = csv.writer(exportFile)

					# Creates header in csv files
					csvWriter.writerow(['Timestamp', 'Action'])

					# Use standardized csv writer because ',' could appear in encrypted passwords
					for entries in cLogs:
						print(colors.darkgrey('Writiing logs into file, {}/{}'.format(cLogs.index(entries), len(cLogs)))) if self.verbose else None
						csvWriter.writerow([entries[0], entries[1]])

				elif exportType == 'json':
					print(colors.darkgrey('Importing python json module')) if self.verbose else None
					# I first disliked this but its actually fine -- json files. 12/12/19
					import json
					# import the in-built json module

					outputList = {}
					# Json file only takes 'dict' type entries

					for entries in cLogs:
						print(colors.darkgrey('Appending logs into dictionary: {}/{}'.format(cLogs.index(entries), 
							len(cLogs)))) if self.verbose else None
						outputList.update({entries[0]: entries[1]})

					# Put into file
					print(colors.darkgrey('Dumping dictionary into json file')) if self.verbose else None
					json.dump(outputList, exportFile)

		print(colors.darkgrey('All logs outputted\nFile closed')) if self.verbose else None
		print(colors.red('DONE'))
		# Tells user action has been finished

		self.log('Export Logs finished')
		print(colors.yellow('Export finished'))
		waitForInput(colors)

		emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def importFile(self):
		self.log('Called function importFile')
		# import files from backups 

		print(colors.darkgrey('Generating backup folder name')) if self.verbose else None
		# backup location
		backupName = hashlib.pbkdf2_hmac('sha224', 
						self.userName.encode('utf-32'), b'e302b662ae87d6facf8879dc1dabc573', 
						500000).hex() if self.preferences.get('hashBackupFile') else self.userName
		try:
			print(colors.darkgrey('Getting latest backup file')) if self.verbose else None
			# Could possibly return an error if no backup files could be found
			latestBackupFile = max([int(x[-12:-3]) for x in [f for d, b, f in os.walk(os.path.expanduser('~/Library/.pbu/.'+ backupName))][0]])
		except ValueError:
			print(colors.darkgrey('Fatal:No file can be retrieved')) if self.verbose else None
			print(colors.red('Error:'), colors.orange('The backup folder has no backups avaliable! We are sorry but we cannot extract your file!'))	
			return None
		# print(latestBackupFile)
		# change string into a datetime stamp
		print(colors.darkgrey('Formatting backup file time')) if self.verbose else None
		t = str(datetime.strptime(str(latestBackupFile), '%Y%j%H'))
		print(colors.green('Your latest backup is on {day} {around} {time}'.format(day=colors.purple(t.split()[0]),
		 around=colors.green('around'),time=colors.purple(t.split()[1][:5]))))
		# ask if the user actually wants to backup
		print(colors.pink('Do you want to restore from the copy?[yn]\nThis will quit the program'))
		yn = readchar.readchar()
		self.log('restored from backup')
		if yn == 'y':
			print(colors.darkgrey('Moving file from backup to current file')) if self.verbose else None
			# Copies the file and would replace current file
			shutil.copy2(
				os.path.join(os.path.expanduser('~/Library/.pbu/.' + backupName), '.'+str(latestBackupFile) + '.db'),
				# original file
				os.path.join(os.path.expanduser('~/.password'), '.' + self.userName + '.db'))
			print(colors.darkgrey('Done\nForce quit program\nRaise quit without backup')) if self.verbose else None
			waitForInput(colors)
			emptyline() if not self.verbose else None
			self.buildActionsPreferences()
		else:
			# File will not be imported
			print(colors.lightblue('File not imported'))
			self.log('File is not imported')
			waitForInput(colors)
			emptyline() if not self.verbose else None
		print(colors.darkgrey('Redirecting to user interface')) if self.verbose else None
		return None

	def changePreferences(self):
		self.log('Called function changePreferences')
		# get current preferences
		emptyline() if not self.verbose else None

		# Get a set of preferences and copy it
		oldPreferences = self.preferences.copy()
		print(colors.darkgrey('Fetching current preferences')) if self.verbose else None
		
		# Give out a list of 'preference' class
		# Change list of class to a big class in which changing operations can be done
		preferenceClass = alterPreferences([usrp(x, count) for count, x in enumerate(
			[row for row in self.cursor.execute('SELECT * FROM userPreferences').fetchall()], start=1)])
		print(colors.darkgrey('Building preference model')) if self.verbose else None

		# Assign preferences in class
		preferenceClass.buildPrefs()
		print(colors.darkgrey('Changing preference values')) if self.verbose else None

		# Change user prefrences in prefrence object '''recursive function!!''''
		preferenceClass.changePrefs()
		print(colors.darkgrey('Updating preferences...\nDeleting old values\nInserting new values')) if self.verbose else None

		# Delete old preferences
		self.cursor.execute('''DELETE FROM userPreferences''')
		# Add in new preferences
		self.cursor.executemany('''INSERT INTO userPreferences VALUES(?,?,?,?,?,?)''',
			[(x.key,x.description,x.valueType,x.value,x.default,x.avaliable) for x in preferenceClass.returnList()])
		print(colors.darkgrey('Building new preferences')) if self.verbose else None

		# Build user prefrences based on current preferernces
		self.buildActionsPreferences()

		print(colors.darkgrey('Getting differences'))if self.verbose else None

		# Get difference of preferences from two different sets
		difference = dict(set(self.preferences.items())-set(oldPreferences.items()))

		print(colors.darkgrey('Building new functions')) if self.verbose else None

		oldBackupName = self.userName if not oldPreferences.get('hashBackupFile') else hashlib.pbkdf2_hmac('sha224', 
				self.userName.encode('utf-32'), b'e302b662ae87d6facf8879dc1dabc573', 500000).hex() 
		print(colors.darkgrey('Getting old backup file...successful!\n%s'%oldBackupName)) if self.verbose else None

		# Gets old backup location
		oldBackupLocation = os.path.join(os.path.expanduser(oldPreferences.get('backupLocation')) ,'.'+oldBackupName)
		print(colors.darkgrey('Getting old backup location...successful!\n%s'%oldBackupLocation)) if self.verbose else None

		# Removes old backup folder
		if oldPreferences.get('createBcF'):


			print(colors.darkgrey('Deleting backup folder')) if self.verbose else None
			print(colors.darkgrey(f'The old backup folder has a size of {os.path.getsize(oldBackupLocation)}bytes')) if self.verbose else None

			# removes file
			shutil.rmtree(oldBackupLocation)

			print(colors.darkgrey('successful!')) if self.verbose else None

		# Value in dict key 'hashuserfile' is changed
		if 'hashUserFile' in difference.keys():
			print(colors.darkgrey('making copy of old userName')) if self.verbose else None
			# Make a copy of the old username
			oldUserName = self.userName
			print(colors.darkgrey('Gettting new user name')) if self.verbose else None

			# change from not hashing user file to hashing user file
			if self.preferences.get('hashUserFile'):
				print(colors.darkgrey('Hashing user name')) if self.verbose else None
				self.userName = hashlib.pbkdf2_hmac('sha224', self.userName.encode('utf-32'), b'08944de8a152170e823f865c7a41d75c', 500000).hex()

			# change from hashing user file to not hashing user file-->Need to re input username
			else:
				print(colors.darkgrey('Requesting new username')) if self.verbose else None
				self.userName = input('Please enter a new user name')
		else:
			print(colors.darkgrey('Setting username')) if self.verbose else None
			oldUserName = self.userName

		# Backup
		if any(x in difference.keys() for x in['hashUserFile','backupLocation','hashBackupFile']) or self.preferences.get('createBcF'):
			self.backup(oldUserName)

		# Create bunch of random file to make the creepers don't know what to do
		if 'createRandF' in difference.keys() and self.preferences.get('createRandF'):
			print(colors.red('You are about to run action "create random file", this is a one-way function. Are you sure you to proceed?[yn]'))
			randf = readchar.readchar()
			if randf != 'y':
				self.cursor.execute('''UPDATE userPreferences SET Value = 0 WHERE sysdefname = "createRandF"''')
			else:
				numsOfRandFiles = input('How many random files do you want to create?[number]')

				# User did not enter an integer
				if numsOfRandFiles.isdigit():
					print(colors.darkgrey('Good. You can read english')) if self.verbose else None
					numsOfRandFiles = int(numsOfRandFiles)

				# User did enter an integer
				else:
					print(colors.darkgrey('Seems like someone doesn\'t know what is "integer"\nSetting number to 50')) if self.verbose else None
					numsOfRandFiles = 50


				print(colors.yellow(f'Please allow up to {0.123*numsOfRandFiles} seconds'))
				createRandomFile(num=numsOfRandFiles, printall=self.verbose, color=colors.darkgrey)
				print(colors.yellow('Done!'))

		# Change user files
		if 'hashUserFile' in difference.keys():

			# Quits current file first
			self.cursor.close()
			self.file.commit()
			self.file.close()

			# Move file
			shutil.copy2(
				# Old user file
				os.path.join(os.path.expanduser('~'),'.password','.'+oldUserName+'.db'),
				# New user file
				os.path.join(os.path.expanduser('~'),'.password','.'+self.userName+'.db'))

			# Sets up current user file
			self.file = sqlite3.connect(os.path.join(os.path.expanduser('~'),'.password','.'+self.userName+'.db'))
			self.cursor = self.file.cursor()

			os.remove(os.path.join(os.path.expanduser('~/.password'),'.'+oldUserName+'.db'))

		print(colors.darkgrey('Redirecting to user interface'))	 if self.verbose else None
		return None