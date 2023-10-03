#!/bin/bash

cd /home/shaharzafran/CS236781-Mini-Project/yolov7
echo "$(pwd)"

source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate mini-project

python train.py --img 640 --epochs 22 --data ../taco-dataset/taco.yaml --cfg ./cfg/training/yolov7.yaml --weights yolov7_training.pt --batch-size 8 --adam