#!/bin/sh
bert-serving-start -cpu -max_batch_size 16 -http_port 8125 -num_worker=$1 -model_dir /model