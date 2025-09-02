import numpy as np
from bmtk.utils.reports.spike_trains import SpikeTrains

def flash_to_bit(firing_rate):
    with open("flicker.py", "r") as file:
        script = file.readlines()
    script[0] = f'frequency = {firing_rate}\n'
    with open("flicker.py", "w") as file:
        file.writelines(script)

    import os
    os.system("uflash flicker.py")

spikes = SpikeTrains.load('output/spikes.h5', population = 'PING-Assembly')
ISI = np.diff(np.sort(spikes.get_times(node_id = 0)))
firing_rate = 1000 / np.mean(ISI)
print(f"The network is oscillating around {firing_rate} Hz.")

try:
    flash_to_bit(firing_rate)
except:
    pass