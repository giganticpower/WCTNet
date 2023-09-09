export CUDA_VISIBLE_DEVICES=0,1
python train_wctnet.py \
--task_name "TT_mode2" \
--mode 2 \
--dataset 1 \
--batch_size 24 \
--sub_batch_size 24 \
--size_p 512 \
--size_g 512 \
--pre_path TT.epoch99.pth \
--train \
--val 