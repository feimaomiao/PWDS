import sys, os, random, string
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