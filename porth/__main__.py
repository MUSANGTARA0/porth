#!/usr/bin/env python3
import subprocess
import shlex
import sys
from os import path
from typing import List
from porth import compile_file_to_program, simulate_little_endian_linux, generate_nasm_linux_x86_64

def cmd_call_echoed(cmd: List[str]) -> int:
    print("[CMD] %s" % " ".join(map(shlex.quote, cmd)))
    return subprocess.call(cmd)

def usage(compiler_name: str):
    print("Usage: %s [OPTIONS] <SUBCOMMAND> [ARGS]" % compiler_name)
    print("  OPTIONS:")
    print("    -debug                Enable debug mode.")
    print("  SUBCOMMAND:")
    print("    sim <file>            Simulate the program")
    print("    com [OPTIONS] <file>  Compile the program")
    print("      OPTIONS:")
    print("        -r                  Run the program after successful compilation")
    print("        -o <file|dir>       Customize the output path")
    print("    help                  Print this help to stdout and exit with 0 code")

if __name__ == '__main__' and '__file__' in globals():
    debug = False
    argv = sys.argv
    assert len(argv) >= 1
    compiler_name, *argv = argv

    while len(argv) > 0:
        if argv[0] == '-debug':
            debug = True
            argv = argv[1:]
        else:
            break

    if debug:
        print("[INFO] Debug mode is enabled")

    if len(argv) < 1:
        usage(compiler_name)
        print("[ERROR] no subcommand is provided")
        exit(1)
    subcommand, *argv = argv

    if subcommand == "sim":
        if len(argv) < 1:
            usage(compiler_name)
            print("[ERROR] no input file is provided for the simulation")
            exit(1)
        program_path, *argv = argv
        program = compile_file_to_program(program_path);
        simulate_little_endian_linux(program)
    elif subcommand == "com":
        run = False
        program_path = None
        output_path = None
        while len(argv) > 0:
            arg, *argv = argv
            if arg == '-r':
                run = True
            elif arg == '-o':
                if len(argv) == 0:
                    usage(compiler_name)
                    print("[ERROR] no argument is provided for parameter -o")
                    exit(1)
                output_path, *argv = argv
            else:
                program_path = arg
                break

        if program_path is None:
            usage(compiler_name)
            print("[ERROR] no input file is provided for the compilation")
            exit(1)

        basename = None
        basedir = None
        if output_path is not None:
            if path.isdir(output_path):
                basename = path.basename(program_path)
                porth_ext = '.porth'
                if basename.endswith(porth_ext):
                    basename = basename[:-len(porth_ext)]
                basedir = path.dirname(output_path)
            else:
                basename = path.basename(output_path)
                basedir = path.dirname(output_path)
        else:
            basename = path.basename(program_path)
            porth_ext = '.porth'
            if basename.endswith(porth_ext):
                basename = basename[:-len(porth_ext)]
            basedir = path.dirname(program_path)
        basepath = path.join(basedir, basename)

        print("[INFO] Generating %s" % (basepath + ".asm"))
        program = compile_file_to_program(program_path);
        generate_nasm_linux_x86_64(program, basepath + ".asm")
        cmd_call_echoed(["nasm", "-felf64", basepath + ".asm"])
        cmd_call_echoed(["ld", "-o", basepath, basepath + ".o"])
        if run:
            exit(cmd_call_echoed([basepath] + argv))
    elif subcommand == "help":
        usage(compiler_name)
        exit(0)
    else:
        usage(compiler_name)
        print("[ERROR] unknown subcommand %s" % (subcommand))
        exit(1)
