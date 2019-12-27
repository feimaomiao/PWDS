# Matthew Lam
# module designed to import to [[encrypt]] and [[decrypt]]
import random, hashlib

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
	'"' : 97,
	'\'' : 98,
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
	'"' : 97,
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
	'\'' : 122,
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
	key = ((len(str(password))+len(str(string))) % 28)
	spbin = ["{0:b}".format(int(encd.get(chars))).zfill(7) for chars in string]
	ilist = []
	for items in spbin:
		spstr = ''
		for count, bins in enumerate(items):
			spstr = spstr + (bins if str(count) in str(keyd.get(key)) else inv.get(str(bins)))
		ilist.append(spstr)
	return ''.join([decd.get(int(str(i), 2)) for i in ilist])

def encrypt(encs, pwd):
	encs = ''.join(str(ord(chars)).zfill(7) for chars in str(encs))
	front0s = [encs.index(i) for i in encs if i != '0'][0]
	ending0s = len(encs) - len(encs.rstrip('0'))
	npwd = ''.join(str(ord(l)) for l in str(hashlib.pbkdf2_hmac(
		'sha512', str(pwd).encode('utf-32'), ''.join(sorted(pwd, reverse=True)).encode('utf-32'), 300000).hex()))
	intencd = str(int(encs) * int(npwd))
	cy = ''.join(random.choices([m for m in newdec.values()], k=4)) + str(front0s).zfill(2) + str(ending0s).zfill(2)
	for p in [int(intencd[i:i+2]) for i in range(0, len(intencd), 2)]:
		cy += newdec.get(p)
	return encsp(cy, pwd)

def decrypt(decs, pwd):
	decs = encsp(decs, pwd)
	zeros = decs[4:8]
	product = ''.join([str(newd.get(i)).zfill(2) for i in decs[8:]])
	npwd = ''.join(str(ord(l)) for l in str(hashlib.pbkdf2_hmac(
		'sha512', str(pwd).encode('utf-32'), ''.join(sorted(pwd, reverse=True)).encode('utf-32'), 300000).hex()))
	divided = str(int(product) // int(npwd))
	subzeroed = ('0' * int(zeros[:2]) if int(zeros[:2]) > 0 else '') + divided + ('0' * int(zeros[2:]) if int(zeros[2:])> 0 else '')
	subzlist = [int(subzeroed[i:i+7]) for i in range(0,len(subzeroed), 7)]
	if subzlist[-1] <10 and subzlist[-1]>0:
		subzlist[-2] += 1
		subzlist.pop(-1)
	elif subzlist[-1] == 0:
		subzlist.pop(-1)
	return ''.join([chr(k) for k in subzlist])


















