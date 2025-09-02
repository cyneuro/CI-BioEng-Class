# Simple simulation of the fear mechanism

## Setup

1. Follow instructions [from this page](https://www.anaconda.com/download/success) to download and install Anaconda.
2. Create a new conda environment for the simulation and activate it.
```bash
conda create --name fear_sim python=3.10
conda activate fear_sim
```
3. Install the required libraries.
```bash
pip install neuron
pip install bmtk
```

If you want to flash output to the micro:bit, additionally install
```bash
pip install uflash
```

4. Compile the modfiles.
```
cd fear_simulation/components/mechanisms
nrnivmodl .
```

## Run

The general algorithm for running a simulation is

1. Update `parameters.py` to the right values.
2. Run 
```bash
python build_network.py
python update_configs.py
```
to build the network.
3. Run `python run_bionet.py config.json` to run the simulation. 
4. Run `python check_output.py` to compute the oscillation frequency. The script will also try to flash the output onto the micro:bit.

Note: the output file must be on your local machine (to which the micro:bit is connected) for flashing to work. If you are running the scripts on a remote machine (e.g., FABRIC), you might need an additional step to transfer the outputs to your local machine.

## To do

1. Apply a 0.2 nA current. What is the oscillation frequency? What emotional state can it correspond to?
2. Apply a 1.0 nA current. What is the oscillation frequency? What emotional state can it correspond to?

## To submit

Submit a single Word document with:
1. Answers to the questions in the **To do** section.
2. Screenshots of the Terminal window showing the oscillation frequencies.

Additionally, sumbit 2 short videos showcasing micro:bit flickering for the two cases. 
