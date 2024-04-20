/*
get info from logs to be displayed by python
*/

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

#define CINPUT "tests/couttest.log"
#define VINPUT "tests/vouttest.log"
#define COUTPUT "tests/datapoints.log"
#define VOUTPUT "tests/vdatapoints.log"
// read timing logs
// size time blocks
int readTimingLogs(){
    FILE* readFile = fopen(CINPUT, "r");
    if(readFile == NULL){
        printf("Error opening file\n");
        return 1;
    }
    FILE* writeFile = fopen(COUTPUT, "w"); //write from the beginning
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
        printf("%d, %f, %d\n", curr_size, curr_time, curr_blocks);

        // wait for input to continue
        getchar();
        //if done with current size block combination
        // write to file at last iteration
        if(((curr_size != prev_size) || (curr_blocks != prev_blocks)) && prev_size != 0){ // && prev_size != 0
            // write to file
            if(iter > 0){
                avg_time = total_time / iter;
            }
            printf("writing to file %d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
                
            if(curr_blocks > 0){
                //printf("writing to file %d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
                fprintf(writeFile, "%d, %d, %f, %f, %f\n", prev_size, prev_blocks, avg_time, min_time, max_time);
            }else{
                fprintf(writeFile, "%d, %f, %f, %f\n", prev_size, avg_time, min_time, max_time);
            }
    
            // reset values
            iter = 0;
            //prev_size = curr_size;
            //prev_blocks = curr_blocks;
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

    fclose(readFile);
    fclose(writeFile);
    return 0;
}
//#I1m LLim I1mr LLimr D1m LLdm D1mr LLdmr LLm LLmr
//2,237 2,130 0.10 0.09 14,558 9,242 1.9 1.2 11,372 0.4
int readMissRates(){
    FILE* readFile = fopen(VINPUT, "r");
    if(readFile == NULL){
        printf("Error opening file\n");
        return 1;
    }
    FILE* writeFile = fopen(VOUTPUT, "w"); //write from the beginning
    char line[256];
    float I1mr, LLimr, D1mr, LLdmr, LLmr; 
    float miss_rates[5] = {0}; 
    int iter = 0;
    while(fgets(line, sizeof(line), readFile)){
        if(line[0] == 's'){ 
            continue;
        }
        if(line[0] == '\n'){
            // write to file
            fprintf(writeFile, "%f, %f, %f, %f, %f\n", miss_rates[0], miss_rates[1], miss_rates[2], miss_rates[3], miss_rates[4]);
            continue;
        }
        strtok(line, " ");
        strtok(NULL, " ");
        I1mr = atof(strtok(NULL, " "));
        LLimr = atof(strtok(NULL, " "));
        strtok(NULL, " ");
        strtok(NULL, " ");
        D1mr = atof(strtok(NULL, " "));
        LLdmr = atof(strtok(NULL, " "));
        strtok(NULL, " ");
        LLmr = atof(strtok(NULL, " "));
        
        
        printf("%f %f %f %f %f\n", I1mr, LLimr, D1mr, LLdmr, LLmr);

        // wait for input to continue
        getchar();
    }
    return 0;

}
int main(int argc, char* argv[]) {
    //readTimingLogs();
    readMissRates();
    return 0;
}
/*
int main(int argc, char* argv[]) {
    int size, blocks;
    float time;
    std::ifstream readFile("logs/coutput.log");
    std::string line;

    while(getline(readFile,line)){
        if(line[0] == 's'){ 
            continue;
        }
        std::getline(line, size, ',');
        std::getline(line, time, ',');
        std::getline(line, blocks, '\n');
        printf("%s\n", line.c_str());
    }


// for each line make a dictionary with the values, compute average among each matrix and block size 
// discard outliers may be needed?

// better to do everything in c style


    readFile.close();
    return 0;
}

*/
