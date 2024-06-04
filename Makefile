CC = g++
CPPFLAGS = -g -std=c++11
BINS = testsimple testblock analyser transpose
T = 32
B = 8

all: setup clean $(BINS)

main: main.o
	$(CC) $(CPPFLAGS) $(OPTFLAGS) build/main.o -o main
main.o: main.cpp
	$(CC) $(CPPFLAGS) $(OPTFLAGS) -c main.cpp -o build/main.o

testsimple: main.cpp
	$(CC) $(CPPFLAGS) -O0 -DDEBUG -DSIMPLE main.cpp -o testsimple
testblock: main.cpp
	$(CC) $(CPPFLAGS) -O0 -DDEBUG -DBLOCK main.cpp -o testblock
build: main.cpp
	$(CC) $(CPPFLAGS) -O0 -DPRINT -DSIMPLE -DDEBUG main.cpp -o main
analyser: analyser.cpp	
	$(CC) $(CPPFLAGS) analyser.cpp -o analyser


valgrind_simple: testsimple
	valgrind --tool=cachegrind ./testsimple $(ARGS)
valgrind_block: testblock
	valgrind --tool=cachegrind ./testblock $(ARGS)

setup:
	mkdir -p build
	mkdir -p logs logs2
	mkdir -p plots plots2

clearvalgrind:
	rm -rf cachegrind.*

.PHONY: clean cudarun
cudarun: transpose
	@nvidia-optimus-offload-glx ./transpose $(N)
transpose: transpose.cu
	@nvcc -DTILE_SIZE=$(T) -DBLOCK_ROWS=$(B) transpose.cu -o transpose
transpose-cluster: transpose.cu
	nvcc -DTILE_SIZE=$(T) -DBLOCK_ROWS=$(B) transpose.cu -o transpose$(T)$(B)
clean:
	rm -rf build/* \
	rm *.o $(BINS) main transpose cachegrind.* *.log