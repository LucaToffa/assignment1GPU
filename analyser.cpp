/*
get info from logs to be displayed by python
*/

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

// read timing logs
// size time blocks
int readTimingLogs(const char* cinput, const char* coutput){
    FILE* readFile = fopen(cinput, "r");
    if(readFile == NULL){
        printf("Error opening file\n");
        return 1;
    }
    FILE* writeFile = fopen(coutput, "w"); //write from the beginning
    char line[256];
    int curr_size, curr_blocks = 0;
    int prev_size = 0; 
    float curr_time;
    int prev_blocks = 0;
    float avg_time = 0;
    float total_time = 0;
    float min_time = 1000000.0;
    float max_time = 0;
    int iter = 0;
    while(fgets(line, sizeof(line), readFile)){
        if(line[0] == 's'){ 
            continue;
        }
        sscanf(line, "%d, %f, %d", &curr_size, &curr_time, &curr_blocks);

        //if done with current size block combination
        // write to file at last iteration
        if(((curr_size != prev_size) || (curr_blocks != prev_blocks)) && prev_size != 0){
            // write to file
            if(iter > 0){
                avg_time = total_time / iter;
            }
            fprintf(writeFile, "%d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
    
            // reset values
            iter = 0;
            total_time = 0;
            min_time = 1000000.0;
            max_time = 0.0;
        }
        
        
        prev_size = curr_size;
        prev_blocks = curr_blocks;
        total_time = total_time + curr_time;
        // compute min and max
        if(curr_time < min_time){
            min_time = curr_time;
        }   
        if(curr_time > max_time){
            max_time = curr_time;
        }
        iter++;    
    }
    //print last iteration 
    fprintf(writeFile, "%d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
            
    fclose(readFile);
    fclose(writeFile);
    return 0;
}

int main(int argc, char* argv[]) {
    readTimingLogs("logs/coutput-O0.log", "logs/timings-O0.log");
    readTimingLogs("logs/coutput-O1.log", "logs/timings-O1.log");
    readTimingLogs("logs/coutput-O2.log", "logs/timings-O2.log");
    readTimingLogs("logs/coutput-O3.log", "logs/timings-O3.log");
    return 0;
}
