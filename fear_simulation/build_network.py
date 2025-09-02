import numpy as np
import json

from bmtk.builder.networks import NetworkBuilder
from bmtk.utils.sim_setup import build_env_bionet

from parameters import Parameters
parameters = Parameters() 

random_state = np.random.RandomState(parameters.random_state)

def syn_connector(source, target, p):
    if source['node_id'] == target['node_id']: return 0
    return 1 if random_state.random() < p else 0

MAX_BETWEEN = 0 if parameters.N_assemblies == 1 else int(parameters.N_cell_per_assembly * parameters.N_between / (parameters.N_assemblies - 1))
BETWEEN_COUNTER = 0
def between_connector(source, target, p):
    global BETWEEN_COUNTER, MAX_BETWEEN
    if source['node_id'] == target['node_id']: return 0
    if BETWEEN_COUNTER < MAX_BETWEEN:
        BETWEEN_COUNTER += 1
        return 1
    else:
        return 0

if __name__ == "__main__":

    net = NetworkBuilder("PING-Assembly")

    all_gids = []
    all_exc_gids = []
    all_inh_gids = []
    GID_COUNTER = 0

    # Build each assembly
    for assembly_id in range(parameters.N_assemblies):
        assembly_gids = []

        # Exc cells
        net.add_nodes(
            N = parameters.N_E, 
            pop_name = f'{assembly_id}_E', 
            model_type = 'biophysical',
            model_template = 'hoc:RTMExcCell',
            morphology='blank.swc')
        
        assembly_gids.extend(list(range(GID_COUNTER, GID_COUNTER + parameters.N_E)))
        all_exc_gids.extend(list(range(GID_COUNTER, GID_COUNTER + parameters.N_E)))
        GID_COUNTER += parameters.N_E
        
        # Inh cells
        net.add_nodes(
            N = parameters.N_I, 
            pop_name = f'{assembly_id}_I',
            model_type = 'biophysical',
            model_template = 'hoc:WBInhCell', 
            morphology = 'blank.swc')
        
        assembly_gids.extend(list(range(GID_COUNTER, GID_COUNTER + parameters.N_I)))
        all_inh_gids.extend(list(range(GID_COUNTER, GID_COUNTER + parameters.N_I)))
        GID_COUNTER += parameters.N_I

        all_gids.append(assembly_gids)
        
        # E-I
        net.add_edges(
            source = {'pop_name': f'{assembly_id}_E'}, 
            target = {'pop_name': f'{assembly_id}_I'},
            connection_rule = syn_connector, 
            connection_params = {'p': parameters.p_EI},
            delay = 0,
            syn_weight = parameters.g_EI / parameters.N_E,
            weight_function = None,
            target_sections = ['soma'],
            distance_range = [0.0, 0.1],
            dynamics_params = 'PING_ExcToInh.json',
            model_template  ='Exp2Syn')

        # I-I
        net.add_edges(
            source = {'pop_name': f'{assembly_id}_I'}, 
            target = {'pop_name': f'{assembly_id}_I'},
            connection_rule = syn_connector, 
            connection_params={'p': parameters.p_II},
            delay = 0,
            syn_weight = parameters.g_II / parameters.N_I,
            weight_function = None,
            target_sections = ['soma'],
            distance_range = [0.0, 0.1],
            dynamics_params = 'PING_InhToInh.json',
            model_template = 'Exp2Syn')
                        
        # I-E
        net.add_edges(
            source={'pop_name': f'{assembly_id}_I'}, 
            target={'pop_name': f'{assembly_id}_E'},
            connection_rule = syn_connector,
            connection_params = {'p': parameters.p_IE},
            delay = 0,
            syn_weight = parameters.g_IE / parameters.N_I,
            weight_function = None,
            target_sections = ['soma'],
            distance_range = [0.0, 0.1],
            dynamics_params = 'PING_InhToExc.json',
            model_template = 'Exp2Syn')
    
    # Add between-assembly connections
    for source_assembly_id in range(parameters.N_assemblies):
        for target_assembly_id in range(parameters.N_assemblies):
            # Don't connect to self
            if source_assembly_id == target_assembly_id: continue

            BETWEEN_COUNTER = 0
            net.add_edges(
                source = {'pop_name': f'{source_assembly_id}_E'}, 
                target = {'pop_name': f'{target_assembly_id}_I'},
                connection_rule = between_connector, 
                connection_params = {'p': parameters.p_EI},
                delay = 0,
                syn_weight = parameters.g_EI / parameters.N_E,
                weight_function = None,
                target_sections = ['soma'],
                distance_range = [0.0, 0.1],
                dynamics_params = 'PING_ExcToInh.json',
                model_template  ='Exp2Syn') 


    net.build()
    net.save_nodes(output_dir = 'network')
    net.save_edges(output_dir = 'network')

    # Build the environment
    build_env_bionet(
        base_dir = '.',
        network_dir = 'network',
        tstop = parameters.tstop, 
        dt = parameters.dt,
        report_vars = ['v'],
        v_init = -65,
        include_examples = False,
        compile_mechanisms = False,
        config_file = 'config.json'
    )

    with open("gid_info.json", "w") as file:
        json.dump({
            "all_gids": all_gids,
            "all_exc_gids": all_exc_gids,
            "all_inh_gids": all_inh_gids
        }, file, indent = 1)

