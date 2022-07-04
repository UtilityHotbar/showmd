# NOVOS Assembly Language Editor (NOVOS-ALED) Specification
*Copyright HAVLAND TECHNICA 1999. All rights reserved.*

## Introduction
ALED is intended for debugging small programs written in the NOVOS Assembly dialect (NOVASM). These programs usually implement low-level syscalls due to their high efficiency and low runtime cost. In th event of a misimplemented or corrupted syscall on startup ALED is automatically started from ROM in manual debugging mode.

## Debugger Commands
* **name**: Gives the name of the syscall. *Example: "name" will return "Swizzle Function" for a syscall that implements the swizzle function.*
* **tgt**: Allows you to view the *target* memory state of the virtual memory allocated to this syscall. Your aim is to make sure that at the end of program execution memory resembles the output of `tgt`. *Example: "tgt" shows you the relevant memory locations for the current syscall. (? means any value is acceptable at that memory location)*
* **mem**: Allows you to inspect the *current* state of the virtual memory allocated to this syscall. *Example:  "mem" after a program has crashed allows you to examine the memory at the moment of the crash.*
* **diff** `x`: Gives you the memory limit for this patch (the number of characters you can add/edit/delete) and shows the difference between the starting line `x` and the current (patched) line `x`. If you haven't changed line `x`, there will be no difference. If `x` is not provided it diffs the entire source code. *Example: "diff 10" will show differences in line 11 of the source code (ALED is 0-indexed)*.
* **res**: Resets memory to initial state. Useful for restarting programs. Patched code is NOT reset. *Example usage: "res".*
* **marks**: Prints all marks. Marks are points code can jump to using `JIF` or `JMP`. *Example: "marks"*
* **print** `x`: Prints the *current* state of the code at line `x`. If `x` is not provided it will print the entire code block with line numbers. *Example: "print 10" prints the code at line 11.*
* **orig** `x`: Prints the *original* state of the code at line `x`. If `x` is not provided it will print the entire code block. *Example: "orig 10" prints the original unpatched code at line 11.*
* **patch** `x` `newline`: Replaces line `x` with the contents of `newline`. Shows you how many characters have changed. *Example: "patch 0 ADD $0 $1 $2" will replace the contents of line 0 with "ADD $0 $1 $2".*
* **run** `x`: Runs `x` lines of code, then stops until you invoke `run` again. If `x` is not provided will run until it errors, finishes, or runs into a breakpoint. *Example: "run 2" will run the next 2 lines of code.*

## Assembly Instruction Set
### System Description
For most low-level syscalls the system has:
* An initial code-block implementing the syscall
* An Instruction Pointer (`$IP`) register pointing ot the current line of code
* 100 memory locations labelled from `$0` to `$99`

### Arithmetic
* **ADD** `val1` `val2` `dest`: Adds the values at memory locations `val1` and `val2` and writes the result to memory location `dest`. `ADD $0 $1 $2` adds the values at `$0` and `$1` and writes the output to memory location `$2`.
* **SUB** `val1` `val2` `dest`: Subtracts the values at memory locations `val1` and `val2` and writes the result to memory location `dest`.

### Testing
* **TEQ** `val1` `val2` `dest`: Tests if the values at memory locations `val1` and `val2` fulfill the condition `val1 == val2`. If yes, writes `1` to memory location `dest`. If not, writes `-1`.
* **TLT** `val1` `val2` `dest`: Tests if the values at memory locations `val1` and `val2` fulfill the condition `val1 < val2`. If yes, writes `1` to memory location `dest`. If not, writes `-1`.
* **TLT** `val1` `val2` `dest`: Tests if the values at memory locations `val1` and `val2` fulfill the condition `val1 > val2`. If yes, writes `1` to memory location `dest`. If not, writes `-1`.

### Flow Control
* **MRK** `name`: Creates a mark with the name `name`. `MRK START` creates a mark with the name `START` that can be referenced with `:START`.
* **JMP** `name`: Jumps to the mark with the name `name` and continues executing.
* **JIF** `loc` `tgt`: If the value at memory location `loc` is positive (i.e. `loc >= 1`) jump to the location specified in `tgt`. This can be the value of another memory location or a mark. `JIF $1 $2` means if the value at `$1` is positive, jump to the line of code with line number specified by `$2`. `JIF $1 :START` means if the value at `$1` is positive, jump to the mark with the name `START`.

### Memory read/write
* **MOV** `start` `end`: Copies the value from the memory location `start` to the memory location `end`. `MOV $0 $1` means that `$1` will now have the value of `$0`.
* **MRD** `loc` `dest`: Reads the memory location specified by the value of `loc` and copies it to the memory location `dest`. `MRD $0 $1` where `$0` has a value of `5` means that the system will copy the value at memory location `$5` to `$1`.
* **MWT** `loc` `dest`: Writes the value at memory location `loc` to the memory location specified by the value of `dest`. `MWT $0 $1` where `$1` has a value of `5` means that the system will copy the value at memory location `$0` to `$5`.