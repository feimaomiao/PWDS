import sqlite3, os, enc, random, time, sys, hashlib, shutil, readchar, pyperclip
from datetime import datetime, timedelta
from funcs import *
from enc import encrypt as enc, decrypt as dec, newd, EncryptionError

# user class. All actions are done under a class structure.
class userInterface():

	# __init__ builds the variables in class userInterface
	def __init__(self,filename, password):
		# build and/or connects the user database file
		self.file = sqlite3.connect(os.path.expanduser('~/.password/')+ '.%s.db' %filename)

		# creates cursor object for user database 
		self.cursor = self.file.cursor()

		# user password
		self.password = password

		# user actions and preferences will be filled in later
		self.actions = {}
		self.preferences = {}

		# Default verbose is False
		self.verbose = False

		# Get username
		self.userName = filename


	# builds the user actions and preferences
	def buildActionsPreferences(self):

		# builds user preferences
		for prefs in self.cursor.execute('''SELECT * FROM userPreferences''').fetchall():

			#get true/false/defined value
			self.preferences.update({prefs[0]: bool(int(prefs[3])) if prefs[3] in ['0','1', 0, 1] else prefs[3]}) 

		# builds user actions
		self.actions = {k: v for v, k in dict(self.cursor.execute('SELECT * FROM commands').fetchall()).items()}

		# Assign to verbose
		self.verbose = self.preferences.get('verbose')

		# Set colors after building user prefernces
		global colors
		colors = buildColors(self.preferences.get('customColor'))
		self.file.commit()

	def initialiseNewUser(self):

		def requestforinput(item, usedlist): 

			# Does not allow duplicatews
			i = input(colors.lightcyan('Please enter the command you want for the action %s\n' % colors.green(item)))

			# return values if sequences has been entered before 
			if i in usedlist:
				print(colors.orange('%s has been used.' % i),colors.lightred('\nPlease use another one instead!'))
				print(colors.lightblue('Your current list is %s' % str(usedlist)))
				waitForInput(colors)
				emptyline() if not self.verbose else None
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
		self.cursor.execute('''CREATE TABLE userPreferences(sysdefname TEXT,description TEXT, type TEXT, Value TEXT, 'Default' TEXT, possible TEXT)''')
		self.log('Created file')

		self.cursor.executemany(
			'''INSERT INTO userPreferences VALUES(?,?,?,?,?,?)''', 
			# list of preferences avaliable
			[

			# System preferences in UI
			('verbose','verbose', 'bool', False, False, 'True,False'), 
			('copyAfterGet','Copy after get', 'bool',True, True, 'True,False'),
			('askToQuit','Ask before quit','bool',False, False, 'True,False'),
			('customColor','Use custom color', 'bool',True, True, 'True,False'),
			('logLogin','log login','bool',True,True, 'True,False'),

			# Exports preferences
			('encryptExportDb','Exportdb as encrypted','bool',True, True, 'True,False'),
			('useDefaultLocation','Use default location','bool',True, True, 'True,False'),
			('exportType','Export type','str in list','db','db ', 'csv,db,json,txt'),
			('defaultExportLocation','Default export location', 'string',os.path.expanduser('~/Documents'), os.path.expanduser('~/Documents'), 'True,False'),

			# Backup preferences
			('createBackupFile','backup','bool',True, True, 'True,False'),
			('backupFileTime','Backup Passwords time','string','d','d','h,d,w,2w,m,2m,6m,y,off'),
			('backupLocation','The location of back-up','string',os.path.expanduser('~/Library/.pbu'), os.path.expanduser('~/Library/.pbu'), ''),
			('hashBackupFile','Hashing the Backup File', 'bool', True,True, 'True,False'),

			# Extrasecure 
			('hashUserFile', 'Hash User File Name', 'bool', False,False, 'True,False'),
			('createRandomFile','Creates random nonsense files', 'bool',False, False, 'True,False')
			])
		self.log('Preferences set')

		# Save master password
		# hashing time should be within 1 second --> group tested by using hashing urandom and salt as urandom for 100 times and taking the average as 0.65 seconds
		self.cursor.execute('''INSERT INTO password VALUES (0,'master',?)''', (
			# hashing
			hashlib.pbkdf2_hmac(
			# security level sha-512
			'sha512',
			# user inputted password-->binary values encoded in utf-32
			self.password.encode('utf-32'),
			# salt is generated by encrypting the user's password
			enc(self.password, self.password)[:-1].encode('utf-32'),
			# times
			750000).hex(),))

		self.log('Stored master password')

		# different shortcuts avaliable
		actions = ['get','new','changepassword','generate','quit','delete','changecommand','exportpwd','exportlog','import file','user preferences','backup now'] 
		
		# built in function for 'Help'
		defactions = ['??'] 

		# Enters default function--> Help
		self.cursor.execute('''INSERT INTO commands VALUES (?,?)''', ('help','??'))

		for items in actions: 
			# inputs user-defined passwords
			ucmd = requestforinput(items, defactions)
			defactions.append(ucmd)

			# saves user defined actions
			self.cursor.execute('''INSERT INTO commands VALUES(?,?)''', (items, ucmd)) 
			emptyline() if not self.verbose else None

		# Logs command input
		self.log('User commands inputted')

		# Saves file
		self.file.commit()

		# build backup file
		os.mkdir(os.path.join(os.path.expanduser('~/Library'),'.pbu','.'+ hashlib.pbkdf2_hmac('sha224', self.userName.encode('utf-32'), b'e302b662ae87d6facf8879dc1dabc573', 500000).hex()))

	def login(self):
		try:
			# Gets user actions and preferences
			self.buildActionsPreferences()
			# Compares hashes
			if self.cursor.execute('''SELECT password FROM password WHERE id = 0''').fetchone()[0] == hashlib.pbkdf2_hmac('sha512',self.password.encode('utf-32'),enc(self.password,self.password)[:-1].encode('utf-32'),750000).hex():
				self.log('Logged in') if bool(int(self.preferences.get('logLogin'))) else None
			else:
			 	self.log('Failed attempt') if bool(int(self.preferences.get('logLogin'))) else None
			 	raise WrongPassWordError

		# WrongPasswordError is raised if user entered a wrong password 
		except WrongPassWordError:
			raise

	def log(self, action):

		# Logs exact time and Action
		self.cursor.execute('''INSERT INTO log VALUES(?,?)''',(datetime.now().strftime("%Y-%m-%d %H:%M:%S:{}".format(str(datetime.now().microsecond)[:-3])),action))

		# saves file 
		self.file.commit()

	def get(self):

		# Ask for user input
		getValue = input(colors.lightblue('Please enter what do you want to get\n'))
		emptyline() if not self.verbose else None

		# Get all values -> Select * From Password
		if getValue == '*':
			self.log('Requested for all key, output printed')
			print('The list of your keys are:')

			# only print the key (search query) of all. Prevents data beach
			for k in [i[1] for i in self.cursor.execute('SELECT * FROM password').fetchall()[1:]]:
				print(colors.orange(k))

			waitForInput(colors)
			emptyline() if not self.verbose else None

			# save file
			self.file.commit()
			return self.get()

		if getValue == 'master':

			# user tries to get login password, returns fail 
			print(colors.red('Warning:'),colors.lightred('"Master"'),colors.blue('password is hashed and cannot be retrieved. Sorry!'))
			waitForInput(colors)

			# Logs user error
			self.log('Requested for master password, Error raised.')
			emptyline() if not self.verbose else None


		else:	
			# Else --> Get value from key
			# Fetchone reduces an extra tuple and increases running time

			getResult = self.cursor.execute('SELECT * FROM password WHERE key =(?)', (getValue,)).fetchone()
			# If key exists -->
			if getResult is not None:

				# Logs user have requeted for a valid result
				self.log('Searched for %s, valid output printed' % getValue)

				# Format to 20 px
				print(colors.cyan('{0:20}'.format(getResult[1])), '|', colors.lightgreen('{0:60}'.format(dec(getResult[2], self.password))))

				# Check if user preferences set to copy
				copy = self.preferences.get('copyAfterGet')

				# Copies outputted password
				if copy:

					# Pyperclip syntax to copy password
					pyperclip.copy(dec(getResult[2], self.password))

					# Tell the user password has been copied
					print(colors.lightgrey('Your password has been copied!'))
				waitForInput(colors)
				if not self.verbose:
					# Empty line to prevent data from keeping in Terminal Window. Prevents data breach
					emptyline() if copy else emptyline()

			# Search query not valid
			else:
				print(colors.lightred('This is not a valid value in your table! Please choose again!'))

				# logs invalid
				self.log('Searched for %s, invalid result' %getValue)
				waitForInput(colors)
				emptyline() if not self.verbose else None
				# Saves file as we are not gonna hit :saveFile line
				self.file.commit()

				# Goes back to beginning of :get
				self.get()

		# Saves log
		self.file.commit()

	def new(self):

		# Inserts new key into database
		currentKeys = [x[1] for x in self.cursor.execute('SELECT * FROM password').fetchall()]
		# Asks for key value
		newInputKey = input(colors.cyan('Please enter what do you want to enter:\n'))

		if newInputKey in currentKeys:
			self.log('Used value is re-inputted[new], no value is updated')
			print(colors.red('{} has been used! Please use a distinct key instead!'.format(newInputKey)))
			waitForInput(colors)
			emptyline() if not self.verbose else None
			return self.new()

		generateKeyword = list(self.actions.keys())[list(self.actions.values()).index('generate')]

		# Asks for new password

		print(colors.red('Please enter the new password:'),colors.green('\nYou can enter your generate keyword'), colors.yellow(generateKeyword), colors.green('to generate one.'))
		# Does not show
		newPassword = input()


		if newPassword == generateKeyword:

			# generates password
			newPassword = ''.join(random.choices(list(newd.keys()), k=19))

			# Copies password
			pyperclip.copy(newPassword)
			self.log('A new password is generated')
			print(colors.orange('This password has been copied'))

		emptyline() if not self.verbose else None

		# Gets current max index-> figures out the index value of this password
		currentIndex = max(int(x[0]) for x in self.cursor.execute('''SELECT * FROM password''').fetchall()) + 1

		# Error could be raised
		try:
			# Encrypts the password
			encryptedPassword = enc(newPassword, self.password)

			# Deletes password to prevent data breach
			del(newPassword)

			# Saves password into database with key and index
			self.cursor.execute('''INSERT INTO password VALUES(?,?,?)''', (currentIndex, newInputKey, encryptedPassword))

			# Logs the saved password
			self.log('Inserted new password %s' % newInputKey)

			# Deletes variables to prevent data breach
			del(encryptedPassword, newInputKey)
			print(colors.yellow('Success!'))
			waitForInput(colors)
			emptyline() if not self.verbose else None

		# EncryptionError is raised when the password inclueds some unencryptable characters
		except EncryptionError:

			# Deletes variable to prevent data breach
			del(newPassword, encryptedPassword)

			# Logs error value
			self.log('Password with invalid character inputted')

			print(colors.red('Please try again!'))
			waitForInput(colors)
			emptyline() if not self.verbose else None
			self.new()

		# Happens no matter what
		finally:

			# Saves file--> Log and password
			self.file.commit()

	def changePassword(self):

		# Requests for password--> Requests for authenication
		oldPassword = input(colors.yellow('Please enter your old password\n'))
		emptyline() if not self.verbose else None

		# Requests for new password --> Used to encrypt user data
		newEncPassword = input(colors.red('Please enter your new password\n'))
		emptyline() if not self.verbose else None

		# Check if the password is properly encryptable
		try:
			dontBreakMyProgram = enc(oldPassword, oldPassword)
			del(dontBreakMyProgram)
		except EncryptionError:
			print(colors.red('This is nto the right password! Please try again!'))
			waitForInput(colors)
			emptyline() if not self.verbose else None

			# Returns none if this key is not valid
			return None

		# Check if the new password is properly encryptable
		try:
			testIfValid = enc(newEncPassword, newEncPassword)
			del(testIfValid)
		except EncryptionError:
			print(colors.red('Please try again!'))
			waitForInput(colors)
			emptyline() if not self.verbose else None
			self.changePassword()

		# select all password db in current password database
		curPwds = [x for x in self.cursor.execute('SELECT * FROM password').fetchall() if x[0] != 0]

		emptyline() if not self.verbose else None

		# Checks if password hash matches saved hash
		if not hashlib.pbkdf2_hmac('sha512',oldPassword.encode('utf-32')
			,enc(oldPassword,oldPassword)[:-1].encode('utf-32'),750000).hex() == self.cursor.execute(
			'SELECT password FROM password WHERE id = 0').fetchone()[0]:
			print(colors.red('WrongPasswordError:'), colors.green('You entered the wrong password! Please try again!'))
			waitForInput(colors)
			return None

		# deletes all from database 
		self.cursor.execute('DELETE FROM password')

		# Inserts new passwords into database 
		newPwds = [(0, 'master', hashlib.pbkdf2_hmac('sha512', newEncPassword.encode('utf-32'), enc(newEncPassword, newEncPassword)[:-1].encode('utf-32'),750000).hex())]
		for currentPwds in curPwds:
			newPwds.append((currentPwds[0], currentPwds[1], enc(dec(currentPwds[2], self.password), newEncPassword)))
		self.cursor.executemany('INSERT INTO password VALUES(?,?,?)', newPwds)

		# Sets user password to the new password
		self.password = newEncPassword

		# Deletes the password in current scope
		del(newPassword)

	def backup(self):

		# Save after log 
		self.log('CreatedBackup')
		self.file.commit()

		print(colors.green('Backing up....'))

		# Generates backup db name
		now = time.time()
		fileTime = str(time.localtime(now).tm_year).zfill(4) + str(time.localtime(now).tm_yday).zfill(3) + str(time.localtime(now).tm_hour).zfill(2)

		# Determines the backup db name by preferences
		backupName = hashlib.pbkdf2_hmac('sha224', 
						self.userName.encode('utf-32'), b'e302b662ae87d6facf8879dc1dabc573', 
						500000).hex() if self.preferences.get('hashBackupFile') else self.userName

		# joins path to determine file location
		backupFile = os.path.join(self.preferences.get('backupLocation'),'.' + backupName,'.' +fileTime+'.db')

		# shutil.copy is willing to replace
		# Copies file to backup file
		shutil.copy2(
			# original file
			os.path.join(os.path.expanduser('~/.password'), '.' + self.userName + '.db'), 
			# backup location
			backupFile)

		# Logs backup
		self.log('Backup copied successfully')
		emptyline() if not self.verbose else None

	def checkBackup(self):
		print(colors.blue('Checking auto backup'))

		# logs checking backup
		self.log('Checking Backup')
		now = time.time()

		# time format relates to numbers
		timeD = {'h': 1,'d': 100,'w': 700,'2w': 1400,'m': 3000,'2m': 6000,'6m': 18000,'y' : 100000}

		# gets the user backup file name
		backupName = hashlib.pbkdf2_hmac('sha224', 
						self.userName.encode('utf-32'), 
						b'e302b662ae87d6facf8879dc1dabc573', 
						500000).hex() if self.preferences.get('hashBackupFile') else self.userName

		# get the time of the latest backup
		try:
			latestBackup = max([int(fName[1:-3]) for fName in [files for r, d,files in os.walk(os.path.join(self.preferences.get('backupLocation'),'.'+ backupName))][0]])
		except ValueError:
			self.backup() if user.preferences.get('createBackupFile') else None
			return None

		# Gets current time
		currentTime = int(str(time.localtime(now).tm_year).zfill(4) + str(time.localtime(now).tm_yday).zfill(3) + str(time.localtime(now).tm_hour).zfill(2))

		# Backs up if the difference is bigger than the time user needs to auto-backup
		if ((currentTime - latestBackup) >= timeD.get(self.preferences.get('backupFileTime'))):
			print(colors.cyan('Backup needed'))
			self.backup()
			print(colors.lightgreen('Backup finished'))
		else:
			self.log('No auto backup needed') 
			print(colors.cyan('No backup needed'))

		print(colors.lightblue('Auto-backup check finished'))
		time.sleep(random.random())
		self.log('Auto backup check finished')

	def changeCommand(self):
		def requestforinput(item, usedlist): 

			# Does not allow duplicates
			i = input(colors.lightcyan('Please enter the command you want for the action %s\n' % colors.green(item)))

			# return values if sequences has been entered before 
			if i in usedlist:

				print(colors.orange('%s has been used.' % i),colors.lightred('\nPlease use another one instead!'))
				print(colors.lightblue('Your current list is %s' % str(usedlist)))
				waitForInput(colors)
				emptyline() if not self.verbose else None
				# Recursive func if user repeatedly inputs used functions
				return requestforinput(item, usedlist) 
			# returns value if values have not been used before  
			return i

		# List of user actions possible
		userActions = [

		# Gets user password stored in database
		'get',

		# inputs new password
		'new',

		# Changes user password
		'changepassword',

		# generates a password of len(19)
		'generate',

		# quit program
		'quit',
		
		# Delete item from file
		'delete',
		
		# Change user commands
		'changecommand',
		
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

		
		self.cursor.execute('DELETE FROM commands')
		usedActions = []
		for items in userActions: 
			# inputs user-defined passwords
			userCommand = requestforinput(items, usedActions)
			usedActions.append(userCommand)

			# saves user defined actions
			self.cursor.execute('''INSERT INTO commands VALUES(?,?)''', (items, userCommand)) 
			emptyline() if not self.verbose else None
		listOfActions = []
		self.file.commit()

		# Commands have been changed, rebuild actions.
		self.buildActionsPreferences()

	def quit(self):
		# Raises quit -->Goes to global scope before quits
		raise normalQuit


	def delete(self):
		currentPwds = [x for x in range(1000)]
		# [x for x in self.cursor.execute('SELECT * FROM password').fetchall()]
		currentTerminalSize = shutil.get_terminal_size().lines - 10
		i = 0
		try:
			while i < len(currentPwds):
				print(len(currentPwds))
				for m in range(currentTerminalSize):
					print(currentPwds[i])
					i += 1
				waitForInput(colors)
				emptyline(currentTerminalSize + 4)
				print(i)
		except IndexError:
			pass




	# Prints user help, lists all actions
	def help(self):

		for userActions in self.actions.items():

			# Formatted user actions
			print(colors.cyan('{0:16}'.format(userActions[0])), colors.lightgreen('{0:16}'.format(userActions[1])))
		waitForInput(colors)

		# Clears listed line , prevents data breach 
		emptyline() if not self.verbose else None

	def exportPassword(self):
		# Gets export file type
		exportType = self.preferences.get('exportType')
		# Gets export location
		exportLocation = self.getExportLocation(bool(self.preferences.get('useDefaultLocation')))
		# Exports as different file
		currentFiles = self.cursor.execute('SELECT * FROM password').fetchall()
		if os.path.isfile(os.path.join(exportLocation, self.userName + '.' + exportType)):
			# Export already exists
			print(colors.yellow('You already have an exported file in %s! Please try again!') % exportLocation)
			self.log('Export location has repeated file, password not exported')
			waitForInput(colors)
			emptyline()
			return None
		self.file.commit()
		if exportType == 'db':
			# Database
			exportFile = sqlite3.connect(os.path.join(exportLocation ,self.userName + '.db'))
			# Creates export db file
			exportCursor = exportFile.cursor()
			exportFile.commit()
			exportCursor.execute('CREATE TABLE exportedPasswords (id char NOT NULL, key TEXT, password TEXT)')
			# Creates cursor and table
			self.log('Password Export Created')
			for entries in currentFiles:
				# Insert all entries into export database
				if entries[0] != 0:
					# Inserts values -- can be decryted
					exportCursor.execute('INSERT INTO exportedPasswords values (?,?,?)', entries) if bool(self.preferences.get('encryptExportDb')) else exportCursor.execute('INSERT INTO exportedPasswords values (?,?,?)', (entries[0], entries[1], decrypt(enctries[2], self.password)))
				else:
					# Inserts values -- hashed and cannot be decrypted
					exportCursor.execute('INSERT INTO exportedPasswords values (?,?,?)', entries)
			exportFile.commit()
			exportCursor.close()
			# Saves File and closes file

		else:
			with open(os.path.join(exportLocation, self.userName + '.' + exportType), 'w') as exportFile:
				self.log('Password Export Created')
				if exportType == 'txt':
					# Text file
					exportFile.write('{0:20} {1}'.format('Password key', 'Password'))
					# Creates header in txt file
					for entries in currentFiles:
						if currentFiles[0] != entries:
							# Write - can be decrypted
							exportFile.write('{0:20}:{1}\n'.format(entries[1], entries[2] if bool(self.preferences.get('encryptExportDb')) else decrypt(entries[2], self.password))) 
						
						else:
							# Write -Hashed
							exportFile.write('{0:20}:{1}\n'.format(entries[1], entries[2]))
				
				elif exportType == 'csv':
					# Cursor seperated files
					import csv
					# import the python in-built csv modle
					csvWriter = csv.writer(exportFile)

					# Creates header in csv files
					csvWriter.writerow(['Password key', 'Password'])
					# Use standardized csv writer because ',' could appear in encrypted passwords
					for entries in currentFiles:

						# Items saved
						if currentFiles[0] != entries:
							# Write - can be decrypted
							csvWriter.writerow([entries[1], entries[2] if bool(self.preferences.get('encryptExportDb')) else decrypt(entries[2], self.password)])

						else:
							# Write - hashed cannot be decrypted
							csvWriter.writerow([entries[1], entries[2]])

				elif exportType == 'json':
					# I first disliked this but its actually fine -- json files. 12/12/19
					import json
					# import the in-built json module

					encList = {}
					# Json file only takes 'dict' type entries

					for entries in currentFiles:

						# Enters into dictionary first
						if currentFiles[0] != entries:
							# updates dictionary -- can be decrypted
							encList.update({entries[1]: entries[2] if bool(self.preferences.get('encryptExportDb')) else decrypt(entries[2], self.password)})

						else:
							# updates dictionary -- cannot be decrypted
							encList.update({entries[1]: entries[2]})

					# Put into file
					json.dump(encList, exportFile)

		print(colors.red('DONE'))
		# Tells user action has been finished

		self.log('Export Password finished')
		print(colors.yellow('Export created'))
		waitForInput(colors)

		emptyline() if not self.verbose else None

	# Gets user Export Location //From preferences
	def getExportLocation(self, useDefaultLocation):
		exportLocation = ''
		if useDefaultLocation:
			exportLocation = self.preferences.get('defaultExportLocation')
		else:
			exportLocation = input(colors.red('Please enter your desired export location in command prompt syntax\n(e.g.: "~/Documents")\n>>>'))
		# Expands location if user uses command line prompt syntax

		exportLocation = os.path.expanduser(exportLocation)

		# Instances of error --> Not an actual location, Folder not accessible
		if not os.path.isdir(exportLocation):
			# Not an actual location
			print(colors.lightred('%s is not a valid export location, please try again!' % exportLocation))
			waitForInput(colors)
			return(getExportLocation(self, False))

		elif not os.access(exportLocation, os.W_OK):
			# Folder not accessible
			print(colors.red('%s is not accessable by this python module. \nPlease either use another location or run this application with sudo!'))
			waitForInput(colors)
			return(getExportLocation(self, False))
		else:	
			emptyline if not self.verbose else None
			return exportLocation

	def exportLog(self):
		exportType = self.preferences.get('exportType')

		# Current logs
		cLogs = self.cursor.execute('SELECT * FROM log').fetchall()

		# Gets users export location
		exportLocation = self.getExportLocation(bool(self.preferences.get('useDefaultLocation')))
		# get backup location

		if os.path.isfile(os.path.join(exportLocation, self.userName +'_LOGS'+ '.' + exportType)):
			# Export already exists
			print(colors.yellow('You already have an exported file in %s! Please try again!') % exportLocation)
			self.log('Export location has repeated file, password not exported')
			waitForInput(colors)
			emptyline()
			return None

		self.log('Asked for Log output request')

		if exportType == 'db':
			# Database
			exportFile = sqlite3.connect(os.path.join(exportLocation ,self.userName +'_LOGS'+ '.db'))
			self.log('Export Created')
			# Creates export db file
			exportCursor = exportFile.cursor()
			exportFile.commit()
			exportCursor.execute('CREATE TABLE logs (Timestamp TEXT NOT NULL, command TEXT)')
			# Creates cursor and table
			self.log('Logs exported')
			exportCursor.executemany('INSERT INTO logs VALUES(?,?)', cLogs)
			exportFile.commit()
			exportCursor.close()
			# Saves File and closes file
		else:
			with open(os.path.join(exportLocation, self.userName +'_LOGS'+ '.' + exportType), 'w') as exportFile:
				self.log('Password Export Created')
				if exportType == 'txt':
					# Text file
					exportFile.write('{0:30} {1}'.format('Timestamp', 'Action'))
					# Creates header in txt file
					for entries in cLogs:
						exportFile.write('{0:30}:{1}\n'.format(entries[0], entries[1]))
				
				elif exportType == 'csv':
					# Cursor seperated files
					import csv
					# import the python in-built csv modle
					csvWriter = csv.writer(exportFile)

					# Creates header in csv files
					csvWriter.writerow(['Timestamp', 'Action'])

					# Use standardized csv writer because ',' could appear in encrypted passwords
					for entries in cLogs:
						csvWriter.writerow([entries[0], entries[1]])

				elif exportType == 'json':
					# I first disliked this but its actually fine -- json files. 12/12/19
					import json
					# import the in-built json module

					outputList = {}
					# Json file only takes 'dict' type entries

					for entries in cLogs:
						outputList.update({entries[0]: entries[1]})

					# Put into file
					json.dump(outputList, exportFile)

		print(colors.red('DONE'))
		# Tells user action has been finished

		self.log('Export Logs finished')
		print(colors.yellow('Export finished'))
		waitForInput(colors)

		emptyline() if not self.verbose else None

	def importFile(self):
		# import files from backups 

		# backup location
		backupName = hashlib.pbkdf2_hmac('sha224', 
						self.userName.encode('utf-32'), b'e302b662ae87d6facf8879dc1dabc573', 
						500000).hex() if self.preferences.get('hashBackupFile') else self.userName
		try:
			# Could possibly return an error if no backup files could be found
			latestBackupFile = max([int(x[-12:-3]) for x in [f for d, b, f in os.walk(os.path.expanduser('~/Library/.pbu/.'+ backupName))][0]])
		except ValueError:
			print(colors.red('Error:'), colors.orange('The backup folder has no backups avaliable! We are sorry but we cannot extract your file!'))	
			return None
		# print(latestBackupFile)
		# change string into a datetime stamp
		t = str(datetime.strptime(str(latestBackupFile), '%Y%j%H'))
		print(colors.green('Your latest backup is on {day} {around} {time}'.format(day=colors.purple(t.split()[0]), around=colors.green('around'),time=colors.purple(t.split()[1][:5]))))
		# ask if the user actually wants to backup
		print(colors.pink('Do you want to restore from the copy?[yn]\nThis will quit the program'))
		yn = readchar.readchar()
		self.log('restored from backup')
		if yn == 'y':
			# Copies the file and would replace current file
			shutil.copy2(
				os.path.join(os.path.expanduser('~/Library/.pbu/.' + backupName), '.'+str(latestBackupFile) + '.db'),
				# original file
				os.path.join(os.path.expanduser('~/.password'), '.' + self.userName + '.db'))
			waitForInput(colors)
			emptyline() if not self.verbose else None
			raise instantQuit
		else:
			# File will not be imported
			print(colors.lightblue('File not imported'))
			self.log('File is not imported')
			waitForInput(colors)
			emptyline() if not self.verbose else None


