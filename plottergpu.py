import matplotlib.pyplot as plt

import numpy as np
import math

MAX_ESP = 13
input_prefix = "logs2/" #where does data come from
output_prefix = "plots2/" #where to save images

#data shape:
#T: 32, B: 16#
#N, OpTime, Op-GB/s, KTime, K-GB/s (basic, conflcit, block)#
#T and B change each 9 lines, 13 combinations

def load_data(filename):
    #data = np.loadtxt(input_prefix + filename, delimiter=",")
    #skip lines with comments
    data = np.genfromtxt(input_prefix + filename, delimiter=",", comments="#", skip_header=0)
    #print(data)
    return data

#troughput over N for each kernel
def plot_throughput_over_N(data, title, filename): #T: 32, B: 8#
    data = data[-18:-9] #second to last group
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at T=32, B=8")
    ax.set_ylabel("Throughput (GB/s)")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    # ax.plot(data[:,0].astype(int).astype(str), data[:,2], label="Basic") #horrible
    ax.plot(data[:,0].astype(int).astype(str), data[:,6], label="Conflict")
    ax.plot(data[:,0].astype(int).astype(str), data[:,10], label="Block")
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

#troughput over T for each kernel
def plot_throughput_over_T(data, title, filename): #N: 1024, B: 8#
    #groups 0idx: 4, 7, 11
    #data = data[(6*9):(6*9+9)] + data[(9*9):(9*9+9)] + data[(13*9):(13*9+9)]
    data0 = data[(4*9):(4*9+9)]
    data1 = data[(7*9):(7*9+9)]
    data2 = data[(11*9):(11*9+9)]
    # T = 8, 16, 32
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at B=8")
    ax.set_ylabel("Throughput (GB/s)")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    # ax.plot(data0[:,0].astype(int).astype(str), data0[:,2], label="Basic-T8", color="cyan")
    # ax.plot(data1[:,0].astype(int).astype(str), data1[:,2], label="Basic-T16", color="purple")
    # ax.plot(data2[:,0].astype(int).astype(str), data2[:,2], label="Basic-T32", color="blue")
    #adding the basic makes the plot unreadable, and its not that interesting
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,6], label="Conflict-T8", color="pink")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,6], label="Conflict-T16", color="orange")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,6], label="Conflict-T32", color="red")
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,10], label="Block-T8", color="gray")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,10], label="Block-T16", color="olive")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,10], label="Block-T32", color="green")
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

#troughput over B for each kernel
def plot_throughput_over_B(data, title, filename): #N: 1024, T: 32#
    #skip 9*9 lines, B = 2, 4, 8, 16
    data0 = data[(9*9):(9*9+9)]
    data1 = data[(10*9):(10*9+9)]
    data2 = data[(11*9):(11*9+9)]
    data3 = data[(12*9):(12*9+9)]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at T=32")
    ax.set_ylabel("Throughput (GB/s)")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    #more is better, expect for 2
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,2], label="Basic-B2")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,2], label="Basic-B4")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,2], label="Basic-B8")
    ax.plot(data3[:,0].astype(int).astype(str), data3[:,2], label="Basic-B16")

    #more is better
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,6], label="Conflict-B2")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,6], label="Conflict-B4")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,6], label="Conflict-B8")
    ax.plot(data3[:,0].astype(int).astype(str), data3[:,6], label="Conflict-B16")

    #16 is shit
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,10], label="Block-B2")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,10], label="Block-B4")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,10], label="Block-B8")
    ax.plot(data2[:,0].astype(int).astype(str), data3[:,10], label="Block-B16")
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

#total time over N for each kernel
def plot_time_over_N(data, title, filename): #T=32 B=8
    data = data[-18:-9]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at T=32 B=8")
    ax.set_ylabel("Time (ms)")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    #ax.plot(data[:,0].astype(int).astype(str), data[:,1], label="Basic")
    ax.plot(data[:,0].astype(int).astype(str), data[:,5], label="Conflict")
    ax.plot(data[:,0].astype(int).astype(str), data[:,9], label="Block")
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

#time in kernel only
def plot_kernel_time(data, title, filename):#T=32 B=8
    data = data[-18:-9]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at T=32 B=8")
    ax.set_ylabel("Time (ms)")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    #ax.plot(data[:,0].astype(int).astype(str), data[:,3], label="Basic")
    ax.plot(data[:,0].astype(int).astype(str), data[:,7], label="Conflict")
    ax.plot(data[:,0].astype(int).astype(str), data[:,11], label="Block")
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

#total time over kernel time for each kernel along N
def plot_kernel_time_over_total(data, title, filename): #T=32 B=8
    data = data[-18:-9]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at T=32 B=8")
    ax.set_ylabel("Kernel Time / Total Time")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    #ax.plot(data[:,0].astype(int).astype(str), data[:,3] / data[:,1], label="Basic")
    ax.plot(data[:,0].astype(int).astype(str), data[:,7] / data[:,5], label="Conflict")
    ax.plot(data[:,0].astype(int).astype(str), data[:,11] / data[:,9], label="Block")
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

# kernel time over total time for each kernel along T at N=1024
def plot_kernel_time_over_total_T(data, title, filename): #N=1024 B=8
    data0 = data[(4*9):(4*9+9)]
    data1 = data[(7*9):(7*9+9)]
    data2 = data[(11*9):(11*9+9)]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at B=8")
    ax.set_ylabel("Kernel Time / Total Time")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)

    #not much variation
    # ax.plot(data0[:,0].astype(int).astype(str), data0[:,3] / data0[:,1], label="Basic-T8")
    # ax.plot(data1[:,0].astype(int).astype(str), data1[:,3] / data1[:,1], label="Basic-T16")
    # ax.plot(data2[:,0].astype(int).astype(str), data2[:,3] / data2[:,1], label="Basic-T32")
    
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,7] / data0[:,5], label="Conflict-T8")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,7] / data1[:,5], label="Conflict-T16")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,7] / data2[:,5], label="Conflict-T32")
    
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,11] / data0[:,9], label="Block-T8")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,11] / data1[:,9], label="Block-T16")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,11] / data2[:,9], label="Block-T32")
    
    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)

#same along B for T=32
def plot_kernel_time_over_total_B(data, title, filename): #N=1024 T=32
    data0 = data[(9*9):(9*9+9)]
    data1 = data[(10*9):(10*9+9)]
    data2 = data[(11*9):(11*9+9)]
    data3 = data[(12*9):(12*9+9)]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("N at T=32")
    ax.set_ylabel("Kernel Time / Total Time")
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.grid(True)
    #
    # ax.plot(data0[:,0].astype(int).astype(str), data0[:,3] / data0[:,1], label="Basic-B2")
    # ax.plot(data1[:,0].astype(int).astype(str), data1[:,3] / data1[:,1], label="Basic-B4")
    # ax.plot(data2[:,0].astype(int).astype(str), data2[:,3] / data2[:,1], label="Basic-B8")
    # ax.plot(data3[:,0].astype(int).astype(str), data3[:,3] / data3[:,1], label="Basic-B16")

    # some ok, some dependant
    # ax.plot(data0[:,0].astype(int).astype(str), data0[:,7] / data0[:,5], label="Conflict-B2")
    # ax.plot(data1[:,0].astype(int).astype(str), data1[:,7] / data1[:,5], label="Conflict-B4")
    # ax.plot(data2[:,0].astype(int).astype(str), data2[:,7] / data2[:,5], label="Conflict-B8")
    # ax.plot(data3[:,0].astype(int).astype(str), data3[:,7] / data3[:,5], label="Conflict-B16")

    # consistently dependant
    ax.plot(data0[:,0].astype(int).astype(str), data0[:,11] / data0[:,9], label="Block-B2")
    ax.plot(data1[:,0].astype(int).astype(str), data1[:,11] / data1[:,9], label="Block-B4")
    ax.plot(data2[:,0].astype(int).astype(str), data2[:,11] / data2[:,9], label="Block-B8")
    ax.plot(data3[:,0].astype(int).astype(str), data3[:,11] / data3[:,9], label="Block-B16")

    ax.legend()
    fig.savefig(output_prefix + filename)
    plt.close(fig)


if __name__ == "__main__":
    data = load_data("outputall.log")
    # print(data.shape)

    plot_throughput_over_B(data, "Throughput over B", "throughput_over_B.png")
    plot_throughput_over_N(data, "Throughput over N", "throughput_over_N.png")
    plot_throughput_over_T(data, "Throughput over T", "throughput_over_T.png")
    plot_time_over_N(data, "Time over N", "time_over_N.png")
    plot_kernel_time_over_total(data, "Kernel time over total time", "kernel_time_over_total.png")
    plot_kernel_time_over_total_T(data, "Kernel time over total time", "kernel_time_over_total_T.png")
    plot_kernel_time_over_total_B(data, "Kernel time over total time", "kernel_time_over_total_B.png")
    plot_kernel_time(data, "Kernel time", "kernel_time.png")
    print("Done local")

    data = load_data("outputcluster.log")
    # print(data.shape)

    plot_throughput_over_B(data, "Throughput over B", "C_throughput_over_B.png")
    plot_throughput_over_N(data, "Throughput over N", "C_throughput_over_N.png")
    plot_throughput_over_T(data, "Throughput over T", "C_throughput_over_T.png")
    plot_time_over_N(data, "Time over N", "C_time_over_N.png")
    plot_kernel_time_over_total(data, "Kernel time over total time", "C_kernel_time_over_total.png")
    plot_kernel_time_over_total_T(data, "Kernel time over total time", "C_kernel_time_over_total_T.png")
    plot_kernel_time_over_total_B(data, "Kernel time over total time", "C_kernel_time_over_total_B.png")
    plot_kernel_time(data, "Kernel time", "C_kernel_time.png")
    print("Done cluster")