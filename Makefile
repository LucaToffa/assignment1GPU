CC = g++
CPPFLAGS = -g -std=c++11 #-Wall -Wpedantic -Wextra
#OPTFLAGS = -Wunused-parameter -Wunused-variable #used to pass args ex. make OPTFLAGS=-DPRINT all
all: main

main: main.o
	$(CC) $(CPPFLAGS) $(OPTFLAGS) build/main.o -o main
main.o: main.cpp
	$(CC) $(CPPFLAGS) $(OPTFLAGS) -c main.cpp -o build/main.o

build: main.cpp
	$(CC) $(CPPFLAGS) -DPRINT -DSIMPLE -DDEBUG main.cpp -o main
setup:
	mkdir logs build \
	& touch README.md
clean:
	rm -rf build/* \
	rm *.o main cachegrind.*

clearlogs:
	rm -rf logs/*