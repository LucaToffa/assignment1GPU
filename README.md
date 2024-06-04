# Matrix transposition exploration
## Assignment 1 - GPU computing course 

An exploration of the possible speed-up and cache usage optimization for different matrix transposition algorithms (naive and block transposition) in C++.

### Disclaimer
This guide is meant for and the code is tested only for linux, 
don't expect to run as is on windows / wsl / mac.
#### Dependencies:
- python3, mathplotlib, numpy
    python3 -m pip install -U pip
    python3 -m pip install -U matplotlib numpy
- g++ (sudo apt install build-essential make)
- valgrind (sudo apt install valgrind for ubuntu derivatives)
Command may slightly vary depending on the distribution
### Building the binaries
First of all run:
```
make all
```
it will add needed folders and build the binaries for playing with the code (testsimple, testblock, analyser) except main, which is built with the following command
```
make main
```
is intended for tester.py to build and run each version of the code as needed.
Of course it can be used by the end user manually
```
make main OPTFLAGS="-O3 -DDEBUG -DPRINT -DSIMPLE"
```
Using -DPRINT for large matrices is not suggested as printing that much data in the terminal is not that useful

While -DDEBUG has just more verbose logs 

### Running the code
```shell
./testblock <mat_size_exp, block_size>
./testsimple <mat_size_exp>
```
These programs have the DEBUG flag enabled.

The first argument is the exponent e to make a matrix of 2^e rows and columns, 
for the code to complete succesfully it should not exceed the machine memory capability

```
./testsimple 15 will allocate 8GB of ram
```

The second is the size of the blocks the matrix will be divided into for block-transposition
B = block_size x block_size

**N.B. block_size should always be a power of two (the algorithm can't work otherwise, and the code will segfault)**

For safetly of the machine and timing contraint tester.py will test up to **<13, 128>**

```
python3 tester.py <iterations>
```
If the needed library are installed on the machine running this command (the argument iteration determines the number of time each matrix will be run and timed) should be enough.
Considering that the cache miss percentages coming from valgrind were not sensitive to the number of iterations, and that using valgrind is time consuming, there is only one iteration over each configuration using valgrind.

Running this script will clear all logs already in the logs folder, and it will take some time to complete

(For reference, a single iteration of tester as is may even take some minutes)

coutput-Ox.log files refer to the timing of main,
while foutput-Ox.log files refer to the simplified "final" output of valgrind, the program that performs all the cache miss analysis. 


```
./analyser
```
this program will extract data from the output files that tester.py generated.
The resulting timing and bandwidth logs can then be plotted with plotter.py

the files (one per optimization level) have this format:
```shell
#bandwidths
    <mat_size>, <block_size>, <ext_bandwidth>
#timings
    <mat_size>, <block_size>, <avg_time>, <min_time>, <max_time>
#foutuputs
    <mat_size>, <block_size>, <I1mr>,<LLimr>, <D1mr>, <LLdmr>, <LLmr>

```

finally the plotter.py will generate the plots in the plots folder,
there are many plots that can be generated, custom ones can be added by modifying the script (adding new plotting functions).
By default all the plots present in plots/ will be regenerated, to avoid it just comment the function calls. 
The scripts also uses the variables input_prefix and output_prefix, changing them will change the input and output folders respectively.

### valgrind usage

#### some examples to get you started with valgrind and understand the code
```shell
 valgrind --tool=cachegrind ./main 10 #basic usage, run a program and generate a cachegrind report
 valgrind --tool=cachegrind --log-fd=9 9>>test.log ./main 7 #send output to file descriptor 9 and append to log file
```

The Makefile itself provides a simple way to try valgrind with the code and cleanup afterwords
```shell
make valgrind_simple ARGS="10" #run valgrind with the simple version of the code and a matrix of size 2^10
make valgrind_block ARGS="10 4" #run valgrind with the block version of the code and a matrix of size 2^10 divided in 4x4 blocks
make clear_valgrind #clear the valgrind output files
``` 


# Matrix transposition exploration - GPU implementation
## Assignment 2 - GPU computing course 
Implementation of the matrix transposition algorithm on the GPU using CUDA.

### Building the binaries
make all has been updated to build transpose.cu too
```shell
make transpose T=$(VAL) B=$(VAL)
```
where T is the size of the tiles and B is the block rows.
The valid values depend on the machine and the GPU, T determines the minumum size of the matrix that can be transposed, while B determines the number of rows that will be transposed in a single block.
Also T can't be smaller than B, and both should be powers of 2, otherwise the code will not work correctly.
Default values are 32 for T and 8 for B.
DEBUG and PRINT can be enables by uncommenting the lines in the source code, but just like before PRINT is not suggested for large matrices and the DEBUG output will give a very long output.

### Running the code
on a local machine
```shell
make cuda_run #to test all the matrix sizes on the default T and B
make cuda_run N=$(VAL) #to test a specific matrix size
make cuda_run T=$(VAL) B=$(VAL) N=$(VAL) #optional change to T and B
```
where 2^N is the size of the matrix to be transposed, it should be a power of 2 and greater than 5 if T>32.
The code will run the matrix transposition algorithm on the GPU and print the timing and bandwidth of the operation.
To store the output in a file the following command has been used
```shell
make cuda_run N=$(VAL) > logs2/outputall.log
```
on the cluster 
```shell
load module cuda
make transpose
sbatch query.sh #the current file does not take parameters bacause its for automated testing
squeue -u $USER #check for running/pending jobs
scancel <job_id> #remove job from queue
```

### Profiling the code
To profile the space of possibilities a simple bash script compiles and launches the code, given the asynvhronous nature of the GPU the code will compile with different names. 
```shell
chmod +x tasklocal.sh #make the script executable
bash ./tasklocal.sh
```

On the cluster the script is slightly different, it will launch a job for each T-B combination
each output will be stored in a different file <output-%j.log>
the plotter is sensible to the order or the files, so they need to be concatenated in the correct order, that should be the same as the jobs that were launched.
```shell
chmod +x tasks.sh #make the script executable
bash ./tasks.sh #no do this manually
cat <each> <output> <file> <in> <order> >> <finaloutput> # finaloutput = outputcluster.log in my case
```


### Nvidia profiler
The nvidia visual profiler can be useful to get similar results for comparison,
but it was not relied on considering the cluster interactions are through TUI.

```shell
# the profiler should be installed by default with the nvidia toolkit
# install java if not already installed
sudo apt install openjdk-8-jre
nvvp # start the profiler
```

[for more info](https://docs.nvidia.com/cuda/profiler-users-guide/index.html)

