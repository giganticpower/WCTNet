export CUDA_VISIBLE_DEVICES=0
python train_wctnet.py \
--task_name "Bfcn" \
--mode 1 \
--dataset 2 \
--batch_size 6 \
--sub_batch_size 6 \
--size_p 508 \
--size_g 508 \
--train \
--val 