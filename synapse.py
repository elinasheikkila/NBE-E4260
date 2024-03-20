class Synapse:

    def __init__(self, neuron_in, neuron_out, deg_rate):
        self.neurons_in = [neuron_in]
        self.neurons_out = [neuron_out]
        self.has_astrocyte = False
        self.astrocyte = False
        self.glutamate = 0
        self.degradation_rate = deg_rate
        self.history = []

    def add_neuron_in(self, neuron_in):
        if neuron_in not in self.neurons_in:
            self.neurons_in.append(neuron_in)

    def add_neuron_out(self, neuron_out):
        if neuron_out not in self.neurons_out:
            self.neurons_out.append(neuron_out)

    def get_neurons_in(self):
        return self.neurons_in

    def get_neurons_out(self):
        return self.neurons_out

    def get_glutamate(self):
        return self.glutamate

    def add_astrocyte(self, astrocyte):
        self.has_astrocyte = True
        self.astrocyte = astrocyte

    def update(self, excitation, t_step):
        if excitation >= 0:
            self.glutamate += 5*excitation*t_step
        else:
            self.glutamate += 1*t_step
        self.glutamate -= self.degradation_rate*self.glutamate*t_step
        self.history.append(self.glutamate)

    def reduce_glutamate(self, amount):
        self.glutamate -= amount
        if self.glutamate < 0:
            self.glutamate = 0

    def add_glutamate(self, amount):
        self.glutamate += amount

    def get_history(self):
        return self.history
