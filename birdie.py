import wiggle

#######################################
#
#	Base Operations
#
#######################################
def noop(instruction):
	pass

def set(instruction):
	"""
		code: 0x1
		arguments: dst register ID (4 bits), 1 short value (24 bits)
		effect: the dst register is set to the given value
		Ex: SET %A, $20 ==> 0x10000014
	"""
	register_dst = instruction[:1]
	value = int(instruction[1:], 16)

	registers[register_dst] = value

def move(instruction):
	"""
		code: 0x2
		arguments: dst register ID (4 bits), src register ID (4 bits)
		effect: the dst register is set to the value of the src register
		Ex: MOVE %D, %B ==> 0x23100000
	"""
	register_dst = instruction[:1]
	register_src = instruction[1:2]

	registers[register_dst] = registers[register_src]

def load(instruction):
	"""
		code: 0x3
		arguments: dst register ID (4 bits), stack pointer register ID (4 bits)
		effect: the dst register is set to the value of the memory location 
			identified by the value of the stack pointer register
		Ex: LOAD %C, @A ==> 0x32000000. If register A contains the number 8, 
			and the 7th stack (memory) location (0-indexed) contains a 43, then 
			after this instruction, register C should contain a 43.
	"""
	register_dst = instruction[:1]
	stack_ptr = instruction[1:2]

	stack_val = stack[registers[stack_ptr]]
	registers[register_dst] = stack_val
	

def store(instruction):
	"""
		code: 0x4
		arguments: stack pointer register ID (4 bits), src register ID (4 bits)
		effect: the memory location identified by the value of the stack pointer 
				register is set to the value of the src register
		Ex: STORE @B, %E ==> 0x41400000. If register B contains the number 0, 
			and register E contains the number 1, then after this instruction 
			executes the 1st stack (memory) location (0-indexed) should 
			contain a 1.
	"""
	stack_ptr = instruction[:1]
	register_src = instruction[1:2]

	stack[registers[stack_ptr]] = registers[register_src]

def read(instruction):
	"""
		code: 0x5
		arguments: None
		effect: a number from standard input is stored in register A
		Ex: READ ==> 0x50000000. If the next number of standard input is 74, 
			then after this instruction runs, register A should contain 74. 
			The behavior is not defined for the case where there are no more 
			numbers to read from standard input. But unless you've hit EOF (or 
			an input error occurs), then you HAVE to do whatever necessary 
			to put a number into this register, including waiting for 
			more input.
	"""
	while True:
		value = raw_input('(int): ')
		if value.isdigit():
			break
		print 'The input must be a integer number'

	registers['0'] = int(value)

def write(instruction):
	"""
		code: 0x6
		arguments: None
		effect: the contents of register A are written to stdout
		Ex: WRITE ==> 0x60000000. If register A contains 39, then after 
			this instruction executes, "39\n" should be written to stdout.
	"""
	print registers['0']

def add(instruction):
	"""
		code: 0x7
		arguments: dst register ID (4 bits), src register ID (4 bits)
		effect: the dst register is set to the sum of itself and the 
				src register
		Ex: ADD %D, %B ==> 0x73100000. If register D contains 39, and 
			register B contains -19, then after this instruction executes, 
			register D should contain 20.
	"""
	register_dst = instruction[:1]
	register_src = instruction[1:2]

	registers[register_dst] = registers[register_dst] + registers[register_src]

def sub(instruction):
	"""
		code: 0x8
		arguments: dst register ID (4 bits), src register ID (4 bits)
		effect: the dst register is set to the difference of itself and the 
				src register
		Ex: SUB %D, %B ==> 0x73100000. If register D contains 20, and register 
			B contains 19, then after this instruction executes, register D 
			should contain 39.
	"""
	register_dst = instruction[:1]
	register_src = instruction[1:2]

	registers[register_dst] = registers[register_dst] - registers[register_src]

def mul(instruction):
	"""
		code: 0x9
		arguments: dst register ID (4 bits), src register ID (4 bits)
		effect: the dst register is set to the product of itself and the 
				src register
		Ex: MUL %D, %B ==> 0x73100000. If register D contains 3, and register 
			B contains 13, then after this instruction executes, register 
			D should contain 39.
	"""
	register_dst = instruction[:1]
	register_src = instruction[1:2]

	registers[register_dst] = registers[register_dst] * registers[register_src]

def div(instruction):
	"""
		code: 0xA
		arguments: dst register ID (4 bits), src register ID (4 bits)
		effect: the dst register is set to the quotient (result of 
				division...yes, I had to ask 3 people that, one of which had 
				to google it for us to find out... and one of them used to work 
				at Bloomberg...sigh) of itself and the src register
		Ex: DIV %D, %B ==> 0x73100000. If register D contains 3, and register 
			B contains 2, then after this instruction executes, register D 
			should contain 1.
	"""
	register_dst = instruction[:1]
	register_src = instruction[1:2]

	registers[register_dst] = registers[register_dst] // registers[register_src]

def jmp(instruction):
	"""
		code: 0xB
		arguments: instruction location (28 bits, 0-indexed) to execute next
		effect: the next instruction to execute shall be value'th instruction 
				in the program
		Ex: JMP $1 ==> 0xB0000001. The next instruction to execute shall be the 
			2nd instruction of the program, and normally after that (so, unless 
			that instruction is a jmp itself, then the following instruction 
			should be the 3rd one (index 2).
	"""
	next = int(instruction, 16)
	registers['pc'] = next - 1

def jmp_z(instruction):
	"""
		code: 0xC
		arguments: instruction location (28 bits, 0-indexed) to execute next
		effect: if register A contains a 0, the next instruction to execute 
				shall be value'th instruction in the program, otherwise nothing 
				shall happen
		Ex: JMP_Z $1 ==> 0xC0000001. If register A contains a 0, then the next 
			instruction to execute shall be the 2nd instruction of the program, 
			otherwise the instruction following this one should be executed next.
	"""
	if registers['0'] is 0:
		next = int(instruction, 16)
		registers['pc'] = next - 1

def jmp_nz(instruction):
	"""
		code: 0xD
		arguments: instruction location (28 bits, 0-indexed) to execute next
		effect: if register A doesn't contain a 0, the next instruction to 
		execute shall be value'th instruction in the program, otherwise nothing 
		shall happen
		Ex: JMP_Z $1 ==> 0xD0000001. If register A contains anything besides a 
			0, then the next instruction to execute shall be the 2nd 
			instruction of the program, otherwise the instruction following 
			this one should be executed next.
	"""
	if registers['0'] is not 0:
		next = int(instruction, 16)
		registers['pc'] = next - 1

def jmp_gt(instruction):
	"""
		code: 0xE
		arguments: instruction location (28 bits, 0-indexed) to execute next
		effect: if register A contains a number bigger than 0, the next 
				instruction to execute shall be value'th instruction in the 
				program, otherwise nothing shall happen
		Ex: JMP_GT $1 ==> 0xE0000001. If register A contains a 1 or greater, 
			then the next instruction to execute shall be the 2nd instruction 
			of the program, otherwise the instruction following this one should 
			be executed next.
	"""
	if registers['0'] > 0:
		next = int(instruction, 16)
		registers['pc'] = next - 1

def jmp_lt(instruction):
	"""
		code: 0xF
		arguments: instruction location (28 bits, 0-indexed) to execute next
		effect: if register A contains a number smaller than 0, the next 
				instruction to execute shall be value'th instruction in the 
				program, otherwise nothing shall happen
		Ex: JMP_LT $1 ==> 0xF0000001. If register A contains a -1 or greater, 
			then the next instruction to execute shall be the 2nd instruction 
			of the program, otherwise the instruction following this one should 
			be executed next.
	"""
	if registers['0'] < 0:
		next = int(instruction, 16)
		registers['pc'] = next - 1

#######################################
#
#	Printing functions
#
#######################################
def mute():
	pass

def verbose():
	print "instruction: %s(%s) -> a: %s b: %s c: %s d: %s e: %s s: %s stack: %s" \
			%(
				instruction_map[instruction[:1]].__name__,
				instruction[1:],
				registers['0'],
				registers['1'],
				registers['2'],
				registers['3'],
				registers['4'],
			 	registers['5'],
			 	str(stack),
			)

def debug():
	raw_input('Press a key to continue')

#######################################
#
#	Main App
#
#######################################
if __name__ == '__main__':
	import argparse
	import sys

	parser = argparse.ArgumentParser()

	# adding args
	parser.add_argument("file", help="The file that contains the program to execute")
	parser.add_argument("-c","--compile", help="Compiles the .worma file into .wormbc before execution",
						action="store_true", default=False)
	parser.add_argument("-v", "--verbose", help="increase output verbosity",
	                    action="store_true", default=False)
	parser.add_argument("-d", "--debug", help="Pause for every instruction processed",
	                    action="store_true", default=False)
	args = parser.parse_args()

	try:
		# Load the program and compile if necessary
		if args.compile:	
			program = wiggle.assemble(open(args.file, 'r').readlines())
		else:
			program =  [line.strip() for line in open(args.file, 'r')]
	except:
		sys.exit('Error loading program')
	
	# Define Registers
	registers = {
		'0': 0, # A
		'1': 0, # B
		'2': 0, # C
		'3': 0, # D
		'4': 0,	# E
		'5': 0, # S
		'pc': 0, # program counter
	}

	instruction_map = {
		'0':noop,
		'1':set,
		'2':move,
		'3':load,
		'4':store,
		'5':read,
		'6':write,
		'7':add,
		'8':sub,
		'9':mul,
		'A':div,
		'B':jmp,
		'C':jmp_z,
		'D':jmp_nz,
		'E':jmp_gt,
		'F':jmp_lt,
	}

	stack = {}

	do_verbose = mute if not args.verbose else verbose
	do_debug = mute if not args.debug else debug

	program_len = len(program)

	# for each line execute program
	while registers['5'] != 1 and registers['pc'] < program_len:
		instruction = program[registers['pc']]

		instruction_map[instruction[:1]](instruction[1:])
		do_verbose()
		do_debug()

		registers['pc'] += 1
