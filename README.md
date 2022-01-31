# Semantic Web Search Application IE
This project was taken as a year long project under IE NITK 2020.

## Demo

![](images/demo_image(1).jpeg)

![](images/demo_image(2).jpeg)

![](images/demo_image(3).jpeg)

![](images/demo_image(4).jpeg)

![](images/demo_image(5).jpeg)

## Requirements
- [Docker](https://docs.docker.com/engine/install/)
- [Pre-trained Model Bert](https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip)

## Usage
Unzip the bert model and move the extracted folder into bertserving folder

**CAUTION**: If possible, assign high memory(more than `8GB`) to Docker's memory configuration because BERT container needs high memory.

In the root directory, run

```
docker-compose up
```
