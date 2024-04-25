import matplotlib.pyplot as plt

import numpy as np
import math

MAX_ESP = 13
input_prefix = "logs/" #where does data come from
output_prefix = "plots/" #where to save images
def multibar(): #test to understand how to plot multiple bars
    # data
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = range(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    # plot
    p1 = plt.bar(ind, menMeans, width, yerr=menStd, label='hello')
    p2 = plt.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd, label='world')
    plt.ylabel('Scores')
    plt.title('Scores by group')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.legend()
    plt.show()

def openfile():
    with open("data.txt", "r") as dataset:
        #check if line starts with a number
        datalist  = [line.split(', ') for line in dataset.readlines()]
                     
    #print(datalist)
    for data in datalist:
        print(data)
    #convert list of strings to list of floats
    for i in range(len(datalist)):
        datalist[i] = [float(j) for j in datalist[i]]
    # fill x, y and y_err with data
    x = []
    y = []
    y_err = []
    for data in datalist:
        if(data[1] == 0):
            x.append(int(data[0]))
            y.append(data[2])
            y_err.append((float(data[4]) - float(data[3]) + 0.000001) / 2)
        
    print(x)
    print(y)
    plt.plot(x, y)
    plt.errorbar(x, y, yerr=y_err, fmt='o', elinewidth=2, alpha=0.8)
    plt.xlabel('Matrix Size')
    plt.ylabel('Time (seconds)')
    plt.title('Benchmark times for simple matxices')
    plt.grid(True)
    #plt.legend()
    plt.show()   

def plotTotCacheMiss(): #4
    # B mrx N <= N, B, I1mr, LLimr, D1mr, LLdmr, LLmr
    iter = 0
    outputs = ["totCacheMiss-O0.png", "totCacheMiss-O1.png", "totCacheMiss-O2.png", "totCacheMiss-O3.png"]
    for file in ["foutput-O0.log", "foutput-O1.log", "foutput-O2.log", "foutput-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            datalist  = [line.split(', ') for line in dataset.readlines()]

        for i in range(2, MAX_ESP):#datalist: #this is wrong, need to fix
            #while data[1] does not change from previous value, keep adding to the list
            data = datalist[i]
            x = []
            y = []
            for j in range(len(datalist)):
                if(data[0] == datalist[j][0]):
                    x.append(datalist[j][1])
                    y.append(float(datalist[j][4]))
            #add this line to the legend
            plt.plot(x, y, label=str(data[0]))
        plt.xlabel('Block Size')
        plt.ylabel('Total Cache Misses')
        plt.title('Benchmark times for block matrices')
        plt.grid(True)
        plt.legend()
        plt.savefig(output_prefix + outputs[iter])
        iter = iter + 1
        plt.show() 

def plotSimpleBandwidth(): #6
    # N BW <= N, B, 0.00
    iter = 0
    output = "simpleBandwidths.png"
    for file in ["bandwidths-O0.log", "bandwidths-O1.log", "bandwidths-O2.log", "bandwidths-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            datalist  = [line.split(', ') for line in dataset.readlines()]
            x = []
            y = []
            for j in range(MAX_ESP):
                #for i in range(len(datalist)):
                if(int(datalist[j][1]) == 0):
                    x.append(datalist[j][0])
                    y.append(float(datalist[j][2]))
            plt.plot(x, y, label=file)
    plt.xlabel('Matrix Size')   
    plt.ylabel('Bandwidth')
    plt.title('Benchmark times for simple matrices')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_prefix + output)
    iter = iter + 1
    plt.show()

def plotBWspace(): #8
    # N BW <= N, B, 0.00
    iter = 0
    outputs = ["blockBandwidths-O0.png", "blockBandwidths-O1.png", "blockBandwidths-O2.png", "blockBandwidths-O3.png"]
    for file in ["bandwidths-O0.log", "bandwidths-O1.log", "bandwidths-O2.log", "bandwidths-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            size = ['2', '4', '8', '16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192']
            block = ['0', '1', '2', '4', '8', '16', '32', '64', '128']
            z = [[-1] * len(block) for _ in range(len(size))]
            for line in dataset:
                values = line.strip().split(', ')
                size_in = int(values[0])
                block_in = int(values[1])
                val = float(values[2])

                size_pow = int(math.log2(size_in) - 1) #zero index = size 2
                if(block_in == 0):
                    block_pow = 0
                    z[size_pow][1] = val
                else:
                    block_pow = int(math.log2(block_in) + 1)

                z[size_pow][block_pow] = val

        fig, ax = plt.subplots()
        im = ax.imshow(z)

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(len(block)), labels=block)
        ax.set_yticks(np.arange(len(size)), labels=size)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")

        for i in range(len(size)):
            for j in range(len(block)):
                text = ax.text(j, i, round(z[i][j], 1),
                            ha="center", va="center", color="w")

        ax.set_title("Bandwidth of matrices (in GB/s)")
        fig.tight_layout()
        #save plot bigger size

        plt.gcf().set_size_inches(5, 6)
        plt.savefig(output_prefix + outputs[iter])
        iter = iter + 1
        plt.show()

def plotBlockBandwidth(): #7
    # N BW <= N, B, 0.00
    iter = 0
    output = "blockBandwidths.png"
    for file in ["bandwidths-O0.log", "bandwidths-O1.log", "bandwidths-O2.log", "bandwidths-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            datalist  = [line.split(', ') for line in dataset.readlines()]
            x = []
            y = []

            for j in range(len(datalist)):
                #for i in range(len(datalist)):
                if(int(datalist[j][0]) == 4096):
                    x.append(datalist[j][1])
                    y.append(float(datalist[j][2]))
            plt.plot(x, y, label=file + " 4096")

            # x = []
            # y = []
            # for j in range(len(datalist)):
            #     #for i in range(len(datalist)):
            #     if(int(datalist[j][0]) == 512):
            #         x.append(datalist[j][1])
            #         y.append(float(datalist[j][2]))
            # plt.plot(x, y, label=file + " 512")
        
            # x = []
            # y = []
            # for j in range(len(datalist)):
            #     #for i in range(len(datalist)):
            #     if(int(datalist[j][0]) == 16):
            #         x.append(datalist[j][1])
            #         y.append(float(datalist[j][2]))
            # plt.plot(x, y, label=file + " 16")

    plt.xlabel('Block Size')
    plt.ylabel('Bandwidth')
    plt.title('Benchmark times for block matrices')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_prefix + output)
    iter = iter + 1
    plt.show()


def plotBlockCacheMisses(): #5
    # (N fixed 4096) B mrx <= N, B, 0.00, 0.00, 36.9, 32.5, 10.1
    iter = 0
    outputs = ["blockCacheMisses-O0.png", "blockCacheMisses-O1.png", "blockCacheMisses-O2.png", "blockCacheMisses-O3.png"]
    for file in ["foutput-O0.log", "foutput-O1.log", "foutput-O2.log", "foutput-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            #check if line starts with a number
            datalist  = [line.split(', ') for line in dataset.readlines()]
            
        #convert list of strings to list of floats
        # for i in range(len(datalist)):
        #     datalist[i] = [float(j) for j in datalist[i]]
        #     datalist[i][0] = str(datalist[i][0])

        #for data in datalist:
        #for d in range(2):#datalist: #this is wrong, need to fix
            #while data[1] does not change from previous value, keep adding to the list
        #data = datalist[d]
        x = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        for i in range(len(datalist)):
                if(int(datalist[i][0]) == 8192):
                    x.append(datalist[i][1])
                    y1.append(float(datalist[i][2]))
                    y2.append(float(datalist[i][3]))
                    y3.append(float(datalist[i][4]))
                    y4.append(float(datalist[i][5]))
        plt.plot(x, y1, label='I1mr') #y1 = y2
        plt.plot(x, y2, label='LLimr')
        plt.plot(x, y3, label='D1mr')
        plt.plot(x, y4, label='LLdmr')
        plt.yscale('linear')
        plt.xlabel('Block Size')
        plt.ylabel('Cache miss rates')
        plt.title('Benchmark times for block matxices')
        plt.grid(True)
        plt.legend()
        plt.savefig(output_prefix + outputs[iter])
        iter = iter + 1
        plt.show()   
    
def plotSimpleCacheMiss(): #2
    # N mrx <= N, B, I1mr, LLimr, D1mr, LLdmr, LLmr
    iter = 0
    outputs = ["simpleCacheMisses-O0.png", "simpleCacheMisses-O1.png", "simpleCacheMisses-O2.png", "simpleCacheMisses-O3.png"]
    for file in ["foutput-O0.log", "foutput-O1.log", "foutput-O2.log", "foutput-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            #check if line starts with a number
            datalist  = [line.split(', ') for line in dataset.readlines()]
        x = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        for i in range(len(datalist)):
                if(datalist[i][1] == '0' and int(datalist[i][0]) < 1024 and int(datalist[i][0]) > 4):
                    x.append(datalist[i][0])
                    y1.append(float(datalist[i][2]))
                    y2.append(float(datalist[i][3]))
                    y3.append(float(datalist[i][4]))
                    y4.append(float(datalist[i][5]))
        plt.yscale('linear')
        plt.plot(x, y1, label='I1mr')
        plt.plot(x, y2, label='LLimr')
        plt.plot(x, y3, label='D1mr')
        plt.plot(x, y4, label='LLdmr')
        plt.xlabel('Matrix Size')
        plt.ylabel('Cache miss rates')
        plt.title('Benchmark Cache for simple matrices')
        plt.grid(True)
        plt.legend()
        plt.savefig(output_prefix + outputs[iter])
        iter = iter + 1
        plt.show()

def plotblocktimeNormalized(): #9
    iter = 0
    outputs = ["blocktimeNorm-O0.png", "blocktimeNorm-O1.png", "blocktimeNorm-O2.png", "blocktimeNorm-O3.png"]
    for file in ["timings-O0.log", "timings-O1.log", "timings-O2.log", "timings-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            datalist  = [line.split(', ') for line in dataset.readlines()]

        for i in range(MAX_ESP):
            #while data[1] does not change from previous value, keep adding to the list
            x = []
            y = []
            y_err = []
            for data in datalist:
                if(data[0] == datalist[i][0] ): #and data[1] != '0'
                        x.append(data[1])
                        y.append(float(data[2]) * ((MAX_ESP-i)**2))
                        y_err.append((float(data[4]) - float(data[3]) + 0.000001) / 2 / math.sqrt(float(data[0])))
            plt.yscale('linear')
            plt.plot(x, y, label=datalist[i][0])
            plt.errorbar(x, y, yerr=y_err, fmt='o', elinewidth=2, alpha=0.8)
        my_xticks = x
        plt.xticks(x, my_xticks)
        plt.xlabel('Block Size')
        plt.ylabel('Normalized Time')
        plt.title('Benchmark times for block matrices')
        plt.grid(True)
        plt.legend()
        plt.savefig(output_prefix + outputs[iter])
        iter = iter + 1
        plt.show()  

def plotblocktime(): #3
    iter = 0
    outputs = ["blocktime-O0.png", "blocktime-O1.png", "blocktime-O2.png", "blocktime-O3.png"]
    for file in ["timings-O0.log", "timings-O1.log", "timings-O2.log", "timings-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            datalist  = [line.split(', ') for line in dataset.readlines()]

        for i in range(MAX_ESP):
            #while data[1] does not change from previous value, keep adding to the list
            x = []
            y = []
            y_err = []
            for data in datalist:
                if(data[0] == datalist[i][0] ): #and data[1] != '0'
                        x.append(data[1])
                        y.append(float(data[2]))
                        y_err.append((float(data[4]) - float(data[3]) + 0.000001) / 2 / math.sqrt(float(data[0])))
            plt.yscale('linear')
            plt.plot(x, y, label=datalist[i][0])
            plt.errorbar(x, y, yerr=y_err, fmt='o', elinewidth=2, alpha=0.8)
        my_xticks = x
        plt.xticks(x, my_xticks)
        plt.xlabel('Block Size')
        plt.ylabel('Time (seconds)')
        plt.title('Benchmark times for block matrices')
        plt.grid(True)
        plt.legend()
        plt.savefig(output_prefix + outputs[iter])
        iter = iter + 1
        plt.show()

def plotsimpletimelog(): #10
    iter = 0
    output = "simpletimelog.png"
    for file in ["timings-O0.log", "timings-O1.log", "timings-O2.log", "timings-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            #check if line starts with a number
            datalist  = [line.split(', ') for line in dataset.readlines()]

        x = []
        y = []
        y_err = []
        for data in datalist:
            if(data[1] == '0' and int(data[0]) > 1):
                x.append(data[0])
                y.append(float(data[2]))
                y_err.append((float(data[4]) - float(data[3]) + 0.000001) / 2 / math.sqrt(float(data[0])))
        plt.yscale('log')
        plt.plot(x, y, label=file)
    plt.errorbar(x, y, yerr=y_err, fmt='o', elinewidth=2, alpha=0.8)
    plt.xlabel('Matrix Size')
    plt.ylabel('Time (seconds)')
    plt.title('Benchmark times for simple matxices')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_prefix + output)
    iter = iter + 1
    plt.show()

def plotsimpletime(): #1 this is the shape for simple/time data
    iter = 0
    output = "simpletime.png"
    for file in ["timings-O0.log", "timings-O1.log", "timings-O2.log", "timings-O3.log"]:
        with open(input_prefix + file, "r") as dataset:
            #check if line starts with a number
            datalist  = [line.split(', ') for line in dataset.readlines()]

        x = []
        y = []
        y_err = []
        for data in datalist:
            if(data[1] == '0' and int(data[0])< 1024):
                x.append(data[0])
                y.append(float(data[2]))
                y_err.append((float(data[4]) - float(data[3]) + 0.000001) / 2 / math.sqrt(float(data[0])))
        plt.yscale('linear')
        plt.plot(x, y, label=file)
    plt.errorbar(x, y, yerr=y_err, fmt='o', elinewidth=2, alpha=0.8)
    plt.xlabel('Matrix Size')
    plt.ylabel('Time (seconds)')
    plt.title('Benchmark times for simple matxices')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_prefix + output)
    iter = iter + 1
    plt.show()


def errplot():
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 16]
    y_err = [0.1, 0.2, 0.1, 0.3]
    plt.plot(x, y)
    plt.plot(x, y_err)
    #plt.errorbar(x, y, yerr=y_err, fmt='none', elinewidth=2, alpha=0.8)
    plt.show()

if __name__ == "__main__":
    #plotsimpletime() #1
    plotsimpletimelog() #10
    # plotblocktime() #3 
    # plotSimpleCacheMiss() #2
    # plotBlockCacheMisses() #5
    # plotTotCacheMiss() #4
    # plotSimpleBandwidth() #6
    # plotBlockBandwidth() #7
    # plotBWspace() #8
    # plotblocktimeNormalized() #9
    print("Done")