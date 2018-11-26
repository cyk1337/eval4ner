#!/usr/bin/env python

# -*- encoding: utf-8

'''
                      ______   ___  __
                     / ___\ \ / / |/ /
                    | |    \ V /| ' / 
                    | |___  | | | . \ 
                     \____| |_| |_|\_\
 ==========================================================================
@author: Yekun Chai

@license: School of Informatics, Edinburgh

@contact: chaiyekun@gmail.com

@file: UtilsTest.py

@time: 23/11/2018 17:48 

@desc：       
               
'''

from copy import deepcopy

eval_metics = {"precision": 0,
               "recall": 0,
               "f1_score": 0,
               'count': 0
               }

EvalByType = {"strict": deepcopy(eval_metics),
              "exact": deepcopy(eval_metics),
              "partial": deepcopy(eval_metics),
              "type": deepcopy(eval_metics), }

# evaluation metrics in total
OverallEval = {}


def calc_partial_match_evaluation_per_line(prediction: list, goldenStandard: list, text: str, domain_name: str):
    """
    Calculate detailed partial evaluation metric. See Evaluation of the SemEval-2013 Task 9.1
    :param prediction (list): (k, v) -> (slot tags, slot contents)
    :param goldenStandard (dict): (k, v) -> (slot tags, slot contents)
    :return: eval_results (dict)
    """
    # if no label and no prediction, reguard as all correct!
    if len(prediction) == 0 and len(goldenStandard) == 0:
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
    else:
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

        for pred_tag, pred_val in prediction:
            # exact match, i.e. both entity boundary and entity type match
            # scenario 1
            if check_Scenario1(pred_tag, pred_val, goldenStandard):
                # 'strict' matching
                eval_results['strict']['correct'] += 1
                eval_results['type']['correct'] += 1
                eval_results['exact']['correct'] += 1
                eval_results['partial']['correct'] += 1

            # partial match
            # scenario 5
            elif check_Scenario5(pred_tag, pred_val, goldenStandard, text):
                # exact boundary matching
                eval_results['strict']['incorrect'] += 1
                eval_results['exact']['incorrect'] += 1
                eval_results['partial']['partial'] += 1
                eval_results['type']['correct'] += 1

            # scenario 4: same pred value，entity type disagree
            elif check_Scenario4(pred_tag, pred_val, goldenStandard):
                eval_results['strict']['incorrect'] += 1
                eval_results['exact']['correct'] += 1
                eval_results['partial']['correct'] += 1
                eval_results['type']['incorrect'] += 1

            # scenario 6 : overlap exists, but tags disagree
            elif check_Scenario6(pred_tag, pred_val, goldenStandard, text):
                eval_results['strict']['incorrect'] += 1
                eval_results['exact']['correct'] += 1
                eval_results['partial']['correct'] += 1
                eval_results['type']['incorrect'] += 1

            # predictee not exists in golden standard
            # scenario 2: SPU, predicted entity not exists in golden, and no overlap on entity boundary
            elif check_Scenario2(pred_tag, pred_val, goldenStandard, text):
                eval_results['strict']['spurius'] += 1
                eval_results['exact']['spurius'] += 1
                eval_results['partial']['spurius'] += 1
                eval_results['type']['spurius'] += 1

        for true_tag, true_val in goldenStandard:
            if check_Scenario3(true_tag, true_val, prediction, text):
                # count missing
                eval_results['strict']['missed'] += 1
                eval_results['exact']['missed'] += 1
                eval_results['partial']['missed'] += 1
                eval_results['type']['missed'] += 1

        # calculate P, R, F1
        # POS = len(goldenStandard)
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

    # update evaluation result
    if domain_name not in OverallEval:
        OverallEval.update({domain_name: EvalByType})

    for mode in eval_results:
        OverallEval[domain_name][mode]["precision"] += eval_results[mode]["precision"]
        OverallEval[domain_name][mode]["recall"] += eval_results[mode]["recall"]
        OverallEval[domain_name][mode]["f1_score"] += eval_results[mode]["f1_score"]


def check_Scenario1(pred_tag: str, pred_val: str, goldenStandard: list):
    # scenario 1: both entity type and entity boundary strictly match
    COR_list = [1 for true_tag, true_val in goldenStandard if true_tag == pred_tag and true_val == pred_val]
    if len(COR_list) > 0:
        return True
    else:
        return False


def check_Scenario5(pred_tag: str, pred_val: str, goldenStandard: list, text: str):
    # scenario 5: same entity type and entity boundary overlap
    for true_tag, true_val in goldenStandard:
        if pred_tag == true_tag and checkIfOverlap(true_val, pred_val, text):
            return True
    return False


def check_Scenario2(pred_tag: str, pred_val: str, goldenStandard: list, text: str):
    # scenario 2: SPU, predicted entity type not exists in golden, and no overlap on entity boundary
    for true_tag, true_val in goldenStandard:
        if checkIfOverlap(true_val, pred_val, text):
            return False
    return True


def check_Scenario3(true_tag: str, true_val: str, prediction: list, text: str):
    # Missed
    # scenario 3:entity boundary not overlap,  golden standard not exists in prediction
    for pred_tag, pred_val in prediction:
        if checkIfOverlap(true_val, pred_val, text):
            return False
    return True


def check_Scenario4(pred_tag: str, pred_val: str, goldenStandard: list):
    # scenario 4: same pred value，entity type disagree
    for true_tag, true_val in goldenStandard:
        if true_val == pred_val and true_tag != pred_tag:
            return True
    return False


def check_Scenario6(pred_tag: str, pred_val: str, goldenStandard: list, text: str):
    # scenario 6: entity boundary overlap, entity type disagree
    for true_tag, true_val in goldenStandard:
        if checkIfOverlap(true_val, pred_val, text) and true_tag != pred_tag:
            return True
    return False


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


def calc_overall_evaluation(count_by_type_dict: dict):
    """
    Evaluation summary by domain type
    :param count_by_type_dict: {k:v}  key->domain_name, value-> count number by domain name
    :return:
    """
    assert len(count_by_type_dict) > 0, "count by domain class should not be empty!"
    for domain_name, domain_cnt in count_by_type_dict.items():
        for mode, res in OverallEval[domain_name].items():
            OverallEval[domain_name][mode]['precision'] = res['precision'] / domain_cnt
            OverallEval[domain_name][mode]['recall'] = res['recall'] / domain_cnt
            OverallEval[domain_name][mode]['f1_score'] = res['f1_score'] / domain_cnt
            print("Domain:{}, mode:{}, P:{:.3f}, R:{:.3f}, f1:{:.3f}".format(
                domain_name, mode, OverallEval[domain_name][mode]['precision'],
                OverallEval[domain_name][mode]['recall'],
                OverallEval[domain_name][mode]['f1_score']))
    return OverallEval
