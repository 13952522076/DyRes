#!/bin/bash

CUDA_VISIBLE_DEVICES=0,1 nohup python3 train.py -n cc_alexnet --dataset cifar100 --ngpu 2 --save --cuda &
CUDA_VISIBLE_DEVICES=2,3,4 nohup python3 train.py -n cc_resnet18 --dataset cifar100 --ngpu 3 --save --cuda &
CUDA_VISIBLE_DEVICES=5,6,7 nohup python3 train.py -n cc_mobilenetv2 --dataset cifar100 --ngpu 3 --save --cuda &