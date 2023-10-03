#!/bin/bash
sbatch -c 2 --gres=gpu:1 -o train.out -J 319002721_train train.sh
