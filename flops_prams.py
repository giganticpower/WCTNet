from helper import create_model_load_weights
import torch
from thop import profile
import os


def get_para_andflops(model):
    total_num = sum(p.numel() for p in model.parameters())
    trainable_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print('tt=' + total_num)

# model, global_fixed_medium, global_fixed_large = create_model_load_weights(7, './saved_models_dg/', './saved_models_dg/', './saved_models_dg/', 1)
# net = model
#
# inp_shape = (3, 508, 508) #输入的分辨率
#
# from ptflops import get_model_complexity_info
#
# FLOPS = 0
# macs, params = get_model_complexity_info(net, inp_shape, verbose=False, print_per_layer_stat=True)
#
# # params = float(params[:-4])
# print(params, macs)
# macs = float(macs[:-4]) + FLOPS / 10 ** 9
#
# print('mac', macs, params)


if __name__ == '__main__':
    # os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    model, global_fixed_medium, global_fixed_large = create_model_load_weights(7, './saved_models_dg/', './saved_models_dg/', './saved_models_dg/', 1)
    input = torch.randn(1, 3, 508, 508)
    input = input.cuda()
    # model = model.cuda()
    # global_fixed_medium = global_fixed_medium.cuda()
    # global_fixed_large = global_fixed_large.cuda()
    flops, pram = profile(model, inputs=(input,))
    print("flops= {}".format(flops / 1e9))
    print("prams= {}".format(pram / 1e6))