#!/bin/sh
  
#SBATCH --job-name=sim
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --ntasks-per-node=4

START=$(date)
mpiexec nrniv -mpi -quiet -python run_bionet.py config.json
END=$(date)

printf "Start: $START \nEnd:   $END\n"
