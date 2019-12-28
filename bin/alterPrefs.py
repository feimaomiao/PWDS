from funcs import *
class usrp():
	def __init__(self, pref, index):
		self.index = index
		self.key, self.description, self.valueType, self.value, self.default, self.avaliable,  = pref

	def __repr__(self):
		return(str(self.description))

def validRequest(vartype):
	aval = []
	if vartype == 'bool':
		boolvals = {True:['true','t','yes','y'], False:['false','f','no','n']}
		aval = boolvals[True] + boolvals[False]
		if usrinput not in aval:
			print('This is not a valid input...')
			waitforinput(buildColors(False))
			return(False, None)




# userPreferences = [alterPrefs.usrp(x, count) for count, x in enumerate(
# 	[row for row in self.cursor.execute('SELECT * FROM userPreferences').fetchall()], start=1)]

# self.cursor.executemany(
# '''INSERT INTO userPreferences VALUES(?,?,?,?,?,?)''', 
# # list of preferences avaliable
# [

# # System preferences in UI
# ('verbose','Shows everything', 'bool', False, False, 'True,False'), 
# ('copyAfterGet','Copy password after output', 'bool',True, True, 'True,False'),
# ('askToQuit','Ask before quit','bool',False, False, 'True,False'),
# ('customColor','Use custom color', 'bool',True, True, 'True,False'),
# ('logLogin','Record Logins','bool',True,True, 'True,False'),

# # Exports preferences
# ('encExpDb','Export files are encrypted','bool',True, True, 'True,False'),
# ('useDefaultLocation','Use default export location','bool',True, True, 'True,False'),
# ('exportType','Export type','str in list','db','db ', 'csv,db,json,txt'),
# ('defExpLoc','Default export location', 'string',os.path.expanduser('~/Documents'),
#  os.path.expanduser('~/Documents'), 'True,False'),

# # Backup preferences
# ('createBackupFile','backup','bool',True, True, 'True,False'),
# ('backupFileTime','Backup Passwords time','string','d','d','h,d,w,2w,m,2m,6m,y,off'),
# ('backupLocation','The location of back-up','string',os.path.expanduser('~/Library/.pbu'), os.path.expanduser('~/Library/.pbu'), ''),
# ('hashBackupFile','Hashing the Backup File', 'bool', True,True, 'True,False'),

# # Extrasecure 
# ('hashUserFile', 'Hash User File Name', 'bool', False,False, 'True,False'),
# ('createRandomFile','Creates random nonsense files', 'bool',False, False, 'True,False')
# ])
class preferences():
	def __init__(self, listOfPref):

		for p in listOfPref:

		self.verbose = [p for p in listOfPref if p.key == 'verbose'][0]
		self.copyAfterGet = [p for p in listOfPref if p.key == 'copyAfterGet'][0]
		self.askToQuit = [p for p in listOfPref if p.key == 'askToQuit'][0]
		self.customColor = [p for p in listOfPref if p.key == 'customColor'][0]
		self.logLogin = None
		self.encExpDb = None
		self.useDefaultLocation = None
		self.exportType = None
		self.defExpLoc = None
		self.createBackupFile = None
		self.backupFileTime = None
		self.backupLocation = None
		self.hashBackupFile = None
		self.hashUserFile = None
		self.createRandomFile = None






























