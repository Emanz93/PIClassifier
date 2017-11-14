library(caret);
library(rpart);
library(e1071);
source("functions.R");

# I need to oversampling the 0 class of the dataset.
breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");
breath = read.csv(breath_names[[1]]);
for (i in 2:length(breath_names)) {
  breath = rbind(breath, read.csv(breath_names[[i]]));
}

#split the dataset
ok_breath = NULL;
an_breath = NULL;
for(i in 1:nrow(breath)){
  if(breath[i,1] == 0) {
    an_breath = rbind(an_breath, breath[i,]);
  } else {
    ok_breath = rbind(ok_breath, breath[i,]);
  }
}

# sampling
an_idxs = sample(1:nrow(an_breath), 500, replace = TRUE);
ok_idxs = sample(1:nrow(ok_breath), 500);

balanced_breath = NULL;
for(i in 1:length(an_idxs)) {
  balanced_breath = rbind(balanced_breath, an_breath[an_idxs[i],]);
  balanced_breath = rbind(balanced_breath, ok_breath[ok_idxs[i],]);
}

#as.data.frame(balanced_breath);

# debug
ok = 0;
an = 0;
for(i in 1:nrow(balanced_breath)) {
  if(balanced_breath[i,1] == 0) {
    an = an + 1;
  } else {
    ok = ok + 1;
  }
}

# k folding
k=6;
k_folds <- createFolds(1:nrow(balanced_breath), k, list = TRUE, returnTrain = FALSE);

# accumulators
DT_acc = c();
DT_TPR = c();
DT_TNR = c();
DT_PR = c();
SVM_acc = c();
SVM_TPR = c();
SVM_TNR = c();
SVM_PR = c();

for(i in 1:k) {
  test_indexes = k_folds[[i]];
  train_indexes = NULL;
  for(j in 1:k) {
    if(i != j) {
      train_indexes = c(test_indexes, k_folds[[j]]);
    }
  }
  
  # training
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max, data = data.frame(balanced_breath[train_indexes,1:18]),
                     method = 'class');
  # before_concavity_counter+  before_area_1+before_area_2+before_area_3+after_concavity_counter+after_area_1
  breath_svm <- svm(balanced_breath[train_indexes, 2:18], y = balanced_breath[train_indexes, 1]);
  
  # testing
  breath_res_dt = predict(breath_dt, balanced_breath[test_indexes, 2:18], type='class');
  cm_breath_dt = get_confusion_matrix(balanced_breath[test_indexes,], breath_res_dt);
  
  breath_res_svm = predict(breath_svm, balanced_breath[test_indexes, 2:18], type='class');
  cm_breath_svm = get_confusion_matrix(balanced_breath[test_indexes,], round(breath_res_svm));
  
  # print
  acc = (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(balanced_breath[test_indexes,]);
  DT_acc = c(DT_acc, acc);
  
  TNR = cm_breath_dt[1,1]/(cm_breath_dt[1,1] + cm_breath_dt[1,2]);
  DT_TNR = c(DT_TNR, TNR);
  
  TPR = cm_breath_dt[2,2]/(cm_breath_dt[2,1] + cm_breath_dt[2,2]);
  DT_TPR = c(DT_TPR, TPR);
  
  PR = cm_breath_dt[2,2]/(cm_breath_dt[1,2]+cm_breath_dt[2,2]);
  DT_PR = c(DT_PR, PR);
  
  cat('iteration ', i, '\n');
  cat('Decision Tree\n');
  print(cm_breath_dt);
  cat("DT Accuracy= ", acc, '\n');
  cat("DT TN Rate =   ", TNR, "\n");
  cat("DT TP Rate =   ", TPR, "\n");
  cat("DT PR Rate =   ", PR, "\n");
  cat('\n');
  
  acc = (cm_breath_svm[1,1]+cm_breath_svm[2,2]) / nrow(balanced_breath[test_indexes,]);
  SVM_acc = c(SVM_acc, acc);
  
  TPR = cm_breath_svm[2,2]/(cm_breath_svm[2,1] + cm_breath_svm[2,2]);
  SVM_TPR = c(SVM_TPR, TPR);
  
  TNR = cm_breath_svm[1,1]/(cm_breath_svm[1,1] + cm_breath_svm[1,2]);
  SVM_TNR = c(SVM_TNR, TNR);
  
  PR = cm_breath_svm[2,2]/(cm_breath_svm[1,2]+cm_breath_svm[2,2]);
  SVM_PR = c(SVM_PR, PR);
  
  cat('SVM\n');
  print(cm_breath_svm);
  cat("SVM Accuracy=   ", acc, '\n');
  cat("SVM TN Rate =   ", TNR, "\n");
  cat("SVM TP Rate =   ", TPR, "\n");
  cat("SVM PR Rate =   ", PR, "\n");
  cat('-------------\n\n');
}

cat("FINAL RESULTS - OVERSAMPLING\n\n");
cat("DT Average Accuracy = ", mean(DT_acc));
cat("DT Accuracy Variance =", var(DT_acc));
cat("DT Average TP Rate =", mean(DT_TPR));
cat("DT TP Rate Variance =", var(DT_TPR));
cat("DT Average TN Rate =", mean(DT_TNR));
cat("DT TN Rate Variance =", var(DT_TNR));
cat("DT Average PR Rate =", mean(DT_PR));
cat("DT PR Rate Variance =", var(DT_PR));

cat("SVM Mean Accuracy = ", mean(SVM_acc));
cat("SVM Variance Accuracy =", var(SVM_acc));
cat("SVM Average TP Rate =", mean(SVM_TPR));
cat("SVM TP Rate Variance =", var(SVM_TPR));
cat("SVM Average TN Rate =", mean(SVM_TNR));
cat("SVM TN Rate Variance =", var(SVM_TNR));
cat("SVM Average PR Rate =", mean(SVM_PR));
cat("SVM PR Rate Variance =", var(SVM_PR));




