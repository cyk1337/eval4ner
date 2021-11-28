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
@file: test.py
@time: @Time : 4/15/21 3:22 PM 
@desc： 
               
'''

# !/usr/bin/env python

# -*- encoding: utf-8


from copy import deepcopy
import pprint

def evaluate_one(prediction: list, ground_truth: list, text: str):
    """
    Evaluate single case
    Calculate detailed partial evaluation metric. See Evaluation of the SemEval-2013 Task 9.1
    :param prediction (list): [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...]
    :param ground_truth (list): [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...]
    :return: eval_results (dict)
    """
    prediction = deepcopy(prediction)
    ground_truth = deepcopy(ground_truth)
    # if no label and no prediction, reguard as all correct!
    if len(prediction) == 0 and len(ground_truth) == 0:
        eval_metics = {"correct": 1,
                       "incorrect": 1,
                       "partial": 1,
                       "missed": 1,
                       "spurius": 1,
                       "precision": 1,
                       "recall": 1,
                       "f1_score": 1,
                       }
        # evaluation metrics in total
        eval_results = {"strict": deepcopy(eval_metics),
                        "exact": deepcopy(eval_metics),
                        "partial": deepcopy(eval_metics),
                        "type": deepcopy(eval_metics), }
        return eval_results

    eval_metics = {"correct": 0,
                   "incorrect": 0,
                   "partial": 0,
                   "missed": 0,
                   "spurius": 0,
                   "precision": 0,
                   "recall": 0,
                   "f1_score": 0,
                   }
    # evaluation metrics
    eval_results = {"strict": deepcopy(eval_metics),
                    "exact": deepcopy(eval_metics),
                    "partial": deepcopy(eval_metics),
                    "type": deepcopy(eval_metics), }
    prediction_tmp = deepcopy(prediction)
    ground_truth_tmp = deepcopy(ground_truth)
    for pred_tag, pred_val in prediction:
        # exact match, i.e. both entity boundary and entity type match
        # scenario 1
        flag1, ground_truth = check_Scenario1(pred_tag, pred_val, ground_truth)
        if flag1:
            # 'strict' matching
            eval_results['strict']['correct'] += 1
            eval_results['type']['correct'] += 1
            eval_results['exact']['correct'] += 1
            eval_results['partial']['correct'] += 1
            continue
        # partial match
        # scenario 5
        flag5, ground_truth = check_Scenario5(pred_tag, pred_val, ground_truth, text)
        if flag5:
            # exact boundary matching
            eval_results['strict']['incorrect'] += 1
            eval_results['exact']['incorrect'] += 1
            eval_results['partial']['partial'] += 1
            eval_results['type']['correct'] += 1
            continue

        # scenario 4: same pred value，entity type disagree
        flag4, ground_truth = check_Scenario4(pred_tag, pred_val, ground_truth)
        if flag4:
            eval_results['strict']['incorrect'] += 1
            eval_results['exact']['correct'] += 1
            eval_results['partial']['correct'] += 1
            eval_results['type']['incorrect'] += 1
            continue

        # scenario 6 : overlap exists, but tags disagree
        flag6, ground_truth = check_Scenario6(pred_tag, pred_val, ground_truth, text)
        if flag6:
            eval_results['strict']['incorrect'] += 1
            eval_results['exact']['incorrect'] += 1
            eval_results['partial']['partial'] += 1
            eval_results['type']['incorrect'] += 1
            continue

        # predictee not exists in golden standard
        # scenario 2: SPU, predicted entity not exists in golden, and no overlap on entity boundary
        flag2, ground_truth = check_Scenario2(pred_tag, pred_val, ground_truth, text)
        if flag2:
            eval_results['strict']['spurius'] += 1
            eval_results['exact']['spurius'] += 1
            eval_results['partial']['spurius'] += 1
            eval_results['type']['spurius'] += 1
            continue

    for true_tag, true_val in ground_truth_tmp:
        flag, prediction_tmp = check_Scenario3(true_tag, true_val, prediction_tmp, text)
        if flag:
            # count missing
            eval_results['strict']['missed'] += 1
            eval_results['exact']['missed'] += 1
            eval_results['partial']['missed'] += 1
            eval_results['type']['missed'] += 1

    # calculate P, R, F1
    # POS = len(grount_truth)
    # ACT = len(prediction)

    for k, eval_ in eval_results.items():
        COR = eval_["correct"]
        INC = eval_["incorrect"]
        PAR = eval_["partial"]
        MIS = eval_["missed"]
        SPU = eval_['spurius']
        eval_['possible'] = POS = COR + INC + PAR + MIS
        eval_['actual'] = ACT = COR + INC + PAR + SPU
        eval_["precision"] = (COR + 0.5 * PAR) / ACT if ACT > 0 else 0
        eval_["recall"] = (COR + 0.5 * PAR) / POS if POS > 0 else 0
        eval_["f1_score"] = 2 * eval_["precision"] * eval_["recall"] / (eval_["precision"] + eval_["recall"]) \
            if eval_["precision"] + eval_["recall"] > 0 else 0
    return eval_results


def check_Scenario1(pred_tag: str, pred_val: str, grount_truth: list):
    # scenario 1: both entity type and entity boundary strictly match
    COR_list = [1 for true_tag, true_val in grount_truth if true_tag == pred_tag and true_val == pred_val]
    if len(COR_list) > 0:
        grount_truth.remove((pred_tag, pred_val))
        return True, grount_truth
    else:
        return False, grount_truth


def check_Scenario5(pred_tag: str, pred_val: str, grount_truth: list, text: str):
    # scenario 5: same entity type and entity boundary overlap
    for true_tag, true_val in grount_truth:
        if pred_tag == true_tag and checkIfOverlap(true_val, pred_val, text):
            grount_truth.remove((true_tag, true_val))
            return True, grount_truth
    return False, grount_truth


def check_Scenario2(pred_tag: str, pred_val: str, grount_truth: list, text: str):
    # scenario 2: SPU, predicted entity type not exists in golden, and no overlap on entity boundary
    for true_tag, true_val in grount_truth:
        if checkIfOverlap(true_val, pred_val, text):
            return False, grount_truth
    return True, grount_truth


def check_Scenario3(true_tag: str, true_val: str, prediction: list, text: str):
    # Missed
    # scenario 3:entity boundary not overlap,  golden standard not exists in prediction
    for pred_tag, pred_val in prediction:
        if checkIfOverlap(true_val, pred_val, text):
            prediction.remove((pred_tag, pred_val))
            return False, prediction
    return True, prediction


def check_Scenario4(pred_tag: str, pred_val: str, grount_truth: list):
    # scenario 4: same pred value，entity type disagree
    for true_tag, true_val in grount_truth:
        if true_val == pred_val and true_tag != pred_tag:
            grount_truth.remove((true_tag, true_val))
            return True, grount_truth
    return False, grount_truth


def check_Scenario6(pred_tag: str, pred_val: str, grount_truth: list, text: str):
    # scenario 6: entity boundary overlap, entity type disagree
    for true_tag, true_val in grount_truth:
        if checkIfOverlap(true_val, pred_val, text) and true_tag != pred_tag:
            grount_truth.remove((true_tag, true_val))
            return True, grount_truth
    return False, grount_truth


def checkIfOverlap(true_val, pred_val, text):
    # method 1: check if index ranges have intersection (in index level)
    rang_a = findBoundary(true_val, text)
    rang_b = findBoundary(pred_val, text)
    if len(rang_a) == 0 or len(rang_b) == 0:
        return False
    else:
        for i, j in rang_a:
            for k, m in rang_b:
                intersec = set(range(i, j)).intersection(set(range(k, m)))
                if len(intersec) > 0:
                    return True
                else:
                    return False
    # method 2: check if there are intersections (in surface string level)
    # return not set(true_val).isdisjoint(pred_val)


def findBoundary(val, text):
    res = []
    for i in range(0, len(text) - len(val) + 1):
        if text[i:i + len(val)] == val:
            res.append((i, i + len(val)))
    return res


def update_overall_result(total_res: dict, res_single: dict):
    for mode in res_single:
        total_res[mode]["precision"] += res_single[mode]["precision"]
        total_res[mode]["recall"] += res_single[mode]["recall"]
        total_res[mode]["f1_score"] += res_single[mode]["f1_score"]
        total_res[mode]["count"] += 1
    return total_res


def evaluate_all(predictions: list, golden_labels: list, texts: list, verbose=False):
    """
    evaluate all cases
    :param predictions: list(list) [
                                [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...],
                                [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...],
                                [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...]
                            ]
    :param golden_labels: list(list)  [
                                [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...],
                                [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...],
                                [(slot tag, slot content), (slot tag, slot content), (slot tag, slot content), ...]
                            ]
    :param texts: list(str) [ text1, test2, text3, ...]
    :return: dict of results
    """
    assert len(predictions) == len(golden_labels) == len(
        texts), 'the counts of predictions/golden_labels/texts are not equal!'
    eval_metics = {"precision": 0,
                   "recall": 0,
                   "f1_score": 0,
                   'count': 0
                   }
    # evaluation metrics in total
    total_results = {"strict": deepcopy(eval_metics),
                     "exact": deepcopy(eval_metics),
                     "partial": deepcopy(eval_metics),
                     "type": deepcopy(eval_metics), }
    predictions_copy = deepcopy(predictions)
    golden_labels_copy = deepcopy(golden_labels)
    for i, (pred, gt, text) in enumerate(zip(predictions_copy, golden_labels_copy, texts)):
        one_result = evaluate_one(pred, gt, text)
        if verbose:
            print('--'*6, 'sample_{:0>6}:'.format(i + 1))
            pprint.pprint(one_result)
        total_results = update_overall_result(total_results, one_result)

    print('\n', 'NER evaluation scores:')
    for mode, res in total_results.items():
        print("{:>8s} mode, Precision={:<6.4f}, Recall={:<6.4f}, F1:{:<6.4f}"
              .format(mode, res['precision'] / res['count'], res['recall'] / res['count'],
                      res['f1_score'] / res['count']))
    return total_results


if __name__ == '__main__':
    grount_truth = [('PER', 'John Jones'), ('PER', 'Peter Peters'), ('LOC', 'York')]
    prediction = [('PER', 'John Jones and Peter Peters came to York')]
    text = 'John Jones and Peter Peters came to York'
    # print(evaluate_one(prediction, grount_truth, text))
    # print(evaluate_one(prediction, grount_truth, text))

    evaluate_all([prediction] * 1, [grount_truth] * 1, [text] * 1, verbose=True)
    evaluate_all([prediction] * 1, [grount_truth] * 1, [text] * 1, verbose=True)
