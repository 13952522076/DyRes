# DyRes
<!-- Results on the CIFAR10 Dataset

| Models        | Basic         | CondConv      | DyConv        | WeightNet     | DyRes A       | DyRes B       | DyRes C       |
|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AlexNet       | 86.26%        | 86.20%        | 86.89%        | 86.42%        | 86.94%        | 87.21%        | 87.19%        |
| ResNet18      | 94.12%        | 93.76%        | 94.24%        | 92.79%        | 94.16%        | 94.15%        | 93.37%        |
| MobileNetV2   | 92.99%        | 92.88%        | 93.52%        | ------        | ------        | ------        | ------        | -->

<!-- Results on the CIFAR100 Dataset

| Models        | Basic         | CondConv      | DyConv        | WeightNet     | DyRes A       | DyRes B       | DyRes C       |
|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AlexNet       | 61.01%        | 61.47%        | 60.65%        | 60.81%        | 61.70%        | 62.03%        | 61.84%        |
| ResNet18      | 75.65%        | 75.85%        | 75.32%        | 73.00%        | 75.30%        | 74.77%        | 75.93%        |
| MobileNetV2   | 73.44%        | 73.84%        | 73.14%        | 73.58%        | ------        | ------        | ------        | -->

<!-- Results on the SVHN Dataset

| Models        | Basic         | CondConv      | DyConv        | WeightNet     | DyRes A       | DyRes B       | DyRes C       |
|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AlexNet       | 94.50%        | 94.65%        | 94.55%        | 94.61%        | 94.79%        | 94.82%        | 94.60%        |
| ResNet18      | 96.09%        | 96.41%        | 96.34%        | ------        | 96.29%        | ------        | ------        |
| MobileNetV2   | 96.32%        | 96.25%        | ------        | ------        | ------        | ------        | ------        | -->

<!-- Results on the Tiny ImageNet Dataset

| Models        | Basic         | CondConv      | DyConv        | WeightNet     | DyRes A       | DyRes B       | DyRes C       |
|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AlexNet       | 52.68%        | 53.33%        | 52.67%        | 52.78%        | 52.97%        | 52.92%        | 53.53%        |
| ResNet18      | 63.70%        | 65.97%        | 64.73%        | 59.81%        | ------        | ------        | ------        |
| MobileNetV2   | 56.49%        | 57.85%        | 55.84%        | 56.83%        | ------        | ------        | ------        | -->

<!-- Results on the ImageNet Dataset

| Models        | Basic         | CondConv      | DyConv        | WeightNet     | DyRes A       | DyRes B       | MSConv        |
|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AlexNet       | ------        | ------        | ------        | ------        | ------        | ------        | ------        |
| ResNet18      | ------        | ------        | ------        | ------        | ------        | ------        | ------        |
| MobileNetV2   | ------        | ------        | ------        | ------        | ------        | ------        | ------        | -->

| Models            | CIFAR100      | ImageNet      |
|-------------------|---------------|---------------|
| AlexNet           | 53.18%        | ------        |
| CC_AlexNet        | 59.51%        | ------        |
| DY_AlexNet        | 59.21%        | ------        |
| WN_AlexNet        | 59.63%        | ------        |
| ResNet18          | 72.51%        | ------        |
| CC_ResNet18       | 74.35%        | ------        |
| DY_ResNet18       | 73.44%        | ------        |
| WN_ResNet18       | 73.03%        | ------        |
| MobileNetV2       | 70.57%        | ------        |
| CC_MobileNetV2    | 71.07%        | ------        |
| DY_MobileNetV2    | 70.56%        | ------        |
| WN_MobileNetV2    | 70.96%        | ------        |

### Default Training Configurations

| Parameter                     | Value         |
|------------------------------ |---------------|
| epochs                        | 90            |
| batch                         | 128           |
| learning rate                 | 0.01          |
| update learning rate every    | 30 epochs     |
| learning rate update factor   | 0.1           |
| SGD momentum                  | 0.9           |
| SGD weight decay              | 5e-4          |

### How To Set Up Python and Pip

https://www.python.org/downloads/

### How To Set Up the Environment

To install the necessary Python packages for training

    pip3 install -r requirements.txt

### How To Run the Training

For simplicity, just run

    python3 train.py --network some_defined_network

If you want to play around with the hyper-parameters run ``python3 train.py -h`` to see the program's ``flags`` or ``arguments``.

    --network               Some predefined network architecture
    
    -e, --epoch             Number of epochs for training
    -b, --batch             Batch size
    -l, --lr                Learning rate for SGD
    -m, --momentum          Momentum for SGD
    -d, --weight-decay      Weight decay for SGD
    -s, --step-size         Update the learning rate every x epochs
    -g, --gamma             Learning rate update factor. new_lr = old_lr * gamma
    
    --save                  Whether to save network after training
    --dataset               Dataset to be trained with, CIFAR100 or ImageNet
    --cuda                  Use GPU to train if the flag is used
    --ngpu                  Number of GPUs used for training

Another example to run

    python3 train.py --network resnet18 -e 120 -b 512 -l 0.1 -m 0.9 -d 0.0005 -s 80 -g 0.1 --dataset cifar100 --cuda

### TODO:

- Brainstorm and improve ideas
