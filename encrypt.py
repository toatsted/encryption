import os
import sys

import tkinter
from tkinter.filedialog import askopenfilename

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

from shutil import copyfile

import ntpath


# PasswordWindow object
# Creates a window containing an entry and submit button to return a password

class PasswordWindow(tkinter.Tk):

	def __init__(self, parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()
		frame = tkinter.LabelFrame(self)
		frame.grid(row=0, columnspan=7, sticky='W',
				   padx=5, pady=5, ipadx=5, ipady=5)

		self.label = tkinter.Label(frame, text="Enter password to")
		self.label.grid(row=0, column=0, sticky='WE', padx=5, pady=2)
		self.label2 = tkinter.Label(frame,
									text='Your password can not be empty')
		self.label2.grid(row=1, column=2, sticky='W')
		self.label3 = tkinter.Label(frame, text='encrypt/decrypt with')
		self.label3.grid(row=1, column=0, sticky='WE', padx=10)

		self.entry = tkinter.Entry(frame)
		self.entry.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')

		self.password = None

		SubmitBtn = tkinter.Button(frame, text="Submit", command=self.submit)
		SubmitBtn.grid(row=3, column=3, sticky='W', padx=5, pady=2)

	def submit(self):
		self.password = self.entry.get()
		if not self.password == '':
			self.quit()

# End PasswordWindow


# MainMenu object
# Creates a menu with an 'encrypt' button and a 'decrypt' button

class MainMenu(tkinter.Tk):

	def __init__(self, parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()
		frame = tkinter.LabelFrame(self)
		frame.grid(row=0, columnspan=9, sticky='W',
				   padx=10, pady=5, ipadx=0, ipady=0)

		label = tkinter.Label(frame,
							  text='Your finished file will be\nin the same ' +
							  'folder as\nthe encrypt.exe file')
		label.grid(row=1, column=2, sticky='N')
		label2 = tkinter.Label(frame,
							   text='Encrypt or Decrypt any ' +
							   'file with a password')
		label2.grid(row=0, column=2, sticky='N', ipady=5)

		encButton = tkinter.Button(frame, text="Encrypt", command=self.callEnc,
								   width=10, height=5)
		encButton.grid(row=1, column=1, sticky='W', padx=5, pady=5)

		decButton = tkinter.Button(frame, text="Decrypt", command=self.callDec,
								   width=10, height=5)
		decButton.grid(row=1, column=3, sticky='E', padx=5, pady=5)


	# chooseFile method
	# opens a window for the user to choose a file, runs PasswordWindow,
	# and returns the path to chosen file, path to new file, and the password
	# created in PasswordWindow

	def chooseFile(self):
		filename = askopenfilename()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		newfile = copyfile(filename, (dir_path + '\\'
			+ filenameFromPath(filename) + 'TEMP'))

		app = PasswordWindow(None)
		app.title('Password')
		app.mainloop()

		return [filename, newfile, app.password]

	#End chooseFile


	# getKey method
	# Creates a SHA256 hash from the password taken from the PasswordWindow object

	def getKey(self, password):
		encoded = password.encode('utf-8')
		hasher = SHA256.new(encoded)
		return hasher.digest()

	# End getKey


	# callEnc method
	# Calls the encrypt function with the name of the temp
	# file and the hash created from the password in PasswordWindow

	def callEnc(self):
		[newfile, password] = self.chooseFile();
		encrypt(self.getKey(password), newfile)
		os.remove(newfile)
		sys.exit(0)

	# End callEnc


	# callDec method 
	# Calls the decrypt function with the name of the temp
	# file and the hash created from the password in PasswordWindow

	def callDec(self):
		[newfile, password] = self.chooseFile();
		decrypt(self.getKey(password), filenameFromPath(newfile))
		os.remove(newfile)
		sys.exit(0)

	# End callDec

# End MainMenu


# encrypt Function
# Takes in the key passed from getKey, along with the filename of the temp file
# created in callEnc. Opens the temp file in 'rb', opens a new file with
# (encrypted) tag, writes the IV, and encrypts in 64*1042 byte chunks until all
# chunks in temp file have been encrypted

def encrypt(key, filename):
	chunksize = 64 * 1024
	outputFile = filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = get_random_bytes(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open('(encrypted)'
				  + filenameFromPath(outputFile)[:-4:], 'wb') as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += (' '.encode('utf-8')) * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))

# End encrypt


# decrypt Function
# Takes in the key passed from getKey, along with the filename of the temp file
# created in callDec. Opens the temp file in 'rb', opens a new file without
# (encrypted) tag, reads the IV, and decrypts in 64*1042 byte chunks until all
# chunks in temp file have been decrypted

def decrypt(key, filename):
	chunksize = 64 * 1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile[:-4:], 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)

# End decrypt


# filenameFromPath Function
# Takes in the path to a file and just grabs the actual filename from it

def filenameFromPath(path):
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)

# End filenameFromPath


# run the THING
if __name__ == '__main__':
	app = MainMenu(None)
	app.title('Menu')
	app.mainloop()
