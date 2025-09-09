# Emotion recognition using EEG and computer games (+micro:bit)

> [!IMPORTANT]
> You are expected to encounter errors when working on this project (e.g., problems with library installation, environment setup, pathing issues, bad connection to the micro:bit, etc.) These errors are a natural part of developing a CI workflow. Learning how to resolve these errors is a part of this project!

## Setup (for both local and remote)

1. Create a new conda environment for this project (use `python=3.10`) and activate it.
2. Install the required libraries.

```bash
pip install 'numpy < 2'
pip install pandas
pip install matplotlib
pip install scikit-learn
pip install uflash
```

Additonally, install `pytorch` by choosing your OS [here](https://pytorch.org/get-started/locally/) and running the command they provide.
The other parameters should be set to `PyTorchBuild = Stable (X.X.X)`, `Package = Pip`, `Language = Python`, `Compute Platform = CPU`.

3. **(Local-only)** Install an environment to run Jupyter Notebooks, e.g., [Visual Studio Code](https://code.visualstudio.com).

## Experiment 1 (run on local)

You are going to work with the dataset that contains EEG signals recorded from participants playing emotionally different computer games (boring, calm, horror, funny). The goal of this experiment is to train a simple convolutional neural network to predict the emotion from these recordings and display the prediction on the micro:bit.

1. Get familiar with [what EEG data are](https://en.wikipedia.org/wiki/Electroencephalography), [electrode positioning systmes](https://en.wikipedia.org/wiki/10–20_system_(EEG)) and the notion of a [montage](https://www.learningeeg.com/montages-and-technical-components). Summarize advantages and disadvantages of EEG recordings and differences between bipolar and referential montages.

2. Read about [the dataset structure](https://www.kaggle.com/datasets/wajahat1064/emotion-recognition-using-eeg-and-computer-games?resource=download). What is the total recording time for each participant? You are going to work with the data from participant S01 placed in the `data/` folder.

3. Open the [`eeg_emotion_classification.ipynb`](eeg_emotion_classification.ipynb) notebook. If it asks you to install additional modules, kernel, etc., choose "Install". Follow the notebook to process the dataset and train a model. You can adjust the parameters specified by "TODO" comments to increase accuracy.

4. Review [the Heart project](https://microbit.org/projects/make-it-code-it/heart/?editor=python) to learn how to display images on the micro:bit. Choose an image for each emotion and write a script for projecting that image to the micro:bit (see `flicker.py` and `check_output.py` from the previous project for reference). Integrate the projection functionality into the notebook so that when the network makes a prediction, it gets displayed on the micro:bit.

## Experiment 2 (run on remote)

Transform the notebook from Experiment 1 into a script that can run on a terminal-first machine (e.g., FABRIC). Train the network on a remote machine and compare the training time between local and remote.

## To submit

1. A Word document with answers to questions 1-2 from Experiment 1 and with time comparison from Experiment 2.
2. A completed notebook from Experiment 1.
