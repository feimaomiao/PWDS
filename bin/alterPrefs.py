from funcs import *
class preference():
	def __init__(self, preference, userclass, currentPrefs):
		self.user = userclass
		self.changedPreference = preference
		global colors
		colors = buildColors(self.user.preference.get('customColor'))
		self.currentPrefs = currentPrefs

	def changePreference(self):
		typeDict = {'bool': lambda: self.changeBool(), 'str in list': lambda: self.strInList, 'str': lambda: self.changeString}
		self.type = self.changePreference[3]
		return typeDict.get(self.type)()

	def changeBool(self):	
		def trueorfalse(string):
			# defines user input to be true or false (used in changing preferences)
			if string.lower() in ['true','1','t']:
				# avaliable 'true' formats
				return True
			elif string.lower() in ['false','0','f']:
				# avaliable 'false formats'
				return False
			elif 'default' in string.lower() or 'def' in string.lower():
				return 'default'
			else:
				# Neither
				print(colors.red(f'Sorry but {string} is not in our approved list of true/false strings'))
				print(colors.cyan('True: [\'true\', \'1\',\'t\']\nFalse: [\'false\', \'0\', \'f\']'))
				waitForInput(colors)
			
