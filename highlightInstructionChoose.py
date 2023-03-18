# Highlights target instructions using the colors of your choice.

#This is a modification to the "Highlight_Target_Instructions.py" by AGDCservices


from java.awt import Color


# define RGB colors for target instructions

# color_default sets non-target instructions colors
# needed to account for bug in graph view
colorDefault = Color(255,255,255) # white



red = Color(255, 220, 220) #light red
blue = Color(200, 240, 255) # blue
violet = Color(245, 205, 255) # violet
green = Color(180, 230, 170) # green
yellow = Color(255, 233, 180) # yellow
orange = Color(255, 200, 100) # orange
lightGrey = Color(220, 220, 220) # light grey
darkGrey = Color(195, 195, 195) # dark grey


def chooseColor():
	colorNames = ['red', 'blue', 'violet', 'green', 'yellow', 'orange', 'light grey', 'dark grey', ‘default’]
	colors = [red, blue, violet, green, yellow, orange, lightGrey, darkGrey, colorDefault]
	colorChoice = askChoice("Choose a color", "Select a color to use:", colorNames, colorNames[0])
	return colors[colorNames.index(colorChoice)]


print("The first color you choose will be assigned to the call instructions.")
colorCall = chooseColor()
print("The second color you choose will be assigned to the lea instructions.")
colorPointer = chooseColor()
print("The third color you choose will be assigned to suspected crypto instructions.")
colorCrypto = chooseColor()
print("The fourth color you choose will be assigned to string operations.")
colorStringOperation = chooseColor()


REG_TYPE = 512


# loop through all program instructions searching
# for target instructions.  when found, apply defined
# color
instructions = currentProgram.getListing().getInstructions(True)
for curInstr in instructions:

	bIsTargetInstruction = False

	curMnem = curInstr.getMnemonicString().lower()

	# color call instructions
	if curMnem == 'call':
    	bIsTargetInstruction = True
    	setBackgroundColor(curInstr.getAddress(), colorCall)


	# color lea instructions
	if curMnem == 'lea':
    	bIsTargetInstruction = True
    	setBackgroundColor(curInstr.getAddress(), colorPointer)


	#
	# color suspected crypto instructions
	#

	# xor that does not zero out the register
	if (curMnem == 'xor') and (curInstr.getOpObjects(0) != curInstr.getOpObjects(1)):
    	bIsTargetInstruction = True
    	setBackgroundColor(curInstr.getAddress(), colorCrypto)


	# common RC4 instructions
	if (curMnem == 'cmp') and (curInstr.getOperandType(0) == REG_TYPE) and (curInstr.getOpObjects(1)[0].toString() == '0x100'):
    	bIsTargetInstruction = True
    	setBackgroundColor(curInstr.getAddress(), colorCrypto)

	# misc math operations
	mathInstrList = ['sar', 'sal', 'shr', 'shl', 'ror', 'rol', 'idiv', 'div', 'imul', 'mul', 'not']
	if curMnem in mathInstrList:
    	bIsTargetInstruction = True
    	setBackgroundColor(curInstr.getAddress(), colorCrypto)

	# color string operations
	#  skip instructions that start with 'c' to exclude conditional moves, e.g. cmovs
	if (curMnem.startswith('c') == False) and (curMnem.endswith('x') == False) and ( ('scas' in curMnem) or ('movs' in curMnem) or ('stos' in curMnem) ):
    	bIsTargetInstruction = True
    	setBackgroundColor(curInstr.getAddress(), colorStringOperation)




	# fixes ghidra bug
	if bIsTargetInstruction == False:
    	setBackgroundColor(curInstr.getAddress(), colorDefault)
