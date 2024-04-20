#include <iostream>
#include <cmath>
#include <ctime>

#define DEFAULT_SIZE 4
//#define DEBUG
//#define PRINT 

/*
example of csv like output:
opt, type, size, testiter, time 
*/
int initMatrix(int** mat, int size);
int printMatrix(int** mat, int size);

int SimpleTraspose(int** mat, int size);
int BlockTraspose(int** mat, int size, int blocks = 1);

int main(int argc, char* argv[]) {
#ifdef DEBUG
    if (argc > 1){
        for(int i = 0; i < argc; i++){
            printf("arg %d : %s\n", i+1, argv[i]);
        }
        printf("\n");
    }
#endif
    int N;
    int B;
    if(argc >= 2){
        N = (int) pow(2,atoi(argv[1])); //what if is not an integer?
        if(argc == 3) B = atoi(argv[2]);
    }else{
        N = DEFAULT_SIZE; //deafult dimension
    }
#ifdef DEBUG
    printf("Matrix size: %d, ", N);
#else
    printf("%d, ", N);
#endif
    int** mat = (int**) malloc(N * sizeof(int*));
    for(int i = 0; i < N; i++){
        mat[i] = (int*) malloc(N * sizeof(int));
    }

    initMatrix(mat, N);
    printMatrix(mat, N);

#ifdef SIMPLE
    SimpleTraspose(mat, N);
#endif
#ifdef BLOCK
    BlockTraspose(mat, N, B);
#endif

    for(int i = 0; i < N; i++){
        free(mat[i]);
    }
    free(mat);
    printf("\n");
    return 0;
}

int initMatrix(int** mat, int size){
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            mat[i][j] = (i*2+j)%(100);
        }
    }
    return 0;

}

int printMatrix(int** mat, int size){
#ifdef PRINT
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            printf("%2d ", mat[i][j]);
        }
        printf("\n");
    }
    printf("\n");
#endif
    return 0;
}

int SimpleTraspose(int** mat, int size){
    int** trasposed = (int**) malloc(size * sizeof(int*));
    for(int i = 0; i < size; i++){
        trasposed[i] = (int*) malloc(size * sizeof(int));
    }

    double start = clock();
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            trasposed[j][i] = mat[i][j];
        }
    }
    double end = clock(); 
#ifdef DEBUG
    printf("Simple traspose time: %f", (double)(end - start) / CLOCKS_PER_SEC);
#else
    printf("%f", (double)(end - start) / CLOCKS_PER_SEC);
#endif
    printMatrix(trasposed, size);


    for(int i = 0; i < size; i++){
        free(trasposed[i]);
    } 
    free(trasposed);

    return 0;
}

int BlockTraspose(int** mat, int size, int blocks){
    int** trasposed = (int**) malloc(size * sizeof(int*));
    for(int i = 0; i < size; i++){
        trasposed[i] = (int*) malloc(size * sizeof(int));
    }

    int blockSize = blocks;
    if(blockSize < 1 || blockSize > size) blockSize = 1;
    double start = clock();
    //block transpose 
    for(int i = 0; i < size; i+=blockSize){
        for(int j = 0; j < size; j+=blockSize){
            for(int k = i; k < i+blockSize; k++){
                for(int l = j; l < j+blockSize; l++){
                    trasposed[l][k] = mat[k][l];
                }
            }
        }
    }
    double end = clock();
#ifdef DEBUG
    printf("Block traspose time: %f, ", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Block size: %d", blockSize); //down here for log legibility
#else
    printf("%f, %d", (double)(end - start) / CLOCKS_PER_SEC, blockSize);
#endif
    printMatrix(trasposed, size);

    for(int i = 0; i < size; i++){
        free(trasposed[i]);
    } 
    free(trasposed);
    return 0;
}