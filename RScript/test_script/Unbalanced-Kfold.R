# Loading of libraries and dataset.
library(caret);
library(rpart);
library(e1071);
source("functions.R");

breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");

breath = read.csv(breath_names[[1]]);
for (i in 2:length(breath_names)) {
  breath = rbind(breath, read.csv(breath_names[[i]]));
}

# Accumulators
DT_acc = c();
DT_TPR = c();
DT_TNR = c();
SVM_acc = c();
SVM_TPR = c();
SVM_TNR = c();

# k-fold
k=10;
k_folds <- createFolds(1:nrow(breath), k, list = TRUE, returnTrain = FALSE);

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
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1, data = breath[train_indexes,1:18],
                       method = 'class');
  breath_svm <- svm(breath[train_indexes, 2:18], y = breath[train_indexes, 1])
  
  # testing
  breath_res_dt = predict(breath_dt, breath[test_indexes, 2:18], type='class');
  cm_breath_dt = get_confusion_matrix(breath[test_indexes,], breath_res_dt)
  
  breath_res_svm = predict(breath_svm, breath[test_indexes, 2:18]);
  cm_breath_svm = get_confusion_matrix(breath[test_indexes,], round(breath_res_svm));
  
  
  # print
  cat('iteration ', i, '\n\n');
  
  # Decision tree summary
  cat('Decision Tree\n');
  print(cm_breath_dt);
  acc = (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(breath[test_indexes,]);
  DT_acc = c(DT_acc, acc);
  cat("DT Accuracy= ", acc, '\n');
  TPR = cm_breath_dt[2,2]/(cm_breath_dt[2,1] + cm_breath_dt[2,2]);
  TNR = cm_breath_dt[1,1]/(cm_breath_dt[1,1] + cm_breath_dt[1,2]);
  DT_TPR = c(DT_TPR, TPR);
  DT_TNR = c(DT_TNR, TNR)
  cat("DT TN Rate =   ", TNR, "\n");
  cat("DT TP Rate =   ", TPR, "\n");
  cat('\n');
  
  # SVM summary
  cat('SVM\n');
  print(cm_breath_svm);
  acc = (cm_breath_svm[1,1]+cm_breath_svm[2,2]) / nrow(breath[test_indexes,]);
  SVM_acc = c(SVM_acc, acc);
  cat("SVM Accuracy=   ", acc, '\n');
  TPR = cm_breath_svm[2,2]/(cm_breath_svm[2,1] + cm_breath_svm[2,2]);
  TNR = cm_breath_svm[1,1]/(cm_breath_svm[1,1] + cm_breath_svm[1,2]);
  SVM_TNR = c(SVM_TNR, TNR);
  SVM_TPR = c(SVM_TPR, TPR);
  cat("SVM TN Rate =   ", TNR, "\n");
  cat("SVM TP Rate =   ", TPR, "\n");
  cat('-------------\n\n');
}

cat("FINAL RESULTS\n\n");
cat("DT Average Accuracy = ", mean(DT_acc));
cat("DT Accuracy Variance = ", var(DT_acc));
cat("DT Average TP Rate = ", mean(DT_TPR));
cat("DT TP Rate Variance = ", var(DT_TPR));
cat("DT Average TN Rate = ", mean(DT_TNR));
cat("DT TN Rate Variance = ", var(DT_TNR));

cat("SVM Mean Accuracy = ", mean(SVM_acc));
cat("SVM Variance Accuracy = ", var(SVM_acc));
cat("SVM Average TP Rate = ", mean(SVM_TPR));
cat("SVM TP Rate Variance = ", var(SVM_TPR));
cat("SVM Average TN Rate = ", mean(SVM_TNR));
cat("SVM TN Rate Variance = ", var(SVM_TNR));


