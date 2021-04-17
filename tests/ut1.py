#!/usr/bin/env python

# -*- encoding: utf-8

'''
_____.___._______________  __.____ __________    _________   ___ ___    _____  .___ 
\__  |   |\_   _____/    |/ _|    |   \      \   \_   ___ \ /   |   \  /  _  \ |   |
 /   |   | |    __)_|      < |    |   /   |   \  /    \  \//    ~    \/  /_\  \|   |
 \____   | |        \    |  \|    |  /    |    \ \     \___\    Y    /    |    \   |
 / ______|/_______  /____|__ \______/\____|__  /  \______  /\___|_  /\____|__  /___|
 \/               \/        \/               \/          \/       \/         \/     
 

@author: Yekun Chai
@license: CYK
@email: chaiyekun@gmail.com
@file: ut1.py
@time: @Time : 4/15/21 4:10 PM 
@desc： 
               
'''


def single_ut1():
    grount_truth = [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
    prediction = [('PER', 'John Jones and Peter Peters came to York')]
    text = 'John Jones and Peter Peters came to York'
    one_result = muc.evaluate_one(prediction, grount_truth, text)
    pprint.pprint(one_result)


def single_ut2():
    """
        test single
    """
    grount_truth = [("PER", "John Jones")]
    prediction = [("PER", "John"), ("PER", "Jones")]
    text = 'John Jones and Peter Peters came to York'
    one_result = muc.evaluate_one(prediction, grount_truth, text)
    pprint.pprint(one_result)


def all_ut1():
    """
        test all
    """
    grount_truths = [
        [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')],
        [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')],
        [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
    ]
    predictions = [
        [('PER', 'John Jones and Peter Peters came to York')],
        [('LOC', 'John Jones'), ('PER', 'Peters'), ('LOC', 'York')],
        [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
    ]
    texts = [
        'John Jones and Peter Peters came to York',
        'John Jones and Peter Peters came to York',
        'John Jones and Peter Peters came to York'
    ]
    muc.evaluate_all(predictions, grount_truths * 1, texts, verbose=True)


if __name__ == '__main__':
    import eval4ner.muc as muc
    import pprint


    single_ut2()
