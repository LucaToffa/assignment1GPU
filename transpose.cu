#include <stdio.h>
#include <cuda.h>

#define DEFAULT_SIZE 32
//#define DEBUG
#ifdef DEBUG
    #define PRINTF(...) printf(__VA_ARGS__)
#else
    #define PRINTF(...)
#endif
//#define PRINT
#ifndef TILE_SIZE
    #define TILE_SIZE 32 
#endif
#ifndef BLOCK_ROWS
    #define BLOCK_ROWS 8 //works up to 16
#endif
#define TRANSPOSITIONS 100

//i think there is a problem with the matrix allocation
//try managed memory

int initMatrix(float* mat, int size);
int printMatrix(float* mat, int size);
int testTranspose(float* mat, float* mt, int size);
int block_benchmark(uint N);
int basic_benchmark(uint N);
int conflict_benchmark(uint N);

//implementation of block transpose in gpu
//each kernel is a block?
//decoupling tile size in shares memory and block size not possible
__global__ void block_transpose(float *input, float *output){
    __shared__ float tile[TILE_SIZE][TILE_SIZE+1];
    
    //input to shared offsets
    int x = blockIdx.x * TILE_SIZE + threadIdx.x;
    int y = blockIdx.y * TILE_SIZE + threadIdx.y;
    int w = gridDim.x * TILE_SIZE;

    for(int i = 0; i < TILE_SIZE; i += BLOCK_ROWS){
        tile[threadIdx.y+i][threadIdx.x] = input[(y+i) * w + x];
    }

    __syncthreads();

    //shared to output offsets
    x = blockIdx.y * TILE_SIZE + threadIdx.x;
    y = blockIdx.x * TILE_SIZE + threadIdx.y;

    for(int j = 0; j < TILE_SIZE; j += BLOCK_ROWS){
        output[(y+j) * w + x] = tile[threadIdx.x][threadIdx.y+j];
    }


}

//without the +1 the memory access conflicts cannot be avoided
__global__ void conflict_transpose(float *input, float *output){
    __shared__ float tile[TILE_SIZE][TILE_SIZE];
    
    //input to shared offsets
    int x = blockIdx.x * TILE_SIZE + threadIdx.x;
    int y = blockIdx.y * TILE_SIZE + threadIdx.y;
    int w = gridDim.x * TILE_SIZE;

    for(int i = 0; i < TILE_SIZE; i += BLOCK_ROWS){
        tile[threadIdx.y+i][threadIdx.x] = input[(y+i) * w + x];
    }

    __syncthreads();

    //shared to output offsets
    x = blockIdx.y * TILE_SIZE + threadIdx.x;
    y = blockIdx.x * TILE_SIZE + threadIdx.y;

    for(int j = 0; j < TILE_SIZE; j += BLOCK_ROWS){
        output[(y+j) * w + x] = tile[threadIdx.x][threadIdx.y+j];
    }

}

#define B_TILE TILE_SIZE
#define B_ROWS BLOCK_ROWS
// implementation of basic transpose in gpu
// to avoid ifs in the kernel, check the matrix size and derive block/threads size
__global__ void basic_transpose(float *input, float *output, int N){
    //matrix transpose that works for any size
    int x = blockIdx.x * B_TILE + threadIdx.x;
    int y = blockIdx.y * B_TILE + threadIdx.y;

    int index_in = x + N * y;
    int index_out = y + N * x;

    for (int i = 0; i < B_TILE; i += B_ROWS){
        output[index_out + i] = input[index_in + i * N];
    }
}

int main(int argc, char* argv[]){
#ifdef DEBUG
    if (argc > 1){
        printf("argc = %d:\n", argc);
        for(int i = 0; i < argc; i++){
            printf("arg %d : %s\n", i+1, argv[i]);
        }
        printf("\n");
    }
    
#endif
    bool swipe = false;
    uint N = DEFAULT_SIZE;
    if(argc >= 2){
        N = (1<<atoi(argv[1]));
        PRINTF("N changed: %d\n", N);
        printf("N: %d, T: %d, B: %d \n", N, TILE_SIZE, BLOCK_ROWS);
    }else{
        swipe = true;
        //log shape of data
        printf("#T: %d, B: %d#\n", TILE_SIZE, BLOCK_ROWS);
        printf("#N, OpTime, Op-GB/s, KTime, K-GB/s (basic, conflcit, block)#\n");
    }
    if(BLOCK_ROWS > TILE_SIZE){
        printf("Error: BLOCK_ROWS > TILE_SIZE\n");
        return -1;

    }

    // int mem_size = N * N * sizeof(float);
    // PRINTF("Memory size: %d\n", mem_size);
    // //init the matrix to transpose in gpu
    // float* mat = (float*) malloc(mem_size);

    // float* mat_t = (float*) malloc(mem_size);//for some reason the gpu segfaults if i dont maccoc in the function
    // memset(mat_t, 0, mem_size); 

    // initMatrix(mat, N);
    // printMatrix(mat, N);

    /*
    everything gpu related runs in these functions, a bit repetitive 
    but i dont wont to pass around that many parameters
    */
    do{
        PRINTF("N: ");
        printf("%d, ", N);
        basic_benchmark(N);
        conflict_benchmark(N);
        block_benchmark(N);
        N *= 2;
    }while(swipe && N < (2<<13)); //2<<14 = 16384

    //dealloc local memory memory
    // free(mat);
    // free(mat_t);
    PRINTF("\n");
    return 0;
}


int initMatrix(float* mat, int size){
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            mat[i + j*size] = (i*2+j)%(100);
        }
    }
    return 0;

}

int printMatrix(float* mat, int size){
#ifdef PRINT
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            printf("%2.2f ", mat[i + j*size]);
        }
        printf("\n");
    }
    printf("\n");
#endif
    return 0;
}

int testTranspose(float* mat, float* mat_t, int size){
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            if(mat[i + j*size] != mat_t[j + i*size]){
                printf("Error at mat[%d, %d]\n", i, j);
                return -1;
            }   
        }
    }    
    PRINTF("Matrix transposed without errors\n");    
    return 0;
}


int block_benchmark(uint N){
    //give access to the gpu
    int mem_size = N * N * sizeof(float);
    float* mat = (float*) malloc(mem_size);
    float* mat_t = (float*) malloc(mem_size);
    memset(mat_t, 0, mem_size);
    initMatrix(mat, N);
    float *d_mat, *d_mat_t;
    cudaError_t err;
    //int threads, blocks = 0;
    PRINTF("Allocating memory\n");
    if((err = cudaMalloc((void**)&d_mat, mem_size)) != cudaSuccess){
        printf("Error allocating memory for d_a: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    if((err = cudaMalloc((void**)&d_mat_t, mem_size)) != cudaSuccess){
        printf("Error allocating memory for d_mat_t: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    //cudaMalloc((void**)&d_mat_t, mem_size);
    PRINTF("Memory allocated\n");
    //copy data to gpu
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    if((err = cudaMemcpy(d_mat, mat, N * N * sizeof(int), cudaMemcpyHostToDevice)) != cudaSuccess){
        printf("Error copying data to d_mat: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    PRINTF("Data copied\n");
    //setup grid and block size
    dim3 DimGrid = {N/TILE_SIZE, N/TILE_SIZE, 1};
    dim3 DimBlock = {TILE_SIZE, BLOCK_ROWS, 1};
    
    //call kernel as many times as needed
    //first a dummy kernel
    block_transpose<<<DimGrid, DimBlock>>>(d_mat, d_mat_t);
    cudaEvent_t startK, stopK;
    cudaEventCreate(&startK);
    cudaEventCreate(&stopK);
    cudaEventRecord(startK);
    for(int i = 0; i < TRANSPOSITIONS; i++){
        block_transpose<<<DimGrid, DimBlock>>>(d_mat, d_mat_t);
    }
    cudaEventRecord(stopK);
    cudaEventSynchronize(stopK);
    PRINTF("Kernel returned\n");

    //copy data back
    if((err = cudaMemcpy(mat_t, d_mat_t, mem_size, cudaMemcpyDeviceToHost)) != cudaSuccess){
        printf("Error copying data to mat_t: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    //sync
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaDeviceSynchronize();
    
    float millisecondsK = 0;
    cudaEventElapsedTime(&millisecondsK, startK, stopK);
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float ogbs = 2 * N * N * sizeof(float) * 1e-6 * TRANSPOSITIONS / milliseconds;
    float kgbs = 2 * N * N * sizeof(float) * 1e-6 * TRANSPOSITIONS / millisecondsK;
    PRINTF("Operation Time: %11.2f ms\n", milliseconds);
    PRINTF("Throughput in GB/s: %7.2f\n", ogbs);
    PRINTF("Kernel Time: %11.2f ms\n", millisecondsK);
    PRINTF("Throughput in GB/s: %7.2f\n", kgbs);
    printf("%f, %f, %f, %f\n", milliseconds, ogbs, millisecondsK, kgbs);
    cudaEventDestroy(startK);
    cudaEventDestroy(stopK);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);


    //results
    printMatrix(mat_t, N);

    //test if the matrix is transposed
    testTranspose(mat, mat_t, N);  

    //free gpu resources
    cudaFree(d_mat);
    cudaFree(d_mat_t);
    free(mat);
    free(mat_t);
    return 0;
}

int basic_benchmark(uint N){
    //give access to the gpu
    int mem_size = N * N * sizeof(float);
    float* mat = (float*) malloc(mem_size);
    float* mat_t = (float*) malloc(mem_size);
    memset(mat_t, 0, mem_size);
    initMatrix(mat, N);
    float *d_mat, *d_mat_t;
    cudaError_t err;
    //int threads, blocks = 0;
    PRINTF("Allocating memory\n");
    if((err = cudaMalloc((void**)&d_mat, mem_size)) != cudaSuccess){
        printf("Error allocating memory for d_a: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    if((err = cudaMalloc((void**)&d_mat_t, mem_size)) != cudaSuccess){
        printf("Error allocating memory for d_mat_t: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    //cudaMalloc((void**)&d_mat_t, mem_size);
    PRINTF("Memory allocated\n");

    //copy data to gpu
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    if((err = cudaMemcpy(d_mat, mat, mem_size, cudaMemcpyHostToDevice)) != cudaSuccess){
        printf("Error copying data to d_mat: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    PRINTF("Data copied\n");
    //setup grid and block size
    dim3 gridB(N / B_TILE, N / B_TILE);
    dim3 blockB(B_TILE, B_ROWS);
    
    //call kernel as many times as needed
    //first a dummy kernel
    basic_transpose<<<gridB, blockB>>>(d_mat, d_mat_t, N);
    cudaEvent_t startK, stopK;
    cudaEventCreate(&startK);
    cudaEventCreate(&stopK);
    cudaEventRecord(startK);
    for(int i = 0; i < TRANSPOSITIONS; i++){
        basic_transpose<<<gridB, blockB>>>(d_mat, d_mat_t, N);
    }
    cudaEventRecord(stopK);
    cudaEventSynchronize(stopK);
    PRINTF("Kernel returned\n");

    //copy data back
    if((err = cudaMemcpy(mat_t, d_mat_t, mem_size, cudaMemcpyDeviceToHost)) != cudaSuccess){
        printf("Error copying data to mat_t: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    //sync
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaDeviceSynchronize();
    
    float millisecondsK = 0;
    cudaEventElapsedTime(&millisecondsK, startK, stopK);
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float ogbs = 2 * N * N * sizeof(float) * 1e-6 * TRANSPOSITIONS / milliseconds;
    float kgbs = 2 * N * N * sizeof(float) * 1e-6 * TRANSPOSITIONS / millisecondsK;
    PRINTF("Operation Time: %11.2f ms\n", milliseconds);
    PRINTF("Throughput in GB/s: %7.2f\n", ogbs);
    PRINTF("Kernel Time: %11.2f ms\n", millisecondsK);
    PRINTF("Throughput in GB/s: %7.2f\n", kgbs);
    printf("%f, %f, %f, %f, ", milliseconds, ogbs, millisecondsK, kgbs);

    cudaEventDestroy(startK);
    cudaEventDestroy(stopK);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    //test if the matrix is transposed
    PRINTF("basic results:\n");
    printMatrix(mat_t, N);
    testTranspose(mat, mat_t, N);  

    //reset output matrix
    memset(mat_t, 0, mem_size);
    //cudaMemset(d_mat_t, 0, mem_size);
    cudaFree(d_mat);
    cudaFree(d_mat_t);
    free(mat);
    free(mat_t);
    return 0;
}

int conflict_benchmark(uint N){
    //give access to the gpu
    int mem_size = N * N * sizeof(float);
    float* mat = (float*) malloc(mem_size);
    float* mat_t = (float*) malloc(mem_size);
    memset(mat_t, 0, mem_size);
    initMatrix(mat, N);
    float *d_mat, *d_mat_t;
    cudaError_t err;
    //int threads, blocks = 0;
    PRINTF("Allocating memory\n");
    if((err = cudaMalloc((void**)&d_mat, mem_size)) != cudaSuccess){
        printf("Error allocating memory for d_a: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    if((err = cudaMalloc((void**)&d_mat_t, mem_size)) != cudaSuccess){
        printf("Error allocating memory for d_mat_t: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    //cudaMalloc((void**)&d_mat_t, mem_size);
    PRINTF("Memory allocated\n");
    //copy data to gpu
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    if((err = cudaMemcpy(d_mat, mat, N * N * sizeof(int), cudaMemcpyHostToDevice)) != cudaSuccess){
        printf("Error copying data to d_mat: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    PRINTF("Data copied\n");
    //setup grid and block size
    dim3 DimGrid = {N/TILE_SIZE, N/TILE_SIZE, 1};
    dim3 DimBlock = {TILE_SIZE, BLOCK_ROWS, 1};
    
    //call kernel as many times as needed
    //first a dummy kernel
    conflict_transpose<<<DimGrid, DimBlock>>>(d_mat, d_mat_t);
    cudaEvent_t startK, stopK;
    cudaEventCreate(&startK);
    cudaEventCreate(&stopK);
    cudaEventRecord(startK);
    for(int i = 0; i < TRANSPOSITIONS; i++){
        conflict_transpose<<<DimGrid, DimBlock>>>(d_mat, d_mat_t);
    }
    cudaEventRecord(stopK);
    cudaEventSynchronize(stopK);
    PRINTF("Kernel returned\n");

    //copy data back
    if((err = cudaMemcpy(mat_t, d_mat_t, mem_size, cudaMemcpyDeviceToHost)) != cudaSuccess){
        printf("Error copying data to mat_t: %s\n", cudaGetErrorString(err));
        printf("Line: %d\n", __LINE__);
        return -1;
    }
    //sync
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaDeviceSynchronize();
    
    float millisecondsK = 0;
    cudaEventElapsedTime(&millisecondsK, startK, stopK);
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    PRINTF("Operation Time: %11.2f ms\n", milliseconds);
    float ogbs = 2 * N * N * sizeof(float) * 1e-6 * TRANSPOSITIONS / milliseconds;
    float kgbs = 2 * N * N * sizeof(float) * 1e-6 * TRANSPOSITIONS / millisecondsK;
    PRINTF("Throughput in GB/s: %7.2f\n", ogbs);
    PRINTF("Kernel Time: %11.2f ms\n", millisecondsK);
    PRINTF("Throughput in GB/s: %7.2f\n", kgbs);
    printf("%f, %f, %f, %f, ", milliseconds, ogbs, millisecondsK, kgbs);

    cudaEventDestroy(startK);
    cudaEventDestroy(stopK);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);


    //results
    printMatrix(mat_t, N);

    //test if the matrix is transposed
    testTranspose(mat, mat_t, N);  

    //free gpu resources
    cudaFree(d_mat);
    cudaFree(d_mat_t);
    free(mat);
    free(mat_t);
    return 0;
}