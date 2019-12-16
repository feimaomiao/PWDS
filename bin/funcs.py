import sys, os
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

class instantQuit(Exception):
	pass

def buildColors(trueOrFalse):

	# colors filled with actual colors
	class colorsClassTrue: 
		def black(c): 		return'\033[30m{}\033[0m'.format(c)  
		def blue(c): 		return'\033[34m{}\033[0m'.format(c)
		def cyan(c): 		return'\033[36m{}\033[0m'.format(c)
		def darkgrey(c): 	return'\033[90m{}\033[0m'.format(c)
		def green(c):		return'\033[32m{}\033[0m'.format(c)
		def lightblue(c):	return'\033[94m{}\033[0m'.format(c)
		def lightcyan(c): 	return'\033[96m{}\033[0m'.format(c)
		def lightgreen(c): 	return'\033[92m{}\033[0m'.format(c)
		def lightgrey(c): 	return'\033[37m{}\033[0m'.format(c)
		def lightred(c):	return'\033[91m{}\033[0m'.format(c)
		def pink(c):		return'\033[95m{}\033[0m'.format(c)
		def purple(c): 		return'\033[35m{}\033[0m'.format(c)
		def red(c): 		return'\033[31m{}\033[0m'.format(c) 
		def orange(c): 		return'\033[33m{}\033[0m'.format(c)
		def yellow(c):		return'\033[93m{}\033[0m'.format(c)

	# transparent
	class colorsclassFalse:
		def black(c): 		return '{}\033[0m'.format(c)
		def blue(c): 		return '{}\033[0m'.format(c)
		def cyan(c): 		return '{}\033[0m'.format(c)
		def darkgrey(c): 	return '{}\033[0m'.format(c)
		def green(c): 		return '{}\033[0m'.format(c)
		def lightblue(c): 	return '{}\033[0m'.format(c)
		def lightcyan(c): 	return '{}\033[0m'.format(c)
		def lightgreen(c): 	return '{}\033[0m'.format(c)
		def lightgrey(c): 	return '{}\033[0m'.format(c)
		def lightred(c): 	return '{}\033[0m'.format(c)
		def pink(c):		return '{}\033[0m'.format(c)
		def purple(c): 		return '{}\033[0m'.format(c)
		def red(c): 		return '{}\033[0m'.format(c)
		def orange(c): 		return '{}\033[0m'.format(c)
		def yellow(c): 		return '{}\033[0m'.format(c)

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