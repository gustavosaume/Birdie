A Birdie that love to eat worms
================================

Yeah, every one knows that birds eat worms, but these worms are really special. Each worm contains an awesome piece of program written in Assembler style language specified for the CS for Hackers week 7 challenge. The Worm language specification is compiled into bytecode in which each instruction is 4 bytes long. The highest 4 bits represent the instruction code and the rest can be either 4 bits registers identifiers - one, two or none registers, followed by a value argument, that takes as many bits as it can to complete the 4 bytes.

Birdie is a Virtual Machine written in Python that has 4 registers (A-D), a EOF register (E) and a stack register (S). Additionally, it has a program counter or PC that keeps track of the current instruction.

To begin with Birdie you can type birdie.py --help on your console to get more info on how to launch the VM

For more info go to https://github.com/generalassembly-studio/cs-for-hackers/tree/master/week-07

Usage
=====

Simply execute the python script birdie.py with the program file you wish to process, this file can be a wormc file for the compiled programs or a worma file with the -c arg to compile it before its execution. Additionally, you can use a series of arguments that can help you analize the program execution. This are:

* -d or --debug: will request the user to hit the entre key before executing the next statement
* -v or --verbose: will display each instruction data and stack

How to input data
-----------------

When the program requires input the user has two options. One, while the program is running or two, before executing it in the command line. If the user decides to input data while the program is running, will have to enter a new line and then the ctrl+d combination to delimit the buffer and notify the program that can continue. To use the input from the command line, the user can use for example > echo  1 2 3 | python birdie.py -c programs/reverse_input.worma
