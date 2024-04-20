CC = g++
CPPFLAGS = -g #-std=c++11 -Wall -Wpedantic -Wextra
BINS = main testsimple testblock
#OPTFLAGS = -Wunused-parameter -Wunused-variable #used to pass args ex. make OPTFLAGS=-DPRINT all
all: main

testsimple: main.cpp
	$(CC) $(CPPFLAGS) -DDEBUG -DSIMPLE main.cpp -o testsimple
testblock: main.cpp
	$(CC) $(CPPFLAGS) -DDEBUG -DBLOCK main.cpp -o testblock
	
main: main.o
	$(CC) $(CPPFLAGS) $(OPTFLAGS) build/main.o -o main
main.o: main.cpp
	$(CC) $(CPPFLAGS) $(OPTFLAGS) -c main.cpp -o build/main.o

build: main.cpp
	$(CC) $(CPPFLAGS) -DPRINT -DSIMPLE -DDEBUG main.cpp -o main

analyser: analyser.cpp
	$(CC) $(CPPFLAGS) analyser.cpp -o analyser
	
valgrind_simple: testsimple
	valgrind --tool=cachegrind ./testsimple $(ARGS)
valgrind_block: testblock
	valgrind --tool=cachegrind ./testblock $(ARGS)
setup:
	mkdir logs build \
	& touch README.md
clean:
	rm -rf build/* \
	rm *.o $(BINS) cachegrind.*

clearlogs:
	rm -rf logs/* cachegrind.*