from PIL import Image

print("		************Python Kursova**************")

choice = input("""
                      1: Encode
                      2: Decode

                      Please enter your choice: """)


if choice == "1":

	secretfile = input("Input the name of the file in which you want to hide a message (w/o extension): ")
	secretfile = secretfile + ".txt"

	try:
		f_crypt = open(secretfile, 'r')
		crypt_text = f_crypt.read()
		f_crypt.close()
	except FileNotFoundError:
		print("File does not exist!")
		quit()


	secrettext = input("Input the message you want to hide in the text file: ")

	def TextEncode(secrettext):
		encoded_text = []
		for letter in secrettext:
			for ch in letter:
				encoded_text.append(ord(ch) - 5)

		return ''.join(chr(ch) for ch in encoded_text)
		
	TextEncode(secrettext)

	f = open(secretfile,'w')
	f.write(TextEncode(secrettext))
	f.close()

	#Отваряне с проверка за съществуване на изображението със секретното съобщение
	secretimage = input("Input the name of the image in which you want to hide a message: ")

	try:
		img = Image.open(secretimage)
	except FileNotFoundError:
		print("Image does not exist!")
		quit()

	imagesecret = input("Input the message you want to hide in the image: ") + '@'

	#Функция, която добавя 5 към аски кодовете на всяка буква във въведения стринг за изображение
	def ImageTextEncode(imagesecret):
		img_new = []
		for letter in imagesecret:
			for ch in letter:
				img_new.append(ord(ch) +5)

		return ''.join(chr(ch) for ch in img_new)

	ImageTextEncode(imagesecret)

	#Функция за превръщане на тайното съобщение в двоичен вид
	def EncodeTextToBin():
		secret = ImageTextEncode(imagesecret)
		img_bin = ""
		for symbol in secret:
			img_bin += str(format(ord(symbol), '08b'))
		return img_bin
	EncodeTextToBin()

	# Функция за проверка на четност
	def even(num):
		if num % 2 == 0:
			return True
		else:
			return False

	# Функция за промяна на най-младшия бит
	def change(num, bit):
		if bit == '0' and even(num):
			return num, 0
		if bit == '0' and not even(num):
			return num - 1, 1
		if bit == '1' and even(num):
			return num + 1, 1
		if bit == '1' and not even(num):
			return num, 0

	# Функция за вмъкване на секретното съобщение в изображение
	def Embedding():
		ImgBinText = EncodeTextToBin()
		numberBytes = len(ImgBinText)
		br = 0
		pixels = img.load()
		changes = 0
		for i in range(0, img.size[0]):
			for j in range(0, img.size[1]):
				b,g,r = pixels[i,j]
				if br < numberBytes:
					b, ch = change(b, ImgBinText[br])
					br += 1
					changes += ch
				if br < numberBytes:
					g, ch = change(g, ImgBinText[br])
					br += 1
					changes += ch
				if br < numberBytes:
					r, ch = change(r, ImgBinText[br])
					br += 1
					changes += ch
				pixels[i,j] = b,g,r

		maxByteImage = img.size[0]*img.size[1]*3
		lengthSecretText = len(imagesecret)*8

		if lengthSecretText > maxByteImage:
			print("The message is too big for the image! ")
			quit()
		else:
			img.save("encoded.bmp")
			img.close()
			print("Total changes needed to hide the message:", changes)
			print("Succesfully encoded! ")

	Embedding()



elif choice == "2":
	secretfile = input("Input the name of the file which you want to decode (w/o extension:) ")
	secretfile = secretfile + ".txt"

	try:
		f_crypt = open(secretfile,'r')
		crypt_text = f_crypt.read()
		f_crypt.close()
	except FileNotFoundError:
		print("File does not exist!")
		quit()

	secretimage = input("Input the name of the image you want to decode (w/o extension): ")
	secretimage = secretimage + ".bmp"

	try:
		img = Image.open(secretimage)
		pixels = img.load()
		l_pixels = []
	except FileNotFoundError:
		print("Image does not exist!")
		quit()

	#Функция, която намира двоичния вид на най-младшия бит и, превръща го в аски код и изважда 5
	def Getsymbol(octet):
		bnr = ""
		for each in range(0,len(octet)):
			bnr += str(format(octet[each],'08b'))[7]
		return chr(int(bnr,2) -5)
		

	def PixelMatrixToList(pixels):
		for i in range(0,img.size[0]):
			for j in range(0,img.size[1]):
				b,g,r = pixels[i,j]
				l_pixels.append(b)
				l_pixels.append(g)
				l_pixels.append(r)
		return l_pixels
	PixelMatrixToList(pixels)

	stegoText = ""
	for i in range(0,len(l_pixels),8):
		symbol = Getsymbol(l_pixels[i:i+8])
		if symbol == '@':
			break
		else:
			stegoText += symbol

	#Функция за намиране на Ascii стойностите на буквите от файла, добавя 5 към всяка от тях и връща новополучените стойности като string
	def DecodeText(crypt_text):
		new_text = []
		for letter in crypt_text:
			for ch in letter:
				new_text.append(ord(ch) + 5)
		return ''.join(chr(ch) for ch in new_text)
		
	DecodeText(crypt_text)


	print("The hidden message is:", DecodeText(crypt_text), end=' ' + stegoText)

	#Записва съобщението в нов файл
	f = open("decoded.txt",'w')
	f.write(" ".join([DecodeText(crypt_text),stegoText]))
	f.close()

else:
	print("Wrong choice!")
	print("Please try again!")
