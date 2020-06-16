"""
Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>

This module is responsible for reading instructions from genome as a genotype and translating them into connectome as
a phenotype.

Instructions in this module are biologically inspired and a high level model after the neuroembryogenesis process that
translates genome to a fully developed brain starting from the embryo's neural tube.

In this framework, genome contains a list of all cortical layers and sub-layers for the brain. Each layer or sub-layer
has properties embedded within genome. Such properties are translated using this module to perform neurogenesis that
creates neurons followed by the process of synaptogenesis that is responsible for the creation of the connectivity
among neurons. All of the structures generated as a result of this process is stored in a data structure called
connectome.
"""

import logging
import json
import datetime
from evo import genetics
from functools import partial
from multiprocessing import Pool
from evo import stats
from evo import architect
from inf import disk_ops
from inf import settings
from inf import runtime_data
from inf.db_handler import InfluxManagement


log = logging.getLogger(__name__)
print(settings.Bcolors.YELLOW + "Module loaded: brain_gen" + settings.Bcolors.ENDC)

influxdb = InfluxManagement()


# Resets the in-memory brain for each cortical area
def reset_connectome_in_mem():
    for item in runtime_data.cortical_list:
        runtime_data.brain[item] = {}


# Resets all connectome files
def reset_connectome_files():
    for key in runtime_data.genome['blueprint']:
        file_name = runtime_data.parameters["InitData"]["connectome_path"] + key + '.json'
        with open(file_name, "w") as connectome:
            connectome.write(json.dumps({}))
            connectome.truncate()
        if runtime_data.parameters["Logs"]["print_brain_gen_activities"]:
            print(settings.Bcolors.YELLOW + "Cortical area %s is has been cleared." % key
                  + settings.Bcolors.ENDC)
        runtime_data.brain[key] = {}


def reuse():
    """
    Placeholder for a function to reuse an existing connectome.

    Returns:

    """
    log.info("Reusing an old connectome")
    connectome_path = ''
    return


def connectome_backup(src, dst):
    """
    Backs up an existing connectome to preserve all the structures and associated memory data for future use.
    Args:
        src (String): Location of the source connectome folder
        dst (String): Destination folder for storing connectome backup

    Returns:

    """
    import shutil
    import errno
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def neuron_count(self):
    return


# Reads the list of all Cortical areas defined in Genome
def cortical_list():
    blueprint = runtime_data.genome["blueprint"]
    cortical_list_ = []
    for key in blueprint:
        cortical_list_.append(key)
    return cortical_list_


def synapse_count(cortical_area_src, cortical_area_dst):
    brain = runtime_data.brain
    synapse__count = 0
    for neuron in brain[cortical_area_src]:
        for synapse in brain[cortical_area_src][neuron]['neighbors']:
            if brain[cortical_area_src][neuron]['neighbors'][synapse]['cortical_area'] == cortical_area_dst:
                synapse__count += 1
    return synapse__count


def cortical_connectivity_eval():
    """
    Evaluates whether the cortical structure is meeting minimum expectations for basic functionality.

    Returns: True or False
    """


def build_cortical_map():
    """
    Develops a data structure suitable for graphing cortical connectivity using iGraph package

    Sample output structure
    graph_edges = [(0, 2), (0, 1), (0, 3), (1, 2), (1, 3), (2, 4), (3, 4), (3, 0)]
    graph_weights = [8, 6, 3, 5, 6, 4, 9, 50]
    graph_labels = ['v1', 'v2', 'v3', 'v4', 'v5']

    Returns: Cortical map in a ... format.

    """
    graph_edges, graph_weights, graph_labels = [], [], []

    labels = [label for label in runtime_data.genome['blueprint']]
    indexes = [index for index in range(len(labels))]
    graph_labels = zip(indexes, labels)

    for entry in runtime_data.intercortical_mapping:
        # graph_weights.append(entry[2])
        print(entry)

    # for cortical_area in graph_labels:
    #     for cortical_mapping_dst in runtime_data.genome['blueprint'][cortical_area[1]]['cortical_mapping_dst']:
    #         graph_edges.append((cortical_area[0], cortical_mapping_dst))
    #         graph_weights.append(runtime_data.
    #                              genome['blueprint'][cortical_area[1]]['cortical_mapping_dst']
    #                              [cortical_mapping_dst]['established_synapses'])

    print("graph_edges", graph_edges)
    print("graph weights", graph_weights)
    print("graph labels:", list(graph_labels))

    return graph_edges, graph_weights, graph_labels


def ipu_opu_connectivity():
    """
    Evaluates synaptic connectivity between IPU and OPU

    Returns: True or False
    """


def connectome_structural_fitness():
    """
    To conduct a set of validations and calculate a structural fitness for the developed connectome. The returned value
    can be used to eliminate a premature structure.

    Returns: Structural fitness factor

    """
    #     vision_v2_it_synapse_cnt = synapse_count('vision_v2', 'vision_IT')
    #     vision_it_mem_synapse_cnt = synapse_count('vision_IT', 'vision_memory')
    #
    #     print("Synapse count vision_v2 >> vision_IT == ", vision_v2_it_synapse_cnt)
    #     print("Synapse count vision_IT >> vision_memory == ", vision_it_mem_synapse_cnt)
    #
    #     if vision_v2_it_synapse_cnt < 50 or vision_it_mem_synapse_cnt < 50:
    #         fitness = 0
    #     else:
    #         fitness = 1
    #     return fitness
    return


def develop_brain(reincarnation_mode=False):
    """
    This function operates in two modes. If run with reincarnation mode as false then it will develop a new brain by
    reading instructions from genome and developing it step by step. If run with reincarnation mode as True then the
    last available connectome data will be used to operate as a new brain. Reincarnation set to True will preserve the
    memories and learning from the previous generation while starting a new brain instance.

    Args:
        reincarnation_mode (bool): If true, an existing connectome will be used to reuse an existing brain structure.

    Returns:

    """

    if bool(reincarnation_mode):
        log.info('Reincarnating...')
        reuse()
    else:
        log.info('Developing a new brain...')
        genome_instructions = genetics.selection()
        develop()


def neurogenesis():
    # Develop Neurons for various cortical areas defined in Genome
    for cortical_area in runtime_data.genome["blueprint"]:
        timer = datetime.datetime.now()
        neuron_count = architect.three_dim_growth(cortical_area)
        if runtime_data.parameters["Logs"]["print_brain_gen_activities"]:
            duration = datetime.datetime.now() - timer
            print("Neuron Creation for Cortical area %s is now complete. Count: %i  Duration: %s  Per Neuron Avg.: %s"
                  % (cortical_area, neuron_count, duration, duration / neuron_count))

    disk_ops.save_brain_to_disk(brain=runtime_data.brain, parameters=runtime_data.parameters)
    disk_ops.save_block_dic_to_disk(block_dic=runtime_data.block_dic, parameters=runtime_data.parameters)


def synaptogenesis():
    func1 = partial(build_synapse, runtime_data.genome, runtime_data.brain, runtime_data.parameters)
    pool1 = Pool(processes=1)

    synapse_creation_candidates = []
    for key in runtime_data.genome["blueprint"]:
        if runtime_data.genome["blueprint"][key]["init_synapse_needed"]:
            synapse_creation_candidates.append(key)
        else:
            if runtime_data.parameters["Logs"]["print_brain_gen_activities"]:
                print("Synapse creation for Cortical area %s has been skipped." % key)

    pool1.map(func1, synapse_creation_candidates)
    pool1.close()
    pool1.join()

    print('All internal synapse creation has been completed.')
    # stats.brain_total_synapse_cnt()

    # Build Synapses across various Cortical areas
    func2 = partial(build_synapse_ext, runtime_data.genome, runtime_data.brain,
                    runtime_data.parameters, runtime_data.block_dic)
    pool2 = Pool(processes=1)

    runtime_data.intercortical_mapping = pool2.map(func2, runtime_data.genome["blueprint"])
    pool2.close()
    pool2.join()


def build_synapse(genome, brain, parameters, key):
    # Read Genome data
    timer = datetime.datetime.now()
    synapse_count, runtime_data.brain = \
        architect.neighbor_builder(brain=brain, genome=genome, brain_gen=True, cortical_area=key,
                                   rule_id=genome["blueprint"][key]["neighbor_locator_rule_id"],
                                   rule_param=genome["neighbor_locator_rule"]
                                   [genome["blueprint"][key]["neighbor_locator_rule_id"]]
                                   [genome["blueprint"][key]["neighbor_locator_rule_param_id"]],
                                   postsynaptic_current=genome["blueprint"][key]["postsynaptic_current"])
    if parameters["Logs"]["print_brain_gen_activities"]:
        duration = datetime.datetime.now() - timer
        print("Synapse creation for Cortical area %s is now complete. Count: %i  Duration: %s  Per Synapse Avg.: %s"
              % (key, synapse_count, duration, duration / synapse_count))
    disk_ops.save_brain_to_disk(cortical_area=key, brain=runtime_data.brain, parameters=parameters)


def build_synapse_ext(genome, brain, parameters, block_dic, key):
    runtime_data.block_dic = block_dic
    intercortical_mapping = []
    # Read Genome data
    for mapped_cortical_area in genome["blueprint"][key]["cortical_mapping_dst"]:
        timer = datetime.datetime.now()
        synapse_count, runtime_data.brain = \
            architect.neighbor_builder_ext(brain=brain, genome=genome, brain_gen=True, cortical_area_src=key,
                                           cortical_area_dst=mapped_cortical_area,
                                           rule=genome["blueprint"][key]
                                           ["cortical_mapping_dst"][mapped_cortical_area]
                                           ["neighbor_locator_rule_id"],
                                           rule_param=genome["neighbor_locator_rule"]
                                           [genome["blueprint"][key]
                                               ["cortical_mapping_dst"][mapped_cortical_area]
                                               ["neighbor_locator_rule_id"]]
                                           [genome["blueprint"][key]
                                               ["cortical_mapping_dst"]
                                               [mapped_cortical_area]
                                               ["neighbor_locator_rule_param_id"]],
                                           postsynaptic_current=genome["blueprint"]
                                           [key]["postsynaptic_current"])
        if parameters["Switches"]["influx_brain_gen_stats"]:
            influxdb.insert_inter_cortical_stats(connectome_path=parameters["InitData"]["connectome_path"],
                                                 cortical_area_src=key,
                                                 cortical_area_dst=mapped_cortical_area,
                                                 synapse_count=synapse_count)
        if parameters["Logs"]["print_brain_gen_activities"]:
            duration = datetime.datetime.now() - timer
            print("Synapse creation between Cortical area %s and %s is now complete. Count: %i  Duration: %s, "
                  "Per Synapse Avg.: %s"
                  % (key, mapped_cortical_area, synapse_count, duration, duration / synapse_count))

        # Adding External Synapse counts to genome for future use
        intercortical_mapping.append((key, mapped_cortical_area, synapse_count))

    disk_ops.save_brain_to_disk(cortical_area=key, brain=runtime_data.brain, parameters=parameters)
    return intercortical_mapping


def develop():
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    print("------------  Brain generation has begun-------")
    print("-----------------------------------------------")
    print("-----------------------------------------------")

    parameters = runtime_data.parameters
    runtime_data.brain = {}

    if parameters["Switches"]["folder_backup"]:
        # Backup the current folder
        connectome_backup('../Metis', '../Metis_archive/Metis_' + str(datetime.datetime.now()).replace(' ', '_'))

    # Reset in-memory brain data
    reset_connectome_in_mem()

    print("Here is the list of all defined cortical areas: %s " % runtime_data.cortical_list)
    print("::::: connectome path is:", parameters["InitData"]["connectome_path"])

    # --Reset Connectome--
    reset_connectome_files()

    # --Neurogenesis-- Creation of all Neurons across all cortical areas
    neurogenesis()

    # --Synaptogenesis-- Build Synapses within all cortical areas
    synaptogenesis()

    # Loading connectome data from disk to memory
    runtime_data.brain = disk_ops.load_brain_in_memory()

    print("Neuronal mapping across all Cortical areas has been completed!!")
    print("Total brain synapse count is: ", stats.brain_total_synapse_cnt())

    brain_structural_fitness = connectome_structural_fitness()
    print("Brain structural fitness was evaluated as: ", brain_structural_fitness)
    build_cortical_map()
    return brain_structural_fitness
