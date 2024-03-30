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