# assignment1GPU

## Analisys of the posible cpeedup in cache usage for different matrix transposition algorithms
## possible optimizations for matrix transposition algorithms in GPU

12|34    13|57
34|56    24|68
----- -> -----
56|78    35|79
78|01    46|80

transposed matrix is allocated and deallocated in the function, if a program wanted to use it, it could be allocated outside and passed as a parameter to the function, or inside the function and returned as a pointer to the transposed matrix.

the c program itself could log everydata to a file, and then the python script could read the file and plot the data.

the 2 versions of transposition algorithms should not run at the same time, as they would interfere with each other, the python script should run the c program twice, one for each algorithm.

also trying with O0 and 03 optimization levels

OPTFLAGS = -O0, -O3, -DDEBUG -DPRINT -DSIMPLE -DBLOCK -> python can mix and match calls to make
### valgrind usage
 valgrind --tool=cachegrind ./sum 10
 valgrind --leak-check=yes myprog arg1 arg2
 --main-stacksize=83886080 ;more stack flag in valgrind
 valgrind --log-file="filename" ./my_program < 1.in && cat filename ; log file flag
 valgrind --tool=cachegrind --log-fd=9 9>>test.log ./main 7 ;append log instead of just writing it

### cachegrind output
parsing and plotting the output of cachegrind may be a pain

time to log all data from valgrind for 1 iter: 
real    9m22,059s | real    9m25,435s at exp=14
real    3m33,988s at exp=13
real    1m10,592s at exp=12
x50 iterations at 14 = ~8h
x50 iterations at 13 = ~2.5h -> do this, but only x30
so 30 iterations at 13 = ~1.5h

before that check that that is the exact data i need

exp 13 instead of 14 means 800 less data also 30 iterations instead of 50
x-800 / 50 * 30 = y
7704-800 / 50 * 30 = 4142,4

!oops i need the data for -01 and -02 too

### help with regex:
https://regex101.com/

### valgrind output
for each iteration, output to 2 tmp files, append to same file regex and main_args, then delete tmp files 

!!why 32 instead of 128?? range(1, 6) in valgrind tests



--output of parsing coutput should include block=0 for simple transposition
--output of parsing voutput should build the data size, block ,mrx4 directly
vfiles can then be appended to cfiles from analyser, and then the whole file can be plotted