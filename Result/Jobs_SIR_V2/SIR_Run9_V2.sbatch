#!/bin/bash
#SBATCH --partition=discovery_q
#SBATCH --nodes=1
#SBATCH --job-name=SIR_run9_V2
#SBATCH --array=0-9
##SBATCH --exclusive
#SBATCH -t 24:00:00
#SBATCH --mail-user jacky92@bi.vt.edu
#SBATCH --mail-type=ALL

##Read files from directory into array



module load networkx



JOBROOT=/home/jacky92/CS5424/Code/
OUTDIR=/home/jacky92/Jobs/
#Read files into array
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 0 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 1 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 2 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 3 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 4 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 5 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 6 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 7 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 8 $SLURM_ARRAY_TASK_ID
python $JOBROOT"run9_V2.py" $JOBROOT"network_node-10000_degree-5_seed-1.pkl" 9 $SLURM_ARRAY_TASK_ID





















