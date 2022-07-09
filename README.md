# eval4ner: An All-Round Evaluation for Named Entity Recognition
![Stable version](https://img.shields.io/pypi/v/eval4ner)
![Python3](https://img.shields.io/pypi/pyversions/eval4ner)![wheel:eval4ner](https://img.shields.io/pypi/wheel/eval4ner)
![Download](https://img.shields.io/pypi/dm/eval4ner)
![MIT License](https://img.shields.io/pypi/l/eval4ner)



Table of Contents
=================

- [TL;DR](https://github.com/cyk1337/eval4ner/#tldr)
- [Preliminaries for NER Evaluation](https://github.com/cyk1337/eval4ner/#preliminaries-for-ner-evaluation)
- [User Guide](https://github.com/cyk1337/eval4ner/#user-guide)
    - [Installation](https://github.com/cyk1337/eval4ner/#installation)
    - [Usage](https://github.com/cyk1337/eval4ner/#usage)
- [Citation](https://github.com/cyk1337/eval4ner/#citation)
- [References](https://github.com/cyk1337/eval4ner/#references)

This is a Python toolkit of MUC-5 evaluation metrics for evaluating Named Entity Recognition (NER) results. 


## TL;DR
It considers not only the mode of strict matching, *i.e.*, extracted entities are correct w.r.t both boundaries and types, but that of partial match, summarizing as following four modes:  
- Strict：exact match (Both entity boundary and type are correct)
- Exact boundary matching：predicted entity boundary is correct, regardless of entity boundary
- Partial boundary matching：entity boundaries overlap, regardless of entity boundary
- Type matching：some overlap between the system tagged entity and the gold annotation is required;


Refer to the blog [Evaluation Metrics of Name Entity Recognition](https://ychai.uk/notes/2018/11/21/NLP/NER/NER-Evaluation-Metrics/#SemEval%E2%80%9813) for explanations of MUC metric.

## Preliminaries for NER Evaluation
In research and production, following scenarios of NER systems can occur frequently: 

<table class="tg">
  <tr>
    <th class="tg-0pky">Scenario</th>
    <th class="tg-c3ow" colspan="2">Golden Standard</th>
    <th class="tg-c3ow" colspan="2">NER system prediction</th>
    <th class="tg-c3ow" colspan="4">Measure</th>
  </tr>
  <tr>
    <td class="tg-0pky"></td>
    <td class="tg-c3ow">Entity Type</td>
    <td class="tg-c3ow">Entity Boundary (Surface String)</td>
    <td class="tg-0pky">Entity Type</td>
    <td class="tg-0pky">Entity Boundary (Surface String)</td>
    <td class="tg-0pky">Type</td>
    <td class="tg-0pky">Partial</td>
    <td class="tg-0pky">Exact</td>
    <td class="tg-0pky">Strict</td>
  </tr>
  <tr>
    <td class="tg-0pky">III</td>
    <td class="tg-c3ow">MUSIC_NAME</td>
    <td class="tg-c3ow">告白气球</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky">MIS</td>
    <td class="tg-0pky">MIS</td>
    <td class="tg-0pky">MIS</td>
    <td class="tg-0pky">MIS</td>
  </tr>
  <tr>
    <td class="tg-0pky">II</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow"></td>
    <td class="tg-0pky">MUSIC_NAME</td>
    <td class="tg-0pky">年轮</td>
    <td class="tg-0pky">SPU</td>
    <td class="tg-0pky">SPU</td>
    <td class="tg-0pky">SPU</td>
    <td class="tg-0pky">SPU</td>
  </tr>
  <tr>
    <td class="tg-0pky">V</td>
    <td class="tg-c3ow">MUSIC_NAME</td>
    <td class="tg-c3ow">告白气球</td>
    <td class="tg-0pky">MUSIC_NAME</td>
    <td class="tg-0pky">一首告白气球</td>
    <td class="tg-0pky">COR</td>
    <td class="tg-0pky">PAR</td>
    <td class="tg-0pky">INC</td>
    <td class="tg-0pky">INC</td>
  </tr>
  <tr>
    <td class="tg-0pky">IV</td>
    <td class="tg-c3ow">MUSIC_NAME</td>
    <td class="tg-c3ow">告白气球</td>
    <td class="tg-0pky">SINGER</td>
    <td class="tg-0pky">告白气球</td>
    <td class="tg-0pky">INC</td>
    <td class="tg-0pky">COR</td>
    <td class="tg-0pky">COR</td>
    <td class="tg-0pky">INC</td>
  </tr>
  <tr>
    <td class="tg-0pky">I</td>
    <td class="tg-c3ow">MUSIC_NAME</td>
    <td class="tg-c3ow">告白气球</td>
    <td class="tg-0pky">MUSIC_NAME</td>
    <td class="tg-0pky">告白气球</td>
    <td class="tg-0pky">COR</td>
    <td class="tg-0pky">COR</td>
    <td class="tg-0pky">COR</td>
    <td class="tg-0pky">COR</td>
  </tr>
  <tr>
    <td class="tg-0pky">VI</td>
    <td class="tg-c3ow">MUSIC_NAME</td>
    <td class="tg-c3ow">告白气球</td>
    <td class="tg-0pky">SINGER</td>
    <td class="tg-0pky">一首告白气球</td>
    <td class="tg-0pky">INC</td>
    <td class="tg-0pky">PAR</td>
    <td class="tg-0pky">INC</td>
    <td class="tg-0pky">INC</td>
  </tr>
</table>

Thus, MUC-5 takes into account all these scenarios for all-sided evaluation. 

Then we can compute:

**Number of golden standard**:

<img src="https://render.githubusercontent.com/render/math?math=Possible(POS) = COR %2B INC %2B PAR %2B MIS = TP %2B FN">

**Number of predictee**: 

<img src="https://render.githubusercontent.com/render/math?math=Actual(ACT) = COR %2B INC %2B PAR %2B SPU = TP %2B FP">

The evaluation type of exact match and partial match are as follows:
### Exact match(i.e. Strict, Exact)
<img src="https://render.githubusercontent.com/render/math?math=Precision = \frac{COR}{ACT} = \frac{TP}{TP%2BFP}">
<img src="https://render.githubusercontent.com/render/math?math=Recall =\frac{COR}{POS}=\frac{TP}{TP%2BFN}">


### Partial match (i.e. Partial, Type)
<img src="https://render.githubusercontent.com/render/math?math=Precision = \frac{COR %2B 0.5\times PAR}{ACT}">
<img src="https://render.githubusercontent.com/render/math?math=Recall = \frac{COR %2B 0.5 \times PAR}{POS}">


### F-Measure
<img src="https://render.githubusercontent.com/render/math?math=F_\alpha = \frac{(\alpha^2 %2B 1)PR}{\alpha^2 P%2BR}">
<img src="https://render.githubusercontent.com/render/math?math=F_1 = \frac{2PR}{P%2BR}">

Therefore, we can get the results:
<table class="tg">
  <tr>
    <th class="tg-e6bt">Measure</th>
    <th class="tg-23iq">Type</th>
    <th class="tg-23iq">Partial</th>
    <th class="tg-ww3v">Exact</th>
    <th class="tg-ww3v">Strict</th>
  </tr>
  <tr>
    <td class="tg-e6bt">Correct</td>
    <td class="tg-23iq">2</td>
    <td class="tg-23iq">2</td>
    <td class="tg-ww3v">2</td>
    <td class="tg-ww3v">1</td>
  </tr>
  <tr>
    <td class="tg-e6bt">Incorrect</td>
    <td class="tg-23iq">2</td>
    <td class="tg-23iq">0</td>
    <td class="tg-ww3v">2</td>
    <td class="tg-ww3v">3</td>
  </tr>
  <tr>
    <td class="tg-e6bt">Partial</td>
    <td class="tg-23iq">0</td>
    <td class="tg-23iq">2</td>
    <td class="tg-ww3v">0</td>
    <td class="tg-ww3v">0</td>
  </tr>
  <tr>
    <td class="tg-e6bt">Missed</td>
    <td class="tg-23iq">1</td>
    <td class="tg-23iq">1</td>
    <td class="tg-ww3v">1</td>
    <td class="tg-ww3v">1</td>
  </tr>
  <tr>
    <td class="tg-e6bt">Spurius</td>
    <td class="tg-23iq">1</td>
    <td class="tg-23iq">1</td>
    <td class="tg-ww3v">1</td>
    <td class="tg-ww3v">1</td>
  </tr>
  <tr>
    <td class="tg-e6bt">Precision</td>
    <td class="tg-23iq">0.4</td>
    <td class="tg-23iq">0.6</td>
    <td class="tg-ww3v">0.4</td>
    <td class="tg-ww3v">0.2</td>
  </tr>
  <tr>
    <td class="tg-e6bt">Recall</td>
    <td class="tg-23iq">0.4</td>
    <td class="tg-23iq">0.6</td>
    <td class="tg-ww3v">0.4</td>
    <td class="tg-ww3v">0.2</td>
  </tr>
  <tr>
    <td class="tg-gx32">F1 score</td>
    <td class="tg-t0np">0.4</td>
    <td class="tg-t0np">0.6</td>
    <td class="tg-8l38">0.4</td>
    <td class="tg-8l38">0.2</td>
  </tr>
</table>

## User Guide
### Installation
```bash
pip install [-U] eval4ner
```

### Usage
#### 1. Evaluate single prediction
```python
import eval4ner.muc as muc
import pprint
grount_truth = [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
prediction = [('PER', 'John Jones and Peter Peters came to York')]
text = 'John Jones and Peter Peters came to York'
one_result = muc.evaluate_one(prediction, grount_truth, text)
pprint.pprint(one_result)
```

Output:
```bash
{'exact': {'actual': 1,
           'correct': 0,
           'f1_score': 0,
           'incorrect': 1,
           'missed': 2,
           'partial': 0,
           'possible': 3,
           'precision': 0.0,
           'recall': 0.0,
           'spurius': 0},
 'partial': {'actual': 1,
             'correct': 0,
             'f1_score': 0.25,
             'incorrect': 0,
             'missed': 2,
             'partial': 1,
             'possible': 3,
             'precision': 0.5,
             'recall': 0.16666666666666666,
             'spurius': 0},
 'strict': {'actual': 1,
            'correct': 0,
            'f1_score': 0,
            'incorrect': 1,
            'missed': 2,
            'partial': 0,
            'possible': 3,
            'precision': 0.0,
            'recall': 0.0,
            'spurius': 0},
 'type': {'actual': 1,
          'correct': 1,
          'f1_score': 0.5,
          'incorrect': 0,
          'missed': 2,
          'partial': 0,
          'possible': 3,
          'precision': 1.0,
          'recall': 0.3333333333333333,
          'spurius': 0}}

```

#### 2. Evaluate all predictions
```python
import eval4ner.muc as muc
# ground truth
grount_truths = [
    [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')],
    [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')],
    [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
]
# NER model prediction
predictions = [
    [('PER', 'John Jones and Peter Peters came to York')],
    [('LOC', 'John Jones'), ('PER', 'Peters'), ('LOC', 'York')],
    [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
]
# input texts
texts = [
    'John Jones and Peter Peters came to York',
    'John Jones and Peter Peters came to York',
    'John Jones and Peter Peters came to York'
]
muc.evaluate_all(predictions, grount_truths * 1, texts, verbose=True)
```

Output:
```bash
 NER evaluation scores:
  strict mode, Precision=0.4444, Recall=0.4444, F1:0.4444
   exact mode, Precision=0.5556, Recall=0.5556, F1:0.5556
 partial mode, Precision=0.7778, Recall=0.6667, F1:0.6944
    type mode, Precision=0.8889, Recall=0.6667, F1:0.7222
```

This repo will be long-term supported. Welcome to contribute and PR.

## Citation
For attribution in academic contexts, please cite this work as:
```
@misc{eval4ner,
  title={Evaluation Metrics of Named Entity Recognition},
  author={Chai, Yekun},
  year={2018},
  howpublished={\url{https://cyk1337.github.io/notes/2018/11/21/NLP/NER/NER-Evaluation-Metrics/}},
}

@misc{chai2018-ner-eval,
  author = {Chai, Yekun},
  title = {eval4ner: An All-Round Evaluation for Named Entity Recognition},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/cyk1337/eval4ner}}
}
```

## References
1. [Evaluation of the SemEval-2013 Task 9.1: Recognition and Classification of pharmacological substances](https://www.cs.york.ac.uk/semeval-2013/task9/data/uploads/semeval_2013-task-9_1-evaluation-metrics.pdf)
2. [MUC-5 Evaluation Metrics](https://www.aclweb.org/anthology/M93-1007.pdf)
