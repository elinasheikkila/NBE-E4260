import numpy as np
from synapse import Synapse


class Neuron:

    def __init__(self, network):
        self.network = network
        self.excitation_state = 0
        self.intrinsic_signal = False
        self.switched = False
        self.input_synapses = []
        self.output_synapses = []

    def add_connection(self, other):
        if not self.has_synapse_with(other):
            synapse = Synapse(other, self, self.network.get_deg_rate())
            self.input_synapses.append(synapse)
            other.output_synapses.append(synapse)
            self.network.add_synapse(synapse)
        else:
            self.input_synapses.append(self.get_synapse_with(other))

    def has_synapse_with(self, parent):
        for synapse in self.input_synapses:
            if synapse in parent.output_synapses:
                return True
        return False

    def get_synapse_with(self, parent):
        for synapse in self.input_synapses:
            if synapse in parent.output_synapses:
                return synapse

    def update(self):
        if len(self.input_synapses) == 0:
            if not self.intrinsic_signal:
                state = np.random.uniform(0, 1)
                if state <= 0.5:
                    self.excitation_state = 0
                else:
                    self.excitation_state = 1
            else:
                self.excitation_state = 1
        else:
            sum_term = 0
            for synapse in self.input_synapses:
                sum_term += synapse.get_glutamate()
            self.excitation_state = sum_term

    def output(self, t_step):
        for synapse in self.output_synapses:
            synapse.update(self.excitation_state, t_step)

    def get_value(self):
        return self.excitation_state

    def get_target_state(self, threshold):
        if self.excitation_state >= threshold or self.switched:
            self.switched = True
            return 1
        else:
            return 0

    def set_signal(self, logical):
        self.intrinsic_signal = logical

    def get_output_synapses(self):
        return self.output_synapses

    def add_input_synapse(self, synapse):
        self.input_synapses.append(synapse)

    def add_output_synapse(self, synapse):
        self.output_synapses.append(synapse)
