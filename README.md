# Semantic Web Search Application IE
This project was taken as a year long project under IE NITK 2020.

## Requirements
- [ElasticSearch](https://www.elastic.co/downloads/elasticsearch)
- [Flask](https://www.elastic.co/downloads/elasticsearch)
- [Bert-As-Service](https://bert-as-service.readthedocs.io/en/latest/)
- Pre trained Bert Model

### Downloading a pretrained BERT model

<details>
 <summary>List of released pretrained BERT models (click to expand...)</summary>


<table>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip">BERT-Base, Uncased</a></td><td>12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-24_H-1024_A-16.zip">BERT-Large, Uncased</a></td><td>24-layer, 1024-hidden, 16-heads, 340M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip">BERT-Base, Cased</a></td><td>12-layer, 768-hidden, 12-heads , 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_10_18/cased_L-24_H-1024_A-16.zip">BERT-Large, Cased</a></td><td>24-layer, 1024-hidden, 16-heads, 340M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip">BERT-Base, Multilingual Cased (New)</a></td><td>104 languages, 12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_11_03/multilingual_L-12_H-768_A-12.zip">BERT-Base, Multilingual Cased (Old)</a></td><td>102 languages, 12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
<tr><td><a href="https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip">BERT-Base, Chinese</a></td><td>Chinese Simplified and Traditional, 12-layer, 768-hidden, 12-heads, 110M parameters</td></tr>
</table>

</details>


## Usage

### Commands to setup initially

Run
```
pip install -r requirements.txt
```

Install scrapy

Go to the Spiders Directory and run the following command

```
scrapy crawl stackoverflow -o injest.json
```

Alternatively the default injest.json file provided in the search folder can be used.

move injest.json into the search folder and run the following command to injest data into elasticsearch

```
python initiate.py
```

### Commands to run to start the application
Unzip the bert model and move the extracted folder into root directory and run

```
bert-serving-start -cpu -max_batch_size 16 -num_worker 1 -max_seq_len 256 -model_dir /<model_name>/
```

 go to ElasticSearch directory and run 

```
.\bin\elasticsearch.bat
```

Run the application from the search folder using the following command:

```
python search.py
```

## Demo

![](images/demo_image(1).jpeg)

![](images/demo_image(2).jpeg)

![](images/demo_image(3).jpeg)

![](images/demo_image(4).jpeg)

![](images/demo_image(5).jpeg)
