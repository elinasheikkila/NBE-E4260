from matplotlib import pyplot as plt
import numpy as np
import time
from network import Network


def run_simulation(network, t_total, t_step):
    t_current = 0
    while t_current < t_total:
        network.update(t_step)
        t_current += t_step
    if 1 in network.get_target_output():
        return 1
    else:
        return 0


def plot_target_output(network, t_total, deg_rate):
    target_output = network.get_target_output()
    f, ax = plt.subplots(1)
    f.set_figwidth(10)
    f.set_figheight(6)
    ax.plot(np.linspace(0, t_total, len(target_output)), target_output, color='blue')
    ax.set_title('State of the output switch as a function of time (glutamate degradation = {})'.format(deg_rate))
    ax.set_xlabel('time (s)')
    ax.set_ylabel('State (ON/OFF)')
    ax.set_xlim(0, t_total)
    ax.set_ylim(0, 2)
    ax.grid()
    f.savefig('output.png')


def plot_inputs(network, t_total):
    inputs = network.get_array_output()
    f, ax = plt.subplots(1, len(inputs[0]))
    f.set_figwidth(len(inputs[0]*10))
    f.set_figheight(6)
    for i in range(len(inputs[0])):
        ax[i].plot(np.linspace(0, 1, int(len(inputs[0][i])/t_total)), inputs[0][i][0:int(len(inputs[0][i])/t_total)], color='blue')
        ax[i].set_xlim(0, 1)
        ax[i].set_xlabel('time (s)')
        ax[i].set_ylabel('State (ON/OFF)')
        ax[i].set_title('Input signal {}'.format(i+1))
        ax[i].grid()
        ax[i].set_ylim(0, 3)
    f.savefig('inputs.png')


def plot_synapses(network, t_total):
    synapses = network.get_synapses()
    f, ax = plt.subplots(network.get_n_layers(), int(len(synapses)/network.get_n_layers()))
    f.set_figwidth(int(len(synapses)/network.get_n_layers())*10)
    f.set_figheight(network.get_n_layers()*6)
    for i in range(network.get_n_layers()):
        for j in range(int(len(synapses)/network.get_n_layers())):
            ax[i, j].plot(np.linspace(0, 5, len(synapses[i*int(len(synapses)/network.get_n_layers())+j].get_history()[0:5*int(len(synapses[i+j].get_history())/t_total)])), synapses[i*int(len(synapses)/network.get_n_layers())+j].get_history()[0:5*int(len(synapses[i+j].get_history())/t_total)], color='blue')
            ax[i, j].set_title('Synapse {}'.format(i*int(len(synapses)/network.get_n_layers())+j+1))
            ax[i, j].set_xlabel('time (s)')
            ax[i, j].set_ylabel('[glutamate]')
            ax[i, j].set_xlim(0, 5)
            ax[i, j].set_ylim(0, 2)
            ax[i, j].grid()
    f.savefig('synapses.png')


def plot_astrocytes(network, t_total):
    astrocytes = network.get_astrocytes()
    f, ax = plt.subplots(network.get_n_layers(), int(len(astrocytes)/network.get_n_layers()))
    f.set_figwidth(int(len(astrocytes) / network.get_n_layers()) * 10)
    f.set_figheight(network.get_n_layers() * 6)
    for i in range(network.get_n_layers()):
        for j in range(int(len(astrocytes) / network.get_n_layers())):
            ax[i, j].plot(np.linspace(0, t_total, len(astrocytes[i*int(len(astrocytes) / network.get_n_layers()) + j].get_history())), astrocytes[i*int(len(astrocytes) / network.get_n_layers()) + j].get_history(), color='blue')
            ax[i, j].plot(np.linspace(0, t_total, len(astrocytes[i*int(len(astrocytes) / network.get_n_layers()) + j].get_state_history())), astrocytes[i*int(len(astrocytes) / network.get_n_layers()) + j].get_state_history(), color='black')
            ax[i, j].set_title('Astrocyte {}'.format(i * int(len(astrocytes) / network.get_n_layers()) + j + 1))
            ax[i, j].set_xlabel('time (s)')
            ax[i, j].set_ylabel('[glutamate]')
            ax[i, j].set_xlim(0, t_total)
            ax[i, j].set_ylim(0, 20)
            ax[i, j].grid()
    f.savefig('astrocytes.png')


def plot_accuracies(energies, accuracies, deg_rates, threshold, synapse_type, reps):
    f, ax = plt.subplots(1)
    f.set_figwidth(15)
    f.set_figheight(10)
    ax.plot(deg_rates, accuracies, color='blue')
    ax.set_xlim(min(deg_rates), max(deg_rates))
    ax.set_ylim(0.2, 1.1)
    ax.set_xticks(deg_rates, deg_rates, rotation='vertical')
    ax.invert_xaxis()
    ax2 = ax.twinx()
    ax2.plot(deg_rates, energies, color='red')
    ax2.set_ylim(min(energies), min(energies)+10**6)
    if synapse_type == 1:
        ax.set_title('Signal detection accuracy and synapse energy with t={}, n={} and bipartite synapses'.format(threshold, reps))
    else:
        ax.set_title('Signal detection accuracy and synapse energy with t={}, n={} and tripartite synapses'.format(threshold, reps))
    ax.set_xlabel('degradation rate of glutamate')
    ax.set_ylabel('accuracy', color='blue')
    ax2.set_ylabel('synapse energy', color='red')
    ax.grid()
    f.savefig('accuracies.png')


def main():
    deg_rates = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0.75, 0.5, 0.25, 0.001]  # x-axis for accuracy plots
    threshold = 1.0  # threshold value for the switching of the output node

    mode = 0
    synapse_type = 0
    n_layers = 0
    n_cells = 0

    a_size = 0
    signal_pos = -1
    deg_rate = -1

    print('Welcome to astrocyte simulator.')
    while mode not in [1, 2]:
        print('Enter 1 for single trial mode. Enter 2 for accuracy testing mode.')
        mode = int(input())
        if mode not in [1, 2]:
            print('Not a valid input value.')
    while synapse_type not in [1, 2]:
        print('Enter 1 to simulate with bipartite synapses.\nEnter 2 to simulate with tripartite synapses.')
        synapse_type = int(input())
        if synapse_type not in [1, 2]:
            print('Not a valid input value.')
    while n_layers == 0:
        print('Enter the number of subsequent neuron layers.')
        n_layers = int(input())
        if n_layers <= 0:
            print('Enter a positive number.')
            n_layers = 0
    while n_cells == 0:
        print('Enter the number of neurons per layer.')
        n_cells = int(input())
        if n_cells <= 0:
            print('Enter a positive number.')
            n_cells = 0
    while a_size == 0 and synapse_type == 2:
        print('Enter the number of neurons one astrocyte is connected to.')
        a_size = int(input())
        if a_size <= 0:
            print('Enter a positive number.')
            a_size = 0
    if mode == 1:
        while signal_pos == -1:
            print('Select a neuron from the first layer to have an intrinsic signal.')
            print('Options are integers from {} to {}.'.format(1, n_cells))
            print('Enter zero to give only random inputs from the first layer.')
            signal_pos = int(input())
            if signal_pos < 0 or signal_pos > n_cells:
                print('Enter a valid choice.')
                signal_pos = -1
        while deg_rate == -1:
            print('Give glutamate degradation rate.')
            deg_rate = float(input())
            if deg_rate <= 0:
                print("Give a positive rate.")
                deg_rate = -1

    if mode == 1:
        network = Network(synapse_type, n_layers, n_cells, a_size, signal_pos, threshold, deg_rate)

        t_total = 100
        t_step = 0.01
        print('Running a single trial.')
        st = time.time()
        run_simulation(network, t_total, t_step)
        et = time.time()
        print('Simulation complete.')
        print('Elapsed wall time: {}'.format(et-st))
        plot_target_output(network, t_total, deg_rate)
        plot_inputs(network, t_total)
        plot_synapses(network, t_total)
        if synapse_type == 2:
            plot_astrocytes(network, t_total)

    if mode == 2:
        accuracies = []
        energies = [0]*len(deg_rates)
        reps = 200
        print('Running {} times {} trials.'.format(reps, len(deg_rates)))
        st = time.time()
        for i in range(len(deg_rates)):
            truth = []
            outputs = []
            for j in range(reps):
                on_off = np.random.uniform(0, 1)
                if on_off >= 0.5:
                    truth.append(1)
                    channel = np.random.uniform(0, 1)
                    for k in range(1, n_cells + 1):
                        if (k-1)/n_cells < channel <= k/n_cells:
                            network = Network(synapse_type, n_layers, n_cells, a_size, k, threshold, deg_rates[i])
                else:
                    truth.append(0)
                    network = Network(synapse_type, n_layers, n_cells, a_size, 0, threshold, deg_rates[i])
                t_total = 100
                t_step = 0.01
                outputs.append(run_simulation(network, t_total, t_step))
                for k in range(len(network.get_synapses())):
                    energies[i] += sum(network.get_synapses()[k].get_history())
            sum_term = 0
            energies[i] = energies[i] * (1/reps)
            for n in range(len(outputs)):
                if outputs[n] == truth[n]:
                    sum_term += 1
            accuracies.append(sum_term/len(outputs))
        et = time.time()
        print('Simulation complete.')
        print('Elapsed wall time: {}'.format(et-st))
        plot_accuracies(energies, accuracies, deg_rates, threshold, synapse_type, reps)


main()
