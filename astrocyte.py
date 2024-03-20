class Astrocyte:

    def __init__(self, neuron_array):
        self.neurons_in = neuron_array
        self.glutamate = 0
        self.switched = False
        self.a1 = 15
        self.a2 = 0.3
        self.c2 = 1
        self.b = 10
        self.synapses = []
        self.history = []
        self.state_history = []
        for neuron in self.neurons_in:
            for synapse in neuron.get_output_synapses():
                self.synapses.append(synapse)
                synapse.add_astrocyte(self)

    def update(self, t_step):
        for synapse in self.synapses:
            self.glutamate += synapse.get_glutamate()*self.a1*t_step
            synapse.reduce_glutamate(synapse.get_glutamate()*self.a1*t_step)
        if self.glutamate >= self.b or self.switched and self.glutamate >= 10:
            self.switched = True
            for synapse in self.synapses:
                synapse.add_glutamate(self.glutamate*self.c2*t_step)
            self.glutamate -= self.glutamate*self.c2*t_step*len(self.synapses) + self.glutamate*self.a2*t_step
            self.state_history.append(5)
        else:
            self.switched = False
            self.glutamate -= self.a2*self.glutamate*t_step
            self.state_history.append(0)
        if self.glutamate < 0:
            self.glutamate = 0
        self.history.append(self.glutamate)

    def get_history(self):
        return self.history

    def get_state_history(self):
        return self.state_history
