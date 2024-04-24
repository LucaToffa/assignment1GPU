#run ./main many times and log the output
#run this script to check if the output is correct

import os
import sys
import subprocess
# dl math plot lib
import re
COUTPUT = "logs/coutput"
MAX_ESP = 13 #max allowed exponent by pc = 15
NUM_TESTS = int(sys.argv[1])
opts = ["-O0", "-O1", "-O2", "-O3"]
type = ["-DSIMPLE", "-DBLOCK"]

# timing over a given build configuration
def testMainSimple(opt):
    # run main many times
    # clear the output file
    #os.system("echo \"size, time\" >> logs/coutput.log")
    for i in range(MAX_ESP):
        for j in range(NUM_TESTS):
            curr_path = COUTPUT + opt 
            cmd = "./main " + str(i+1) + " >> " + curr_path +".log" # >> to append to file
            #print(cmd)
            os.system(cmd)
    print("testMainSimple Done")

def testMainBlock(opt):
    # run main many times
    # clear the output file
    #os.system("echo \"size, time, blocks\" >> logs/coutput.log")
    for i in range(MAX_ESP):
        for bsize in range(1, 8):
            for j in range(NUM_TESTS):
                if(i >= bsize):
                    prog_input = str(i+1) + " " + str(1<<bsize)
                    voutput_log = "logs/coutput" + opt +".log" 
                    cmd = "./main " + prog_input + " >> " + voutput_log # >> to append to file
                    #print(cmd)
                    os.system(cmd)
    print("testMainBlock Done")

# somehow need to get the output of valgrind into a file and plot it
# cache results in a given build configuration
def testValgrindSimple(opt):
    # run main many times
    # clear the output file
    for i in range(MAX_ESP):
        #cmd = "valgrind ./main " + str(i+1) + " >> logs/voutput.txt"
        voutput_log = "logs/voutput" + opt +".log"
        cmd = "valgrind --tool=cachegrind --log-fd=9 9>>" + voutput_log + " ./main " + str(i+1) + " > /dev/null"
        #print(cmd)
        os.system(cmd)
        readOutput(1<<(i+1), 0, opt) #get rid of all the useless lines
        #delete the cachegrind.out and valgrind files
        cmd = "rm cachegrind.out* "+ voutput_log
        os.system(cmd)
    print("testValgrindSimple Done")

def testValgrindBlock(opt):
    # run main many times
    # clear the output file
    for i in range(MAX_ESP):
        for bsize in range(1, 8):
            if(i >= bsize):
                prog_input = str(i+1) + " " + str(1<<bsize)
                voutput_log = "logs/voutput" + opt +".log"
                #cmd = "valgrind ./main " + prog_input + " >> logs/voutput.txt"
                cmd = "valgrind --tool=cachegrind --log-fd=9 9>>" + voutput_log + " ./main " + prog_input  + " > /dev/null"
                #print(cmd)
                os.system(cmd)
                readOutput(1<<(i+1), 1<<bsize, opt) #get rid of all the useless lines
                #delete the cachegrind.out and valgrind files
                cmd = "rm cachegrind.out* "+ voutput_log
                os.system(cmd)
    print("testValgrindBlock Done")

def make(flags):
    cmd = "make OPTFLAGS=\"" + flags + "\" all"
    print(cmd)
    os.system(cmd)
    
# Regex pattern
pattern = r"(miss rate|misses):\s+([\d.|,]+)"

def readOutput(size, block, opt):
    input_log = "logs/voutput" + opt +".log"
    with open(input_log, "r") as file:
        text = file.read()
        matches = re.findall(pattern, text, re.DOTALL)
        count = 0
        log = []
        for match in matches:
            log.append(match[1])
    output_log = "logs/foutput"+ opt + ".log"
    with open(output_log, "a") as output:
        output.write(str(size) + ", " + str(block) + ", " + log[2] + ", " + log[3] + ", " + log[6] + ", " + log[7] + ", " + log[9] + "\n")
    log = []

def main():
    os.system("rm logs/*")
    for opt in opts:
        make(opt + " " + type[0])
        testMainSimple(opt)
        testValgrindSimple(opt)

    for opt in opts:
        make(opt + " " + type[1])
        testMainBlock(opt)
        testValgrindBlock(opt)

if __name__ == "__main__":
    main()

