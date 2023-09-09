Multi-level Contexts Weighted Coupling Transformer (WCTNet), for UHR segmentation.

In this paper, we propose Multi-level Contexts Weighted Coupling Transformer (WCTNet), to develop an efficient framework for UHR segmentation. Previous approaches divide UHR images into regular patches for multi-scale local segmentation. Hierarchical reasoning leads to an urgent dilemma between memory efficiency and segmentation quality. To improve it, this paper proposes Multi-level Feature Weighting (MFW) module and Token-based Transformer (TT) to weight and couple multi-level semantic contexts.

WCTNet achieves state-of-the-art performance on two UHR datasets including DeepGlobe and Inria Aerial. Experimental results show that this contextual weighting and coupling of single-scale patches enables WCTNet to balance its accuracy and computational overhead well.

## Test and train
Our code is Available in [WCTNet](https://github.com/giganticpower/WCTNet) and based on [Fctl](https://github.com/liqiokkk/FCtL) 
python>=3.6 and pytorch>=1.2.0  
Please install the dependencies: `pip install -r requirements.txt`
### dataset
Please register and download [Inria Aerial](https://project.inria.fr/aerialimagelabeling/) dataset  
Create folder named 'data_1', its structure is  
```
data_1/
├── train
   ├── Sat
      ├── xxx_sat.tif
      ├── ...
   ├── Label
      ├── xxx_mask.png(two values:0-1)
      ├── ...
├── crossvali
├── offical_crossvali
```

### data transfer
We have provided several key scripts for data conversion
You can use the three files in folder /data_1 to convert label formats, image labels to category labels, and partition datasets
`python class_tranfer.py`  
`python data_splip.py` 
`python label_transfor.py` 

### test
`bash test.sh`  
### train
Please sequentially finish the following steps:   
1.`bash train_pre.sh`
2.`bash train_wct.sh`

## Citation
If you use this code or our results for your research, please cite our paper.
```
publishing
```
