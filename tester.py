#run ./main many times and log the output
#run this script to check if the output is correct

import os
import sys
import subprocess
# dl math plot lib

MAX_ESP = 4
NUM_TESTS = int(sys.argv[1])
opts = ["-O0", "-O3"]
type = ["-DSIMPLE", "-DBLOCK"]

# timing over a given build configuration
def testMain():
    # run main many times
    # clear the output file
    for i in range(MAX_ESP):
        for j in range(NUM_TESTS):
            cmd = "./main " + str(i+1) + " >> logs/coutput.log" # >> to append to file
            #print(cmd)
            os.system(cmd)
    print("Done")

# somehow need to get the output of valgrind into a file and plot it
# cache results in a given build configuration
def testValgrind():
    # run main many times
    # clear the output file
    for i in range(MAX_ESP):
        for j in range(NUM_TESTS):
            #cmd = "valgrind ./main " + str(i+1) + " >> logs/voutput.txt"
            cmd = "valgrind --tool=cachegrind --log-fd=9 9>>logs/voutput.log ./main " + str(i+1)
            print(cmd)
            os.system(cmd)
            #delete the cachegrind.out file
            cmd = "rm cachegrind.out*"
            os.system(cmd)
    print("Done")

def make(flags):
    cmd = "make OPTFLAGS=\"" + flags + "\" all"
    print(cmd)
    os.system(cmd)
    
def readOutput():
    # read the output file and check if the output is correct
    # read the output file
    with open("logs/voutput.log", "rw") as file:
        lines = file.readlines()
        for line in lines:
            #clean the file from usesless lines
            break
    print("Done")

if __name__ == "__main__":
    # build with some flags -> run main many times w/o valgrind -> check output
    # plot everything
    cmd = "rm logs/*"
    os.system(cmd)
    for opt in opts:
        for t in type:
            make(opt + " " + t)
            testMain()
            testValgrind()

