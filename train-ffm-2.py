import numpy as np
import pandas as pd

import os
import argparse

from util.meta import full_split, val_split
from util import gen_prediction_name, gen_submission, score_prediction, print_and_exec


def fit_predict(profile, split, split_name):
    opts = profile['options']

    train_file = 'cache/%s_train_bin_%s' % (split_name, opts['dataset'])
    pred_file = 'cache/%s_test_bin_%s' % (split_name, opts['dataset'])

    if split_name == "val":
        opts += " --val %s" % pred_file

    print_and_exec("bin/ffm %s --train %s --test %s --pred  /tmp/ffm2.preds" % (opts, train_file, pred_file))

    pred = pd.read_csv(split[1])
    pred['pred'] = np.loadtxt('/tmp/ffm2.preds')

    return pred


profiles = {
    'p1': {
        'options': "--epochs 7",
        'dataset': "p1",
    },

    'p1r': {
        'options': "--epochs 7 --restricted",
        'dataset': "p1",
    },
}


parser = argparse.ArgumentParser(description='Train FFM2 model')
parser.add_argument('profile', type=str, help='Train profile')
parser.add_argument('--rewrite-cache', action='store_true', help='Drop cache files prior to train')

args = parser.parse_args()
profile = profiles[args.profile]


if not os.path.exists('cache/val_train_ffm_2.index') or args.rewrite_cache:
    print "Generating data..."
    os.system("bin/export-ffm-data-2")


## Validation

print "Validation split..."

pred = fit_predict(profile, val_split, 'val')

print "  Scoring..."

present_score, future_score, score = score_prediction(pred)
name = gen_prediction_name('ffm2-%s' % args.profile, score)

print "  Present score: %.5f" % present_score
print "  Future score: %.5f" % future_score
print "  Total score: %.5f" % score

pred[['pred']].to_pickle('preds/%s-val.pickle' % name)

del pred

## Prediction

print "Full split..."

pred = fit_predict(profile, full_split, 'full')
pred[['pred']].to_pickle('preds/%s-test.pickle' % name)

print "  Generating submission..."
subm = gen_submission(pred)
subm.to_csv('subm/%s.csv.gz' % name, index=False, compression='gzip')

del pred, subm

print "  File name: %s" % name
print "Done."
