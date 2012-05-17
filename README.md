A Birdie that love worms
========================

Yeah, every one knows that birds eat worms, but these worms are really special. Each worm contains an awesome piece of program written in Assembler style language specified for the CS for Hackers week 7 challenge. The Worm language specification is compiled into bytecode in which each instruction is 4 bytes long. The highest 4 bits represent the instruction code and the rest can be either 4 bits registers identifiers - one, two or none registers, followed by a value argument, that takes as many bits as it can to complete the 4 bytes.

Birdie is a Virtual Machine written in Python that has 4 registers (A-D), a EOF register (E) and a stack register (S). Additionally, it has a program counter or PC that keeps track of the current instruction.

To begin with Birdie you can type birdie.py --help on your console to get more info on how to launch the VM

For more info go to https://github.com/generalassembly-studio/cs-for-hackers/tree/master/week-07


