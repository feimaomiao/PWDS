from funcs import *
import shutil, os
class usrp():
	def __init__(self, pref, index):
		self.index = index
		self.key, self.description, self.valueType, self.value, self.default, self.avaliable,  = pref
		self.value = bool(int(self.value)) if self.valueType == 'bool' else self.value
		self.default = bool(int(self.default)) if self.valueType == 'bool' else self.default

	def __repr__(self):
		return(str(self.key))

class preferences():
	def __init__(self, listOfPref):
		self.preferenceDicts = {}
		self.lisfofPref = listOfPref

	def reqBool(self,colors):
		usrinput = input(colors.green('Type=Bool\nPossible = ["t","true","y","yes","f","false","n","no","d", "def","default"]\nPlease enter your choice\n')).lower()
		possible = {'t':True,'true':True,'y':True,'yes':True,'f':False,'false':False,'n':False,'no':False,'def':'def','default':'def','d':'def'}
		if usrinput not in possible.keys():
			self.clear()
			print(colors.red('This is not a valid result!Please enter again!')) 
			return self.reqBool(colors)
		return possible.get(usrinput)

	def reqStrIL(inpLIst, colors):
		usrinput = input(colors.green(f'Type=String in list\nPossible={inpLIst}\nPlease enter your choice\n'))
		if usrinput not in inpLIst:
			self.clear()
			print(colors.red('This is not a valid result!\nPlease enter again!'))
			return self.reqStrIL(inpLIst, colors)
		return usrinput

	def reqLoc(self,colors):
		usrinput = input(colors.green(f'Type=Location\nPossible=All\nPlease enter a location with unix-like file("~/Path/to/destination")\n'))
		if not os.access(os.path.expanduser(usrinput), os.W_OK) or not os.path.isdir(os.path.expanduser(usrinput)):
			self.clear()
			print(colors.red('This is not a valid path!\nPlease try again!'))
			return self.reqLoc(colors)
		return usrinput

	def clear(self):
		emptyline() if not bool(self.preferenceDicts.get('verbose')) else None
		return None

	def buildPrefs(self):
		for items in self.lisfofPref:
			key = items.key
			value = items
			self.preferenceDicts[key] = value
		return None

	def printCurrentPrefs(self):
		colors = buildColors(bool(self.preferenceDicts.get('customColor').value))
		print(colors.green('Your current preferences are as below:'))
		print('{index:14}||{key:23}||{description:39}||{valueType:20}||{value:30}||{defaultValue:25}||{aval:29}'.format(
			index=colors.orange('Index'), key=colors.blue('key'), description=colors.green('description'),valueType=colors.pink('value type'),
			value=colors.lightgrey('Value'),defaultValue=colors.cyan('Default'),aval=colors.yellow('avaliable')))
		print(colors.purple('-'*shutil.get_terminal_size().columns))
		vertL = colors.purple('||')
		for key, value in self.preferenceDicts.items():
			print(f'{colors.orange(value.index):14}{vertL}{colors.blue(value.key):23}{vertL}{colors.green(value.description):39}{vertL}{colors.pink(value.valueType):20}{vertL}{colors.lightgrey(value.value):30}{vertL}{colors.cyan(value.default):25}{vertL}{colors.yellow(value.avaliable):29}')
		print(colors.purple('-'*os.get_terminal_size().columns))			
		return None

	def changePrefs(self):
		colors = buildColors(bool(self.preferenceDicts.get('customColor').value))
		changeIndex = 1
		while changeIndex != '':
			self.printCurrentPrefs()
			changeIndex = input(colors.yellow('Please enter the index of the prefernce you want to change:'))
			if not changeIndex.isdigit() or not (int(changeIndex) <= len(self.preferenceDicts) and  int(changeIndex) > 0):
				print(colors.red('ValueError:'), colors.yellow('This is not a valid input!'))
				break
			elif len(changeIndex) == 0:
				break
			changeItem = [i for k,i in self.preferenceDicts.items() if i.index == int(changeIndex)][0]
			outputVal = bool(changeItem.value) if changeItem.valueType == 'bool' else str(changeItem.value)
			print(colors.blue(f'You are going to change {changeItem.key}.\nThe current value is {outputVal}.\nDefault value is {changeItem.index}'))
			if changeItem.valueType == 'bool':
				newvalue = self.reqBool(colors)
				if newvalue == 'def':
					changeItem.value = changeItem.default
				else:
					changeItem.value = bool(newvalue)
			elif changeItem.valueType == 'str in list':
				newvalue = self.reqStrIL(changeItem.avaliable.split(',')+['def'], colors)
				changeItem.value = changeItem.default if newvalue == 'def' else newvalue
			else:
				newvalue = self.reqLoc(colors)
				changeItem.value = newvalue
			emptyline()
		waitForInput(colors)
		return None

	def returnList(self):
		print(self.preferenceDicts)
		return [vals for k, vals in self.preferenceDicts.items()]
