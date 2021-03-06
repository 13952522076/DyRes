from __future__ import print_function, absolute_import
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import time

from config import *

def init_params(net):
    '''Init layer parameters.'''
    for m in net.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out')
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=1e-3)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)

def get_mean_and_std(dataset):
    '''Compute the mean and std value of dataset.'''
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=True, num_workers=2)
    mean = torch.zeros(3)
    std = torch.zeros(3)
    print('==> Computing mean and std..')
    for inputs, targets in dataloader:
        for i in range(3):
            mean[i] += inputs[:,i,:,:].mean()
            std[i] += inputs[:,i,:,:].std()
    mean.div_(len(dataset))
    std.div_(len(dataset))
    return mean, std

def count_parameters(net, all=True):
    # If all= Flase, we only return the trainable parameters; tested
    return sum(p.numel() for p in net.parameters() if p.requires_grad or all)

def calculate_acc(dataloader, net, device):
    with torch.no_grad():
        correct = 0
        total = 0
        for data in dataloader:
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    return (correct / total) * 100

# INPUTS: output have shape of [batch_size, category_count]
#    and target in the shape of [batch_size] * there is only one true class for each sample
# topk is tuple of classes to be included in the precision
# topk have to a tuple so if you are giving one number, do not forget the comma
def accuracy(output, target, topk=(1,5)):
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)
        _, pred = torch.topk(input=output, k=maxk, dim=1, largest=True, sorted=True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul(100.0/batch_size))
        return res

def get_network(network, dataset, device):

    # ResNet18 and Related Work
    if network == 'cc_resnet18':
        if dataset == 'cifar100':
            from cifar.cc_resnet import CC_ResNet18
        else:
            from imagenet.cc_resnet import CC_ResNet18
        net = CC_ResNet18()
    elif network == 'dy_resnet18':
        if dataset == 'cifar100':
            from cifar.dy_resnet import Dy_ResNet18
        else:
            from imagenet.dy_resnet import Dy_ResNet18
        net = Dy_ResNet18()
    elif network == 'wn_resnet18':
        if dataset == 'cifar100':
            from cifar.wn_resnet import WN_ResNet18
        else:
            from imagenet.wn_resnet import WN_ResNet18
        net = WN_ResNet18()
    elif network == 'resnet18':
        if dataset == 'cifar100':
            from cifar.resnet import ResNet18
        else:
            from imagenet.resnet import ResNet18
        net = ResNet18()

    # Experiment
    elif network == 'gcwn_resnet18':
        if dataset == 'cifar100':
            from cifar.gcwn_resnet import GCWN_ResNet18
        else:
            from imagenet.gcwn_resnet import GCWN_ResNet18
        net = GCWN_ResNet18()
    elif network == 'gcwnnl_resnet18':
        if dataset == 'cifar100':
            from cifar.gcwn_resnet import GCWNNL_ResNet18
        else:
            from imagenet.gcwn_resnet import GCWNNL_ResNet18
        net = GCWNNL_ResNet18()
    elif network == 'nlcwn_resnet18':
        if dataset == 'cifar100':
            from cifar.nlcwn_resnet import NLCWN_ResNet18
        else:
            from imagenet.nlcwn_resnet import NLCWN_ResNet18
        net = NLCWN_ResNet18()
    elif network == 'dnlcwnp_resnet18':
        if dataset == 'cifar100':
            from cifar.dnlcwn_resnet import DNLCWN_ResNet18
        else:
            from imagenet.dnlcwn_resnet import DNLCWN_ResNet18
        net = DNLCWN_ResNet18(bn=False, gap_mode='prior')
    elif network == 'dnlcwnbnp_resnet18':
        if dataset == 'cifar100':
            from cifar.dnlcwn_resnet import DNLCWN_ResNet18
        else:
            from imagenet.dnlcwn_resnet import DNLCWN_ResNet18
        net = DNLCWN_ResNet18(bn=True, gap_mode='prior')
    elif network == 'dnlcwnl_resnet18':
        if dataset == 'cifar100':
            from cifar.dnlcwn_resnet import DNLCWN_ResNet18
        else:
            from imagenet.dnlcwn_resnet import DNLCWN_ResNet18
        net = DNLCWN_ResNet18(bn=False, gap_mode='later')
    elif network == 'dnlcwnbnl_resnet18':
        if dataset == 'cifar100':
            from cifar.dnlcwn_resnet import DNLCWN_ResNet18
        else:
            from imagenet.dnlcwn_resnet import DNLCWN_ResNet18
        net = DNLCWN_ResNet18(bn=True, gap_mode='later')
    
    # AlexNet and Related Work
    elif network == 'cc_alexnet':
        if dataset == 'cifar100':
            from cifar.cc_alexnet import CC_AlexNet
        else:
            from imagenet.cc_alexnet import CC_AlexNet
        net = CC_AlexNet()
    elif network == 'dy_alexnet':
        if dataset == 'cifar100':
            from cifar.dy_alexnet import Dy_AlexNet
        else:
            from imagenet.dy_alexnet import Dy_AlexNet
        net = Dy_AlexNet()
    elif network == 'wn_alexnet':
        if dataset == 'cifar100':
            from cifar.wn_alexnet import WN_AlexNet
        else:
            from imagenet.wn_alexnet import WN_AlexNet
        net = WN_AlexNet()
    elif network == 'alexnet':
        if dataset == 'cifar100':
            from cifar.alexnet import AlexNet
        else:
            from imagenet.alexnet import AlexNet
        net = AlexNet()

    # Experiment
    elif network == 'gcwn_alexnet':
        if dataset == 'cifar100':
            from cifar.gcwn_alexnet import GCWN_AlexNet
        else:
            from imagenet.gcwn_alexnet import GCWN_AlexNet
        net = GCWN_AlexNet()
    elif network == 'gcwnnl_alexnet':
        if dataset == 'cifar100':
            from cifar.gcwn_alexnet import GCWN_AlexNet
        else:
            from imagenet.gcwn_alexnet import GCWN_AlexNet
        net = GCWN_AlexNet(normalized=True)
    elif network == 'nlcwn_alexnet':
        if dataset == 'cifar100':
            from cifar.nlcwn_alexnet import NLCWN_AlexNet
        else:
            from imagenet.nlcwn_alexnet import NLCWN_AlexNet
        net = NLCWN_AlexNet()
    elif network == 'dnlcwnp_alexnet':
        if dataset == 'cifar100':
            from cifar.dnlcwn_alexnet import DNLCWN_AlexNet
        else:
            from imagenet.dnlcwn_alexnet import DNLCWN_AlexNet
        net = DNLCWN_AlexNet(bn=False, gap_mode='prior')
    elif network == 'dnlcwnbnp_alexnet':
        if dataset == 'cifar100':
            from cifar.dnlcwn_alexnet import DNLCWN_AlexNet
        else:
            from imagenet.dnlcwn_alexnet import DNLCWN_AlexNet
        net = DNLCWN_AlexNet(bn=True, gap_mode='prior')
    elif network == 'dnlcwnl_alexnet':
        if dataset == 'cifar100':
            from cifar.dnlcwn_alexnet import DNLCWN_AlexNet
        else:
            from imagenet.dnlcwn_alexnet import DNLCWN_AlexNet
        net = DNLCWN_AlexNet(bn=False, gap_mode='later')
    elif network == 'dnlcwnbnl_alexnet':
        if dataset == 'cifar100':
            from cifar.dnlcwn_alexnet import DNLCWN_AlexNet
        else:
            from imagenet.dnlcwn_alexnet import DNLCWN_AlexNet
        net = DNLCWN_AlexNet(bn=True, gap_mode='later')

    # MobileNetV2 and Related Work
    elif network == 'cc_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.cc_mobilenetv2 import CC_MobileNetV2
        else:
            from imagenet.cc_mobilenetv2 import CC_MobileNetV2
        net = CC_MobileNetV2()
    elif network == 'dy_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.dy_mobilenetv2 import Dy_MobileNetV2
        else:
            from imagenet.dy_mobilenetv2 import Dy_MobileNetV2
        net = Dy_MobileNetV2()
    elif network == 'wn_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.wn_mobilenetv2 import WN_MobileNetV2
        else:
            from imagenet.wn_mobilenetv2 import WN_MobileNetV2
        net = WN_MobileNetV2()
    elif network == 'mobilenetv2':
        if dataset == 'cifar100':
            from cifar.mobilenetv2 import MobileNetV2
        else:
            from imagenet.mobilenetv2 import MobileNetV2
        net = MobileNetV2()

    # Experiment
    elif network == 'gcwn_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.gcwn_mobilenetv2 import GCWN_MobileNetV2
        else:
            from imagenet.gcwn_mobilenetv2 import GCWN_MobileNetV2
        net = GCWN_MobileNetV2()
    elif network == 'gcwnnl_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.gcwn_mobilenetv2 import GCWN_MobileNetV2
        else:
            from imagenet.gcwn_mobilenetv2 import GCWN_MobileNetV2
        net = GCWN_MobileNetV2(normalized=True)
    elif network == 'nlcwn_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.nlcwn_mobilenetv2 import NLCWN_MobileNetV2
        else:
            from imagenet.nlcwn_mobilenetv2 import NLCWN_MobileNetV2
        net = NLCWN_MobileNetV2()
    elif network == 'dnlcwnp_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        else:
            from imagenet.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        net = DNLCWN_MobileNetV2(bn=False, gap_mode='prior')
    elif network == 'dnlcwnbnp_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        else:
            from imagenet.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        net = DNLCWN_MobileNetV2(bn=True, gap_mode='prior')
    elif network == 'dnlcwnl_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        else:
            from imagenet.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        net = DNLCWN_MobileNetV2(bn=False, gap_mode='later')
    elif network == 'dnlcwnbnl_mobilenetv2':
        if dataset == 'cifar100':
            from cifar.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        else:
            from imagenet.dnlcwn_mobilenetv2 import DNLCWN_MobileNetV2
        net = DNLCWN_MobileNetV2(bn=True, gap_mode='later')
        
    else:
        print('the network is not supported')
        sys.exit()
    
    net = net.to(device)

    return net

def get_dataloader(dataset, batch_size):
    if dataset == 'cifar100':
        train_transform = transforms.Compose(
            [transforms.RandomCrop(size=32, padding=4),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.ToTensor(),
            transforms.Normalize(CIFAR100_MEAN, CIFAR100_STD)
            ])

        test_transform = transforms.Compose(
            [transforms.ToTensor(),
            transforms.Normalize(CIFAR100_MEAN, CIFAR100_STD)
            ])
    
        trainset = torchvision.datasets.CIFAR100(root=DATA_ROOT, train=True, transform=train_transform, download=True)
        testset = torchvision.datasets.CIFAR100(root=DATA_ROOT, train=False, transform=test_transform, download=True)

    elif dataset == 'imagenet':
        train_transform = transforms.Compose(
            [transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
            ])

        test_transform = transforms.Compose(
            [transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
            ])
        
        trainset = torchvision.datasets.ImageNet(root=IMAGENET_DATA_DIR, split='train', transform=train_transform)
        testset = torchvision.datasets.ImageNet(root=IMAGENET_DATA_DIR, split='val', transform=test_transform)
    
    else:
        print('Dataset not supported yet...')
        sys.exit()

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)

    return trainloader, testloader

def save_plot(train_losses, train_accuracy, val_losses, val_accuracy, args, time_stamp):
    x = np.array([x for x in range(1, args.epoch + 1)])
    y1 = np.array(train_losses)
    y2 = np.array(val_losses)

    y3 = np.array(train_accuracy)
    y4 = np.array(val_accuracy)

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

    ax1.plot(x, y1, label='train loss')
    ax1.plot(x, y2, label='val loss')
    ax1.legend()
    ax1.xaxis.set_visible(False)
    ax1.set_ylabel('losses')

    ax2.plot(x, y3, label='train acc')
    ax2.plot(x, y4, label='val acc')
    ax2.legend()
    ax2.set_xlabel('batches')
    ax2.set_ylabel('acc')

    plt.savefig('plots/{}-losses-{}-b{}-e{}-{}.png'.format(args.network, args.dataset, args.batch, args.epoch, time_stamp))