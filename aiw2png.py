import sys
import png

#set to 1 to invert colours
inverse = 0

#set to 1 to display debug messages, might be of use when
#there are some unsupported opcodes which need to be implemented
debug = 0

color_fg = 0
color_bg = 0

if inverse:
	color_fg = 255
	color_bg = 0
else:
	color_fg = 0
	color_bg = 255

width = 0
height = 0
screen = []

def debug_print(s, end = "\r\n"):
	if debug:
		print(s, end = end)

#load file into a byte array
if len(sys.argv) != 2:
	print("Provide filename")
	sys.exit()
	
f = open(sys.argv[1], "rb")
data = bytearray(f.read())

#interpret the data
idx = 0
x = 0
y = 0
linefeed_directon = 0
line_distance = 0
x_step = 1
while 1:
	#escape symboles
	if data[idx] == 0x1b:
		debug_print("escape: ", end = '')
		idx += 1
		escape = data[idx]
		debug_print(hex(escape))
		idx += 1
		if escape == 0x3f:
			debug_print("Self ID - do nothing")
		elif escape == 0x6f:
			debug_print("command: paper detection in function - do nothing")
		elif escape == 0x54:
			debug_print("command: set distance between lines to: ", end = '')
			distance = (data[idx] - 0x30) * 10
			idx += 1
			distance += data[idx] - 0x30
			idx += 1
			debug_print(str(distance) + " / 144 inch")
			line_distance = distance
		elif escape == 0x72:
			debug_print("command: reverse linefeed")
			linefeed_directon = 1
		elif escape == 0x66:
			debug_print("command: normal linefeed")
			linefeed_directon = 0
		elif escape == 0x4e:
			debug_print("command: 10 characters per inch - do nothing")
			x_step = 1
		elif escape == 0x50:
			debug_print("command: 160 points per inch - do nothing")
			x_step = 2
		elif escape == 0x21:
			debug_print("command: boldface begin - do nothing")
		elif escape == 0x3e:
			debug_print("command: left to right only - do nothing")
		elif escape == 0x47:
			debug_print("command: print: ", end = '')
			count = (data[idx] - 0x30) * 1000
			idx += 1
			count += (data[idx] - 0x30) * 100
			idx += 1
			count += (data[idx] - 0x30) * 10
			idx += 1
			count += data[idx] - 0x30
			idx += 1
			debug_print(str(count) + " bytes as bit image graphics")
			for i in range(0, count, x_step):
				for j in range(0, 8):
					while y + j >= len(screen):
						screen.append([])
					while x >= len(screen[y + j]):
						screen[y + j].append(color_bg)						
					if data[idx + i] & (1 << j):
						screen[y + j][x] = color_fg
					else:
						screen[y + j][x] = color_bg
				x += 1
			idx += count
		elif escape == 0x46:
			debug_print("command: begin printing at dot position: ", end = '')				
			count = (data[idx] - 0x30) * 1000
			idx += 1
			count += (data[idx] - 0x30) * 100
			idx += 1
			count += (data[idx] - 0x30) * 10
			idx += 1
			count += data[idx] - 0x30
			idx += 1
			x += count
			debug_print(str(count))
		else:
			debug_print("!!!UNKNOWN OPCODE, FURTHER OPERATION MIGHT BE INVALID!!!")
	#control symboles
	else:
		if data[idx] == 0x0D:
			debug_print("carriage return")
			x = 0
		if data[idx] == 0x0A:
			debug_print("newline")
			if linefeed_directon == 1:
				y -= line_distance // 2
			else:
				y += line_distance // 2
				
		idx += 1
	if idx >= len(data):
		break

for w in screen:
	if len(w) > width:
		width = len(w)
height = len(screen)

print(str(width) + "x" + str(height))

picture = open(sys.argv[1] + ".png", "wb")
writer = png.Writer(width, height, greyscale = True)

for i in range(0, height):
	l = len(screen[i])
	for x in range(0, width - l):
		screen[i].append(color_bg)
	
writer.write(picture, screen)
picture.close()	