import sys, os, random, string, shutil, sqlite3, json
from .enc import encsp as encsp
from .randomnames import name as namelist
try:
	import readchar
except ModuleNotFoundError: 
	# System call to install modules
	os.system('python3 -m pip install readchar')

#Wrong password error 
class WrongPassWordError(Exception): 
	pass

# User quits via a normal method(Keyboard interrupt, raise quit)
class normalQuit(Exception):
	pass

def buildColors(trueOrFalse):

	# colors filled with actual colors
	class colorsClassTrue: 
		def black(c): 		return str('\033[30m{}\033[0m'.format(c))
		def blue(c): 		return str('\033[34m{}\033[0m'.format(c))
		def cyan(c): 		return str('\033[36m{}\033[0m'.format(c))
		def darkgrey(c): 	return str('\033[90m{}\033[0m'.format(c))
		def green(c):		return str('\033[32m{}\033[0m'.format(c))
		def lightblue(c):	return str('\033[94m{}\033[0m'.format(c))
		def lightcyan(c): 	return str('\033[96m{}\033[0m'.format(c))
		def lightgreen(c): 	return str('\033[92m{}\033[0m'.format(c))
		def lightgrey(c): 	return str('\033[37m{}\033[0m'.format(c))
		def lightred(c):	return str('\033[91m{}\033[0m'.format(c))
		def pink(c):		return str('\033[95m{}\033[0m'.format(c))
		def purple(c): 		return str('\033[35m{}\033[0m'.format(c))
		def red(c): 		return str('\033[31m{}\033[0m'.format(c))
		def orange(c): 		return str('\033[33m{}\033[0m'.format(c))
		def yellow(c):		return str('\033[93m{}\033[0m'.format(c))

	# transparent
	class colorsclassFalse:
		def black(c): 		return c
		def blue(c): 		return c
		def cyan(c): 		return c
		def darkgrey(c): 	return c
		def green(c): 		return c
		def lightblue(c): 	return c
		def lightcyan(c): 	return c
		def lightgreen(c): 	return c
		def lightgrey(c): 	return c
		def lightred(c): 	return c
		def pink(c):		return c
		def purple(c): 		return c
		def red(c): 		return c
		def orange(c): 		return c
		def yellow(c): 		return c

	# Assigns class call to variable
	return colorsClassTrue if trueOrFalse else colorsclassFalse

#Empty multiple lines
def emptyline(lines=100): 
	for i in range(lines):
		# move up one line and clear whole line
		sys.stdout.write("\033[F") 
		sys.stdout.write("\033[K") 

def waitForInput(colors):
	print(colors.green('Press any key to continue...'))
	readchar.readchar()
	return ''

def randomPwd():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(15))

def createRandomFile(num, printall, color):
	# re-import string -- I don't know why it works but it does. 
	# Please don't delete or it will fail miserably
	import string 

	# Function to output logs
	def logifvb(pval, p=printall, clr=color):
		print(color(pval)) if p else None

	# List of random names
	names = namelist
	for count in range(num):
		logifvb(count)

		# Generates a name to use in a file
		name=''.join(random.choices([' '.join(random.choices(names,k=random.randrange(1,4))), random.choices(string.hexdigits, k=56)], weights=[1,3])[0]).lower()
		logifvb('Name chosen')

		# create user database file and create cursor object
		file = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.password','.'+name+'.db'))
		logifvb('File Created')
		cursor = file.cursor()
		logifvb('Cursor Created')

		# Create tables
		cursor.execute('''CREATE TABLE password(id INT, key TEXT, password TEXT)''')
		cursor.execute('''CREATE TABLE commands(globalcmd TEXT, usrcmd TEXT)''')
		cursor.execute('''CREATE TABLE log(logtime TEXT, log TEXT)''')
		cursor.execute('''CREATE TABLE userPreferences(sysdefname TEXT,description TEXT, type TEXT, Value TEXT, 'Default' TEXT, possible TEXT)''')
		logifvb('Table created')

		# Insert a random password that looks like a hash
		cursor.execute('''INSERT INTO password VALUES(0, 'master',?)''', (''.join(random.choices(string.hexdigits, k=256)),))
		logifvb('master password entered')

		# Creates random 'password' file
		passwords= []
		for index in range(1, random.randrange(10,40)):
			name 	= encsp(''.join(random.choices(string.ascii_letters, k=random.randrange(5,15))),'.'*random.randrange(1,28))
			pwd 	= encsp(''.join(random.choices(string.ascii_letters, k=random.randrange(25,145))),'.'*random.randrange(1,28))
			passwords.append((index, name, pwd))
			logifvb(name)
			logifvb(pwd)
		cursor.executemany('''INSERT INTO password VALUES(?,?,?)''', passwords)
		logifvb('Random passwords entered')

		# Creates random user actions
		actionsls = ['help','get','new','changepassword','generate','quit','delete','changecommand','exportpwd','exportlog',
		'import file','user preferences','backup now']
		actions = []
		for ats in actionsls:
			act = encsp(''.join(random.choices(string.ascii_letters, k=random.randrange(2,8))), '.'.join(random.choices('.'*random.randrange(1,28))))
			actions.append((ats, act))
			logifvb(act)
		cursor.executemany('''INSERT INTO commands VALUES(?,?)''',actions)
		logifvb('actions entered')

		# Create random log files
		lgs = []
		pwdl = '.'*random.randint(1,27)
		for p in range(random.randint(25,150)):
			time = str(random.randint(2018,2021))+str(random.randint(1,12))+str(random.randint(1,31))+str(random.randint(1,24))+str(
				random.randint(1,60))+str(random.randint(1,60))+str(random.randint(1,1000))
			string1 = encsp(random.choices(string.ascii_letters,k=random.randrange(8,31)), pwdl)
			time = encsp(time,pwdl)
			lgs.append((time,string1))
		cursor.executemany('''INSERT INTO log VALUES(?,?)''',lgs)

		# create random preference files
		cursor.executemany(
		'''INSERT INTO userPreferences VALUES(?,?,?,?,?,?)''', 
		# list of preferences avaliable
		[

		# System preferences in UI
		('verbose','Shows everything', 'bool', random.choice([True, False]), False, 'True,False'), 
		('copyAfterGet','Copy password after output', 'bool',random.choice([True, False]), True, 'True,False'),
		('askToQuit','Ask before quit','bool',random.choice([True,False]), False, 'True,False'),
		('customColor','Use custom color', 'bool',random.choice([True,False]), True, 'True,False'),
		('logLogin','Record Logins','bool',random.choice([True,False]),True, 'True,False'),

		# Exports preferences
		('encExpDb','Export files are encrypted','bool',random.choice([True,False]), True, 'True,False'),
		('useDefLoc','Use default export location','bool',random.choice([True,False]), True, 'True,False'),
		('exportType','Export type','str in list','db',random.choice(['csv','db','json','txt']), 'csv,db,json,txt'),
		('defExpLoc','Default export location', 'location','~/Documents','~/Documents', 'Any folder'),

		# Backup preferences
		('createBcF','backup','bool',random.choice([True, False]), True, 'True,False'),
		('backupFileTime','Backup Passwords time','location','d','d','h,d,w,2w,m,2m,6m,y,off'),
		('backupLocation','The location of back-up','location','~/Library/.pbu', '~/Library/.pbu','Any folder'),
		('hashBackupFile','Hashing the Backup File', 'bool', random.choice([True,False]),True, 'True,False'),

		# Extrasecure 
		('hashUserFile', 'Hash User File Name', 'bool', False,False, 'True,False'),
		('createRandF','Creates random nonsense files', 'bool',False, False, 'True,False')
		])

		# Save and close file
		logifvb('Saving file\nDeleting cursor file\nClosing file')
		file.commit()
		cursor.close()
		file.close()
		logifvb('Returning to user interface')
	return None