from neuron import Neuron
from astrocyte import Astrocyte


class Network:

    def __init__(self, synapse_type, n_layers, n_cells, a_size, signal, threshold, deg_rate):
        self.type = synapse_type
        self.n_layers = n_layers
        self.n_cells = n_cells
        self.a_size = a_size
        self.signal = signal
        self.threshold = threshold
        self.deg_rate = deg_rate
        self.synapses = []

        self.array_output = [[[] for _ in range(self.n_cells)] for _ in range(self.n_layers)]
        self.array = [[[] for _ in range(self.n_cells)] for _ in range(self.n_layers)]

        self.target_output = []
        self.target = Neuron(self)
        self.create_array()
        self.init_target()
        self.init_signal()

        self.astrocytes = []
        if synapse_type == 2:
            self.create_astrocytes()

    def create_array(self):
        for i in range(self.n_layers):
            for j in range(self.n_cells):
                self.array_output[i][j] = []
                self.array[i][j] = Neuron(self)
                if i >= 1:
                    self.array[i][j].add_connection(self.array[i-1][j])

    def init_target(self):
        for i in range(self.n_cells):
            self.target.add_connection(self.array[self.n_layers-1][i])

    def init_signal(self):
        if self.signal != 0:
            self.array[0][self.signal - 1].set_signal(True)

    def create_astrocytes(self):
        for i in range(self.n_layers):
            for j in range(int(self.n_cells/self.a_size)):
                astrocyte = Astrocyte(self.array[i][j*self.a_size:(j+1)*self.a_size])
                self.astrocytes.append(astrocyte)

    def update(self, t_step):
        for i in range(self.n_layers):
            for j in range(self.n_cells):
                self.array[i][j].update()
                self.array_output[i][j].append(self.array[i][j].get_value())
        self.target.update()
        self.target_output.append(self.target.get_target_state(self.threshold))
        for i in range(self.n_layers):
            for j in range(self.n_cells):
                self.array[i][j].output(t_step)
        if self.type == 2:
            for astrocyte in self.astrocytes:
                astrocyte.update(t_step)

    def get_synapse_type(self):
        return self.type

    def get_n_layers(self):
        return self.n_layers

    def get_n_cells(self):
        return self.n_cells

    def get_a_size(self):
        return self.a_size

    def get_target_output(self):
        return self.target_output

    def get_array_output(self):
        return self.array_output

    def add_synapse(self, synapse):
        self.synapses.append(synapse)

    def get_synapses(self):
        return self.synapses

    def get_astrocytes(self):
        return self.astrocytes

    def get_deg_rate(self):
        return self.deg_rate
