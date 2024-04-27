/*
get info from logs to be displayed by python
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// read timing logs and determine average, min, max and troughput

char inputs[4][256] = {"logs/coutput-O0.log", "logs/coutput-O1.log", "logs/coutput-O2.log", "logs/coutput-O3.log"};
char outputs[4][256] = {"logs/timings-O0.log", "logs/timings-O1.log", "logs/timings-O2.log", "logs/timings-O3.log"};
char bw_out[4][256] = {"logs/bandwidths-O0.log", "logs/bandwidths-O1.log", "logs/bandwidths-O2.log", "logs/bandwidths-O3.log"};

int readTimingLogs(const char* cinput, const char* coutput, const char* output_bw);
int calcBandwidth(int size, int blocks, float time, const char* output_bw);

int main(int argc, char* argv[]) {
    for(int i = 0; i < 4; i++){
        FILE* bw_file = fopen(bw_out[i], "w");
        if(bw_file == NULL){
            printf("Error opening BW file\n");
            return 1;
        }
        fclose(bw_file);
        readTimingLogs(inputs[i], outputs[i], bw_out[i]);
    }
    return 0;
}

int readTimingLogs(const char* cinput, const char* coutput, const char* output_bw){
    FILE* readFile = fopen(cinput, "r");
    if(readFile == NULL){
        printf("Error opening input file\n");
        return 1;
    }
    FILE* writeFile = fopen(coutput, "w"); //write from the beginning
    if(writeFile == NULL){
        printf("Error opening output file\n");
        return 2;
    }
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
        // if(line[0] == 's'){ 
        //     continue;
        // }
        sscanf(line, "%d, %f, %d", &curr_size, &curr_time, &curr_blocks);

        //if done with current size block combination
        // write to file at last iteration
        if(((curr_size != prev_size) || (curr_blocks != prev_blocks)) && prev_size != 0){
            // write to file
            if(iter > 0){
                avg_time = total_time / iter;
            }
            fprintf(writeFile, "%d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
            calcBandwidth(prev_size, prev_blocks, avg_time, output_bw);
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
    //print last iteration to file
    fprintf(writeFile, "%d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
    calcBandwidth(prev_size, prev_blocks, avg_time, output_bw);        
    fclose(readFile);
    fclose(writeFile);
    return 0;
}

int calcBandwidth(int size,int blocks, float time, const char* output_bw){
    FILE* bw_file = fopen(output_bw, "a");
    if(bw_file == NULL){
        printf("Error opening BW file\n");
        return 1;
    }
    float eff_bw =  ( 2 * (size*size*sizeof(int)) / time) / (float)(1024*1024*1024);
    fprintf(bw_file, "%d, %d, %f\n", size, blocks, eff_bw);
    fclose(bw_file);
    return 0;
}