#!/bin/bash

CUDA_VISIBLE_DEVICES=0,1 nohup python3 train.py -n alexnet --dataset cifar100 --ngpu 2 --save --cuda &
CUDA_VISIBLE_DEVICES=2,3,4 nohup python3 train.py -n resnet18 --dataset cifar100 --ngpu 3 --save --cuda &
CUDA_VISIBLE_DEVICES=5,6,7 nohup python3 train.py -n mobilenetv2 --dataset cifar100 --ngpu 3 --save --cuda &