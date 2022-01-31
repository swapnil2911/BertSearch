#!/bin/sh

echo "Starting bert server"

bert-serving-start -cpu -max_batch_size 16 -num_worker 1 -max_seq_len 256 -model_dir /bert/cased_L-12_H-768_A-12