import time
# from .FCtL import FCtL
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from .TT_module.resnet import resnet50
from .neck.fpem_v2 import FPEM_v2
from .neck.fpem_v1 import FPEM_v1
from .TT_module.conv_bn_relu import Conv_BN_ReLU
from models.neck.visual_transformer_noxin import FilterBasedTokenizer, Transformer, Projector

class det_Head(nn.Module):
    def __init__(self, in_channels, hidden_dim, num_classes):
        super(det_Head, self).__init__()
        self.conv1 = nn.Conv2d(in_channels,
                               hidden_dim,
                               kernel_size=3,
                               stride=1,
                               padding=1)
        self.bn1 = nn.BatchNorm2d(hidden_dim)
        self.relu1 = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(hidden_dim,
                               num_classes,
                               kernel_size=1,
                               stride=1,
                               padding=0)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, f):
        out = self.conv1(f)
        out = self.relu1(self.bn1(out))
        out = self.conv2(out)

        return out

class PAN_t(nn.Module):
    def __init__(self, num_classes, backbone='resnet50', neck='FPEM_v2', detection_head='PA_Head'):
        super(PAN_t, self).__init__()
        if backbone == 'resnet50':
            self.backbone = resnet50(pretrained=False)
        else:
            print('error backbone')

        if neck == 'FPEM_v1':
            neck = FPEM_v1(in_channels=(256, 512, 1024, 2048),
        out_channels=128)
        elif neck == 'FPEM_v2':
            neck = FPEM_v2(in_channels=(256, 512, 1024, 2048),
        out_channels=128)
        else:
            print('error neck')

        if detection_head == 'PA_Head':
            self.det_head = det_Head(in_channels=512,
        hidden_dim=128,
        num_classes=num_classes)
        else:
            print('error detection_head')

        in_channels = (256, 512, 1024, 2048)
        self.reduce_layer1 = Conv_BN_ReLU(in_channels[0], 128)
        self.reduce_layer2 = Conv_BN_ReLU(in_channels[1], 128)
        self.reduce_layer3 = Conv_BN_ReLU(in_channels[2], 128)
        self.reduce_layer4 = Conv_BN_ReLU(in_channels[3], 128)

        # self.reduce_layer_ts = Conv_BN_ReLU(512, 512)

        self.fpem1 = neck
        self.fpem2 = neck

        self.tokenizer = FilterBasedTokenizer(128, 128, 32)

        self.transformer = Transformer(128)
        self.transformer1 = Transformer(128)

        self.projector = Projector(128, 128)
        # if self.mode == 2 or self.mode == 3:
        #     self.big_attention = FCtL(512, 512)

    def _upsample(self, x, size, scale=1):
        _, _, H, W = size
        return F.upsample(x, size=(H // scale, W // scale), mode='bilinear')

    def forward(self,
                imgs,
                y=None):
        outputs = dict()
        bs, ch, h, w = imgs.shape

        if not self.training:
            torch.cuda.synchronize()
            start = time.time()

        # backbone
        f = self.backbone(imgs)

        if not self.training:
            torch.cuda.synchronize()
            outputs.update(dict(backbone_time=time.time() - start))
            start = time.time()

        # reduce channel
        f1 = self.reduce_layer1(f[0])
        f2 = self.reduce_layer2(f[1])
        f3 = self.reduce_layer3(f[2])
        f4 = self.reduce_layer4(f[3])

        # FPEM
        f1_1, f2_1, f3_1, f4_1 = self.fpem1(f1, f2, f3, f4)
        f1_2, f2_2, f3_2, f4_2 = self.fpem2(f1_1, f2_1, f3_1, f4_1)

        # FFM
        f1 = f1_1 + f1_2
        f2 = f2_1 + f2_2
        f3 = f3_1 + f3_2
        f4 = f4_1 + f4_2

        # transformer
        t1 = torch.flatten(f1, start_dim=2)
        t2 = torch.flatten(f2, start_dim=2)
        t3 = torch.flatten(f3, start_dim=2)
        t4 = torch.flatten(f4, start_dim=2)

        token_t1 = self.tokenizer(t1)
        token_t2 = self.tokenizer(t2)
        token_t3 = self.tokenizer(t3)
        token_t4 = self.tokenizer(t4)

        all_token = torch.cat((token_t1, token_t2, token_t3, token_t4), dim=2)
        encoder1 = self.transformer(all_token)
        encoder2 = self.transformer1(encoder1)


        e1, e2, e3, e4 = torch.split(encoder2, 32, dim=2)

        f1 = self.projector(t1, e1).view(-1, 128, round(h / 4), round(w / 4))
        f2 = self.projector(t2, e2).view(-1, 128, round(h / 8), round(w / 8))
        f3 = self.projector(t3, e3).view(-1, 128, round(h / 16), round(w / 16))
        f4 = self.projector(t4, e4).view(-1, 128, round(h / 32), round(w / 32))

        f2 = self._upsample(f2, f1.size())
        f3 = self._upsample(f3, f1.size())
        f4 = self._upsample(f4, f1.size())

        f = torch.cat((f1, f2, f3, f4), 1)

        # f_t = self.reduce_layer_ts(f)

        # detection
        det_out = self.det_head(f)

        # upsample
        det_out = self._upsample(det_out, imgs.size())

        # score = torch.sigmoid(det_out[:, 0, :, :])
        # kernels = det_out[:, :2, :, :] > 0
        # text_mask = kernels[:, :1, :, :]
        # kernels[:, 1:, :, :] = kernels[:, 1:, :, :] * text_mask
        # emb = det_out[:, 2:, :, :]
        # emb = emb * text_mask.float()
        #
        # score = score.data.cpu().numpy()[0].astype(np.float32)
        # kernels = kernels.data.cpu().numpy()[0].astype(np.uint8)
        # emb = emb.cpu().numpy()[0].astype(np.float32)
        # out1 = det_out[:, 1, :, :]
        # out1 = out1.data.cpu().numpy()[0].astype(np.uint8)
        # out2 = det_out[:, 0, :, :]
        # out2 = out2.data.cpu().numpy()[0].astype(np.uint8)
        #
        # cv2.imwrite('score.jpg', score * 255)
        # cv2.imwrite('out.jpg', out1 * 255)
        # cv2.imwrite('out2.jpg', out2 * 255)
        # cv2.imwrite('kernels.jpg', kernels[0, :, :] * 255)
        # cv2.imwrite('kernels1.jpg', kernels[1, :, :] * 255)
        # cv2.imwrite('emb.jpg', emb[0, :, :] * 255)

        return det_out