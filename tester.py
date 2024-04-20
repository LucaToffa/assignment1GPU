#run ./main many times and log the output
#run this script to check if the output is correct

import os
import sys
import subprocess
# dl math plot lib
import re

MAX_ESP = 13 #max allowed exponent by pc = 15, 13 for valgrind
NUM_TESTS = int(sys.argv[1])
opts = ["-O0", "-O3"] 
#opts = ["-O1", "-O2"] #still need to test 
type = ["-DSIMPLE", "-DBLOCK"]

# timing over a given build configuration
def testMainSimple():
    # run main many times
    # clear the output file
    os.system("echo \"size, time\" >> logs/coutput.log")
    for i in range(MAX_ESP):
        for j in range(NUM_TESTS):
            cmd = "./main " + str(i+1) + " >> logs/coutput.log" # >> to append to file
            #print(cmd)
            os.system(cmd)
    print("Done")

def testMainBlock():
    # run main many times
    # clear the output file
    os.system("echo \"size, time, blocks\" >> logs/coutput.log")
    for i in range(MAX_ESP):
        for bsize in range(1, 8):
            for j in range(NUM_TESTS):
                if(i > bsize):
                    prog_input = str(i+1) + " " + str(1<<bsize)
                    cmd = "./main " + prog_input + " >> logs/coutput.log" # >> to append to file
                    #print(cmd)
                    os.system(cmd)
    print("Done")

# somehow need to get the output of valgrind into a file and plot it
# cache results in a given build configuration
def testValgrindSimple():
    # run main many times
    # clear the output file
    for i in range(MAX_ESP):
        #cmd = "valgrind ./main " + str(i+1) + " >> logs/voutput.txt"
        cmd = "valgrind --tool=cachegrind --log-fd=9 9>>logs/voutput.log ./main " + str(i+1) + " > /dev/null"
        #print(cmd)
        os.system(cmd)
        #delete the cachegrind.out file
        cmd = "rm cachegrind.out*"
        os.system(cmd)
    print("Done")

def testValgrindBlock():
    # run main many times
    # clear the output file
    for i in range(MAX_ESP):
        for bsize in range(1, 6):
            if(i > bsize):
                prog_input = str(i+1) + " " + str(1<<bsize)
                #cmd = "valgrind ./main " + prog_input + " >> logs/voutput.txt"
                cmd = "valgrind --tool=cachegrind --log-fd=9 9>>logs/voutput.log ./main " + prog_input  + " > /dev/null"
                #print(cmd)
                os.system(cmd)
                #delete the cachegrind.out file
                cmd = "rm cachegrind.out*"
                os.system(cmd)
    print("Done")

def make(flags):
    cmd = "make OPTFLAGS=\"" + flags + "\" all"
    print(cmd)
    os.system(cmd)
    
# Regex pattern
pattern = r"(miss rate|misses):\s+([\d.|,]+)"

# Find all matches
def readOutput():
    # read the output file and check if the output is correct
    # read the output file
    with open("logs/voutput.log", "r") as file:
        text = file.read()
        #clean the file from usesless lines
        matches = re.findall(pattern, text, re.DOTALL)
        #print(re.findall(r"(miss rate|misses):\s+([\d.|,]+)", data, re.M))
        # Display the matches
        count = 0
        with open("logs/output.log", "a") as output:
            output.write("#I1m LLim I1mr LLimr D1m LLdm D1mr LLdmr LLm LLmr\n")
        for match in matches:
            #write each match to file
            with open("logs/output.log", "a") as output:
                #output.write(match[0] + " " + match[1] + "\n")
                output.write(match[1] + " ")
                count += 1
                if(count % 10 == 0):
                    output.write("\n") 
                    #if((count) % (NUM_TESTS*10) == 0):
                    #    output.write("\n")               

if __name__ == "__main__":
    # build with some flags -> run main many times w/o valgrind -> check output
    # plot everything
    cmd = "rm logs/*"
    os.system(cmd)
    for opt in opts:
        make(opt + " " + type[0])
        #testMainSimple()
        testValgrindSimple()
    for opt in opts:
        make(opt + " " + type[1])
        #testMainBlock()
        testValgrindBlock()
    readOutput()


