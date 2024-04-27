#run ./main many times and log the output
#run this script to check if the output is correct

import os
import sys
import re
COUTPUT = "logs/coutput"
MAX_ESP = 13 #max allowed exponent by pc = 15 (16GB ram)
NUM_TESTS = int(sys.argv[1])
opts = ["-O0", "-O1", "-O2", "-O3"]
type = ["-DSIMPLE", "-DBLOCK"]

# timing over a given build configuration
def testMainSimple(opt):
    for i in range(MAX_ESP):
        for j in range(NUM_TESTS):
            curr_path = COUTPUT + opt 
            cmd = "./main " + str(i+1) + " >> " + curr_path +".log"
            #print(cmd)
            os.system(cmd)
    print("testMainSimple Done")

def testMainBlock(opt):
    for i in range(MAX_ESP):
        for bsize in range(1, 8):
            for j in range(NUM_TESTS):
                if(i >= bsize):
                    prog_input = str(i+1) + " " + str(1<<bsize)
                    voutput_log = "logs/coutput" + opt +".log" 
                    cmd = "./main " + prog_input + " >> " + voutput_log
                    os.system(cmd)
    print("testMainBlock Done")

def testValgrindSimple(opt):
    for i in range(MAX_ESP):
        voutput_log = "logs/voutput" + opt +".log"
        cmd = "valgrind --tool=cachegrind --log-fd=9 9>>" + voutput_log + " ./main " + str(i+1) + " > /dev/null"
        os.system(cmd)
        readOutput(1<<(i+1), 0, opt) #get rid of all the useless lines
        #delete the cachegrind.out and valgrind files
        cmd = "rm cachegrind.out* "+ voutput_log
        os.system(cmd)
    print("testValgrindSimple Done")

def testValgrindBlock(opt):
    for i in range(MAX_ESP):
        for bsize in range(1, 8):
            if(i >= bsize):
                prog_input = str(i+1) + " " + str(1<<bsize)
                voutput_log = "logs/voutput" + opt +".log"
                cmd = "valgrind --tool=cachegrind --log-fd=9 9>>" + voutput_log + " ./main " + prog_input  + " > /dev/null"
                os.system(cmd)
                readOutput(1<<(i+1), 1<<bsize, opt) #get rid of all the useless lines
                #delete the cachegrind.out and valgrind files
                cmd = "rm cachegrind.out* "+ voutput_log
                os.system(cmd)
    print("testValgrindBlock Done")

def make(flags):
    cmd = "make OPTFLAGS=\"" + flags + "\" main"
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

