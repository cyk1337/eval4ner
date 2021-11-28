# NER-evaluation

This is a Python implementation of NER MUC evaluation. Refer to the blog [Evaluation Metrics of Name Entity Recognition](https://ychai.uk/notes/2018/11/21/NLP/NER/Evaluation-metrics-of-Name-Entity-Recognition-systems/#SemEval%E2%80%9813) for explanations of MUC metric.

## Installation
```bash
pip install eval4ner
```

## Usage
1. Evaluate single prediction
```python
import eval4ner.muc as muc
import pprint
grount_truth = [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
prediction = [('PER', 'John Jones and Peter Peters came to York')]
text = 'John Jones and Peter Peters came to York'
one_result = muc.evaluate_one(prediction, grount_truth, text)
pprint.pprint(one_result)
```

Output
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

2. Evaluate all predictions
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

## Cite
```
@misc{eval4ner,
  title={eval4ner},
  author={Yekun Chai},
  year={2018},
  howpublished={\url{https://cyk1337.github.io/notes/2018/11/21/NLP/NER/Evaluation-metrics-of-Name-Entity-Recognition-systems/}},
}
```

## References
1. [Evaluation of the SemEval-2013 Task 9.1: Recognition and Classification of pharmacological substances](https://www.cs.york.ac.uk/semeval-2013/task9/data/uploads/semeval_2013-task-9_1-evaluation-metrics.pdf)
2. [MUC-5 Evaluation Metrics](https://www.aclweb.org/anthology/M93-1007.pdf)