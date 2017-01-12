import os

input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'input')
cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cache')


full_split = (os.path.join(input_dir, 'clicks_train.csv.gz'), os.path.join(input_dir, 'clicks_test.csv.gz'))

cv1_split = (os.path.join(cache_dir, 'clicks_cv1_train.csv.gz'), os.path.join(cache_dir, 'clicks_cv1_test.csv.gz'))
cv1_split_idx = (os.path.join(cache_dir, 'clicks_cv1_train_idx.csv.gz'), os.path.join(cache_dir, 'clicks_cv1_test_idx.csv.gz'))

cv2_split = (os.path.join(cache_dir, 'clicks_cv2_train.csv.gz'), os.path.join(cache_dir, 'clicks_cv2_test.csv.gz'))

cv1_split_time = 950400000
test_split_time = 1123200000
