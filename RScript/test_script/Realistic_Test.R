library(caret);
library(rpart);
library(e1071);
source("functions.R");

breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");


# TEST 1 - Realistic Test.
# Test con cross validation (k-fold, k=6) "paziente per paziente".

# Accumulators
DT_acc = c();
DT_TPR = c();
DT_TNR = c();
DT_PR = c();
SVM_acc = c();
SVM_TNR = c();
SVM_TPR = c();
SVM_PR = c();

# k-fold
k = 6;

for (i in 1:k) {
  # Selecting fold.
  breath_test = read.csv(breath_names[[i]]);
  breath_learning = NULL;
  for(j in 1:k) {
    if (j != i) {
      breath_learning = rbind(breath_learning, read.csv(breath_names[[j]]));
    }
  }
  
  # training
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1, data = breath_learning[,1:18], method = 'class');
  breath_svm <- svm(breath_learning[, 2:18], y = breath_learning[, 1])
  
  # testing
  breath_res_dt = predict(breath_dt, breath_test[, 2:18], type='class');
  cm_breath_dt = get_confusion_matrix(breath_test, breath_res_dt);
  
  breath_res_svm = predict(breath_svm, breath_test[, 2:18]);
  cm_breath_svm = get_confusion_matrix(breath_test, round(breath_res_svm));
  
  
  # print
  cat('iteration ', i, '\n\n');
  
  # Decision tree summary
  acc = (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(breath_test[,]);
  DT_acc = c(DT_acc, acc);
  
  acc = (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(breath_test[,]);
  DT_acc = c(DT_acc, acc);
  
  TNR = cm_breath_dt[1,1]/(cm_breath_dt[1,1] + cm_breath_dt[1,2]);
  DT_TNR = c(DT_TNR, TNR);
  
  TPR = cm_breath_dt[2,2]/(cm_breath_dt[2,1] + cm_breath_dt[2,2]);
  DT_TPR = c(DT_TPR, TPR);
  
  PR = cm_breath_dt[2,2]/(cm_breath_dt[1,2]+cm_breath_dt[2,2]);
  DT_PR = c(DT_PR, PR);
  
  cat('Decision Tree\n');
  print(cm_breath_dt);
  cat("DT Accuracy= ", acc, '\n');
  cat("DT TN Rate = ", TNR, "\n");
  cat("DT TP Rate = ", TPR, "\n");
  cat("DT PR Rate = ", PR, "\n");
  cat('\n');
  
  # SVM summary
  acc = (cm_breath_svm[1,1]+cm_breath_svm[2,2]) / nrow(breath_test[,]);
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

cat("FINAL RESULTS - REALISTIC TEST\n\n");
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


