import numpy as np
import json
from parameters import Parameters
parameters = Parameters()

random_state = np.random.RandomState(123)

if __name__ == "__main__":

    # Load gids
    with open("gid_info.json", "r") as f:
        gids = json.load(f)

    # Set current injection

    with open("simulation_config.json", "r") as f:
        sim_config = json.load(f)

    node_sets = [f"{i}_E" for i in range(parameters.N_assemblies)]

    CI = {
        f"cclamp_{i}_E": {
        "input_type": "current_clamp",
        "module": "IClamp",
        "node_set": [gid for gid in gids['all_exc_gids'] if gid in gids['all_gids'][i]],
        "gids": [gid for gid in gids['all_exc_gids'] if gid in gids['all_gids'][i]],
        "amp": parameters.I_E,
        "delay": parameters.IClamp_delay,
        "duration": parameters.IClamp_dur
        }
        for i in range(parameters.N_assemblies)
    }

    sim_config["inputs"] = CI

    with open("simulation_config.json", "w") as f:
        json.dump(sim_config, f, indent = 1)

    
    # Set distribution strategy
    with open("circuit_config.json", "r") as f:
        circ_config = json.load(f)

    node_ranks = {}

    if parameters.strategy == "random":
        all_gids_conc = np.concatenate(gids["all_gids"])
        random_state.shuffle(all_gids_conc)
        for array_id, array in enumerate(np.split(all_gids_conc, parameters.N_assemblies)):
            node_ranks[str(array_id)] = array.tolist()

    elif parameters.strategy == "assembly":
        for assembly_id in range(parameters.N_assemblies):
            node_ranks[str(assembly_id)] = gids["all_gids"][assembly_id]

    elif parameters.strategy == "partitioning":
        raise ValueError
    else:
        raise ValueError
    
    circ_config["networks"]["node_ranks"] = node_ranks

    with open("circuit_config.json", "w") as f:
        json.dump(circ_config, f, indent = 1)