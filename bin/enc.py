# Matthew Lam
# module designed to import to [[encrypt]] and [[decrypt]]
import random, hashlib
class EncryptionError(Exception):
	pass

newd = {
	' ' : 0,
	'a' : 1,
	'b' : 2,
	'c' : 3,
	'd' : 4,
	'e' : 5,
	'f' : 6,
	'g' : 7,
	'h' : 8,
	'i' : 9,
	'j' : 10,
	'k' : 11,
	'l' : 12,
	'm' : 13,
	'n' : 14,
	'o' : 15,
	'p' : 16,
	'q' : 17,
	'r' : 18,
	's' : 19,
	't' : 20,
	'u' : 21,
	'v' : 22,
	'w' : 23,
	'x' : 24,
	'y' : 25,
	'z' : 26,
	'A' : 27,
	'B' : 28,
	'C' : 29,
	'D' : 30,
	'E' : 31,
	'F' : 32,
	'G' : 33,
	'H' : 34,
	'I' : 35,
	'J' : 36,
	'K' : 37,
	'L' : 38,
	'M' : 39,
	'N' : 40,
	'O' : 41,
	'P' : 42,
	'Q' : 43,
	'R' : 44,
	'S' : 45,
	'T' : 46,
	'U' : 47,
	'V' : 48,
	'W' : 49,
	'X' : 50,
	'Y' : 51,
	'Z' : 52,
	',' : 53,
	'<' : 54,
	'.' : 55,
	'>' : 56,
	'/' : 57,
	'?' : 58,
	';' : 59,
	':' : 60,
	'[' : 61,
	'{' : 62,
	']' : 63,
	'}' : 64,
	'|' : 65,
	'`' : 66,
	'~' : 67,
	'1' : 68,
	'!' : 69,
	'2' : 70,
	'@' : 71,
	'3' : 72,
	'#' : 73,
	'4' : 74,
	'$' : 75,
	'5' : 76,
	'%' : 77,
	'6' : 78,
	'^' : 79,
	'7' : 80,
	'&' : 81,
	'8' : 82,
	'*' : 83,
	'9' : 84,
	'(' : 85,
	'0' : 86,
	'-' : 87,
	'_' : 88,
	'=' : 89,
	'+' : 90,
	'å' : 91,
	'∫' : 92,
	'∂' : 93,
	'©' : 94,
	'†' : 95,
	'π' : 96,
	'œ' : 97,
	'…' : 98,
	')' : 99,}

newdec ={v: k for k, v in newd.items()}

encd = {
	' ' : 0,
	'a' : 1,
	'b' : 2,
	'c' : 3,
	'd' : 4,
	'e' : 5,
	'f' : 6,
	'g' : 7,
	'h' : 8,
	'i' : 9,
	'j' : 10,
	'k' : 11,
	'l' : 12,
	'm' : 13,
	'n' : 14,
	'o' : 15,
	'p' : 16,
	'q' : 17,
	'r' : 18,
	's' : 19,
	't' : 20,
	'u' : 21,
	'v' : 22,
	'w' : 23,
	'x' : 24,
	'y' : 25,
	'z' : 26,
	'A' : 27,
	'B' : 28,
	'C' : 29,
	'D' : 30,
	'E' : 31,
	'F' : 32,
	'G' : 33,
	'H' : 34,
	'I' : 35,
	'J' : 36,
	'K' : 37,
	'L' : 38,
	'M' : 39,
	'N' : 40,
	'O' : 41,
	'P' : 42,
	'Q' : 43,
	'R' : 44,
	'S' : 45,
	'T' : 46,
	'U' : 47,
	'V' : 48,
	'W' : 49,
	'X' : 50,
	'Y' : 51,
	'Z' : 52,
	',' : 53,
	'<' : 54,
	'.' : 55,
	'>' : 56,
	'/' : 57,
	'?' : 58,
	';' : 59,
	':' : 60,
	'[' : 61,
	'{' : 62,
	']' : 63,
	'}' : 64,
	'|' : 65,
	'`' : 66,
	'~' : 67,
	'1' : 68,
	'!' : 69,
	'2' : 70,
	'@' : 71,
	'3' : 72,
	'#' : 73,
	'4' : 74,
	'$' : 75,
	'5' : 76,
	'%' : 77,
	'6' : 78,
	'^' : 79,
	'7' : 80,
	'&' : 81,
	'8' : 82,
	'*' : 83,
	'9' : 84,
	'(' : 85,
	'0' : 86,
	'-' : 87,
	'_' : 88,
	'=' : 89,
	'+' : 90,
	'å' : 91,
	'∫' : 92,
	'∂' : 93,
	'©' : 94,
	'†' : 95,
	'π' : 96,
	'œ' : 97,
	'…' : 98,
	')' : 99,
	'∞' : 100,
	'∏' : 101,
	'Í' : 102,
	'◊' : 103,
	'¬' : 104,
	'€' : 105,
	'¿' : 106,
	'Â' : 107,
	'º' : 108,
	'÷' : 109,
	'«' : 110,
	'Æ' : 111,
	'°' : 112,
	'‹' : 113,
	'ø' : 114,
	'ˇ' : 115,
	'‡' : 116,
	'·' : 117,
	'»' : 118,
	'Ú' : 119,
	'√' : 120,
	'∆' : 121,
	'ı' : 122,
	'Ç' : 123,
	'Î' : 124,
	'Ô' : 125,
	'Œ' : 126,
	'ﬂ' : 127,
	'§' : 128}

decd = {v: k for k, v in encd.items()}

def encsp(string, password):
	inv = {'0': '1', '1': '0'}
	keyd = {
	0: 0,
	1:(0,1),
	2:(0,2),
	3:(0,3),
	4:(0,4),
	5:(0,5),
	6:(0,6),
	7:(1,2),
	8:(1,3),
	9:(1,4),
	10:(1,5),
	11:(1,6),
	12:(2,3),
	13:(2,4),
	14:(2,5),
	15:(2,6),
	16:(3,4),
	17:(3,5),
	18:(3,6),
	19:(4,5),
	20:(4,6),
	21:(5,6),
	22:1,
	23:2,
	24:3,
	25:4,
	26:5,
	27:6}
	key = (len(str(password))*len(str(string)) % 28)
	spbin = ["{0:b}".format(int(encd.get(chars))).zfill(7) for chars in string]
	ilist = []
	for items in spbin:
		spstr = ''
		for count, bins in enumerate(items):
			spstr = spstr + (bins if str(count) in str(keyd.get(key)) else inv.get(str(bins)))
		ilist.append(spstr)
	return ''.join([decd.get(int(str(i), 2)) for i in ilist])

def encrypt(encs, pwd):
	encs = str(encs)
	pwd = str(hashlib.pbkdf2_hmac('sha512', str(pwd).encode('utf-32'), ''.join(sorted(pwd)).encode('utf-32'), 300000).hex()) + str(hashlib.pbkdf2_hmac('sha512', str(pwd).encode('utf-32'), ''.join(sorted(pwd, reverse=True)).encode('utf-32'), 300000).hex())
	def strtoint(stringinput):
		integers = ''
		stringinput = str(stringinput)
		try:
			for chars in str(stringinput):
				if chars not in encd:
					raise EncryptionError
				integers += str(encd.get(str(chars))).zfill(3)
			if encd.get(stringinput[-1]) < 10:
				integers = integers[:-2] + integers[-1:]
			return integers
		except EncryptionError:
			print("\033[91m{}\033[00m" .format('EncryptionError:'), 'Character %s is not encryptable' % chars)
			raise
	def inttostr(intinput):
		l = [str(intinput)[i:i+2] for i in range(0, len(str(intinput)), 2)]
		c = ''
		for chars in l:
			# print(chars)
			c += newdec.get(int(chars))
		return c
	encs = str(encs)
	eintfinal = int(strtoint(str(encs))) * int(strtoint(str(pwd)))
	lenth = str(len(strtoint(encs))).zfill(4)
	estr = inttostr(eintfinal)
	sped = encsp(estr, pwd)
	final = sped + lenth + random.choice(list(encd.keys()))
	return final

def decrypt(decs, pwd):
	def decstrtoint(stringinput):
		integers = ''
		stringinput = str(stringinput)
		try:
			for chars in str(stringinput):
				if chars not in newd:
					raise EncryptionError
				integers += str(newd.get(chars)).zfill(2)
			if encd.get(stringinput[-1]) < 10:
				integers = integers[:-2] + integers[-1:]
			return integers
		except EncryptionError:
			print("\033[91m{}\033[00m" .format('EncryptionError:'), 'Character %s is not encryptable' % chars)
			quit()
	def strtoint(stringinput):
		stringinput = str(stringinput)
		integers = ''
		try:
			for chars in stringinput:
				if chars not in encd:
					raise EncryptionError
				integers += str(encd.get(chars)).zfill(3)
			if encd.get(stringinput[-1]) < 10:
				integers = integers[:-2] + integers[-1:]
			return integers
		except EncryptionError:
			print("\033[91m{}\033[00m" .format('EncryptionError:'), 'Character %s is not encryptable' % chars)
			quit()
	def decinttostr(intinput):
		l = [str(intinput)[i:i+3] for i in range(0, len(str(intinput)), 3)]
		c = ''
		for chars in l:
			c += decd.get(int(chars))
		return c
	pwd = str(hashlib.pbkdf2_hmac('sha512', str(pwd).encode('utf-32'), ''.join(sorted(pwd)).encode('utf-32'), 300000).hex()) + str(hashlib.pbkdf2_hmac('sha512', str(pwd).encode('utf-32'), ''.join(sorted(pwd, reverse=True)).encode('utf-32'), 300000).hex())
	orglen = int(decs[-5: -1])
	decs = decs[:-5]
	dintfinal = encsp(decs, pwd)
	df = int(decstrtoint(dintfinal))
	dfinal = df // int(strtoint(pwd))
	dfl = str(dfinal).zfill(int(orglen))
	return decinttostr(dfl)