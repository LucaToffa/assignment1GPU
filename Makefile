CC = g++
CPPFLAGS = -g -std=c++11
BINS = main testsimple testblock analyser

all: $(BINS)

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


clearvalgrind:
	rm -rf cachegrind.*

clean:
	rm -rf build/* \
	rm *.o $(BINS) cachegrind.* *.log