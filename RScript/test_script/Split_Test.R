# I want to see if the oversampling approach is better than a random k-fold.
# I do this with k-fold with k=6, testing the model on all dataset wich I have.

library(caret);
library(rpart);
library(e1071);
source("functions.R");




breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");

# Accumulators
DT_acc_UN = c();
DT_TPR_UN = c();
DT_TNR_UN = c();
DT_PR_UN = c();
SVM_acc_UN = c();
SVM_TPR_UN = c();
SVM_TNR_UN = c();
SVM_PR_UN = c();

DT_acc_BA = c();
DT_TPR_BA = c();
DT_TNR_BA = c();
DT_PR_BA = c();
SVM_acc_BA = c();
SVM_TPR_BA = c();
SVM_TNR_BA = c();
SVM_PR_BA = c();

k = 6;
for(i in 1:k) {
  breath_test = read.csv(breath_names[[i]]);
  # breath -> unbalanced dataset
  breath = NULL;
  for(j in 1:k) {
    if (j != i) {
      breath = rbind(breath, read.csv(breath_names[[j]]));
    }
  }
  
  # breath_balanced -> balanced dataset
  #split the dataset
  ok_breath = NULL;
  an_breath = NULL;
  for(index in 1:nrow(breath)){
    if(breath[index,1] == 0) {
      an_breath = rbind(an_breath, breath[index,]);
    } else {
      ok_breath = rbind(ok_breath, breath[index,]);
    }
  }
  
  # sampling
  an_idxs = sample(1:nrow(an_breath), 440, replace = TRUE);
  ok_idxs = sample(1:nrow(ok_breath), 440);
  
  balanced_breath = NULL;
  for(index in 1:length(an_idxs)) {
    balanced_breath = rbind(balanced_breath, an_breath[an_idxs[index],]);
    balanced_breath = rbind(balanced_breath, ok_breath[ok_idxs[index],]);
  }
  
  # training UNBALANCED -> train_indexes = 1:nrow(breath);
  breath_dt_UN <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1, data = breath[,1:18],
                     method = 'class');
  breath_svm_UN <- svm(breath[, 2:18], y = breath[, 1]);
  
  # Training BALANCED
  breath_dt_BA <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1, data = balanced_breath[,1:18],
                     method = 'class');
  breath_svm_BA <- svm(balanced_breath[, 2:18], y = balanced_breath[, 1])
  
  
  
  
  # testing UNBALANCED
  breath_res_dt_UN = predict(breath_dt_UN, breath_test[, 2:18], type='class');
  cm_breath_dt_UN = get_confusion_matrix(breath_test, breath_res_dt_UN);
  
  breath_res_svm_UN = predict(breath_svm_UN, breath_test[, 2:18], type='class');
  cm_breath_svm_UN = get_confusion_matrix(breath_test, round(breath_res_svm_UN));
  
  # testing BALANCED
  breath_res_dt_BA = predict(breath_dt_BA, breath_test[, 2:18], type='class');
  cm_breath_dt_BA = get_confusion_matrix(breath_test, breath_res_dt_BA);
  
  breath_res_svm_BA = predict(breath_svm_BA, breath_test[, 2:18], type='class');
  cm_breath_svm_BA = get_confusion_matrix(breath_test, round(breath_res_svm_BA));
  
  
  
  # print UNBALANCED PART
  # Decision tree summary UNBALANCED
  acc = (cm_breath_dt_UN[1,1]+cm_breath_dt_UN[2,2]) / nrow(breath_test[,]);
  DT_acc_UN = c(DT_acc_UN, acc);
  
  TPR = cm_breath_dt_UN[2,2]/(cm_breath_dt_UN[2,1] + cm_breath_dt_UN[2,2]);
  DT_TPR_UN = c(DT_TPR_UN, TPR);
  
  TNR = cm_breath_dt_UN[1,1]/(cm_breath_dt_UN[1,1] + cm_breath_dt_UN[1,2]);
  DT_TNR_UN = c(DT_TNR_UN, TNR);
  
  PR = cm_breath_dt_UN[2,2]/(cm_breath_dt_UN[1,2]+cm_breath_dt_UN[2,2]);
  DT_PR_UN = c(DT_PR_UN, PR);
  
  cat('iteration ', i, '\n\n');
  cat('Decision Tree UNBALANCED\n');
  print(cm_breath_dt_UN);
  cat("DT Accuracy=   ", acc, '\n');
  cat("DT TN Rate =   ", TNR, "\n");
  cat("DT TP Rate =   ", TPR, "\n");
  cat("DT PR Rate =   ", PR, "\n");
  cat('\n');
  
  # SVM summary UNBALANCED
  acc = (cm_breath_svm_UN[1,1]+cm_breath_svm_UN[2,2]) / nrow(breath_test[,]);
  SVM_acc_UN = c(SVM_acc_UN, acc);
  
  TPR = cm_breath_svm_UN[2,2]/(cm_breath_svm_UN[2,1] + cm_breath_svm_UN[2,2]);
  SVM_TPR_UN = c(SVM_TPR_UN, TPR);
  
  TNR = cm_breath_svm_UN[1,1]/(cm_breath_svm_UN[1,1] + cm_breath_svm_UN[1,2]);
  SVM_TNR_UN = c(SVM_TNR_UN, TNR);
  
  PR = cm_breath_svm_UN[2,2]/(cm_breath_svm_UN[1,2]+cm_breath_svm_UN[2,2]);
  SVM_PR_UN = c(SVM_PR_UN, PR);
  
  
  cat('SVM UNBALANCED\n');
  print(cm_breath_svm_UN);
  cat("SVM Accuracy=   ", acc, '\n');
  cat("SVM TN Rate =   ", TNR, "\n");
  cat("SVM TP Rate =   ", TPR, "\n");
  cat("SVM PR Rate =   ", PR, "\n");
  cat('-------------\n\n');
  
  
  
  # print BALANCED PART
  # Decision tree summary BALANCED
  acc = (cm_breath_dt_BA[1,1]+cm_breath_dt_BA[2,2]) / nrow(breath_test[,]);
  DT_acc_BA = c(DT_acc_BA, acc);
  
  TPR = cm_breath_dt_BA[2,2]/(cm_breath_dt_BA[2,1] + cm_breath_dt_BA[2,2]);
  DT_TPR_BA = c(DT_TPR_BA, TPR);
  
  TNR = cm_breath_dt_BA[1,1]/(cm_breath_dt_BA[1,1] + cm_breath_dt_BA[1,2]);
  DT_TNR_BA = c(DT_TNR_BA, TNR);
  
  PR = cm_breath_dt_BA[2,2]/(cm_breath_dt_BA[1,2]+cm_breath_dt_BA[2,2]);
  DT_PR_BA = c(DT_PR_BA, PR);
  
  cat('Decision Tree BALANCED\n');
  print(cm_breath_dt_BA);
  cat("DT Accuracy=   ", acc, '\n');
  cat("DT TN Rate =   ", TNR, "\n");
  cat("DT TP Rate =   ", TPR, "\n");
  cat("DT PR Rate =   ", PR, "\n");
  cat('\n');
  
  # SVM summary BALANCED
  acc = (cm_breath_svm_BA[1,1]+cm_breath_svm_BA[2,2]) / nrow(breath_test[,]);
  SVM_acc_BA = c(SVM_acc_BA, acc);
  
  TPR = cm_breath_svm_BA[2,2]/(cm_breath_svm_BA[2,1] + cm_breath_svm_BA[2,2]);
  SVM_TPR_BA = c(SVM_TPR_BA, TPR);
  
  TNR = cm_breath_svm_BA[1,1]/(cm_breath_svm_BA[1,1] + cm_breath_svm_BA[1,2]);
  SVM_TNR_BA = c(SVM_TNR_BA, TNR);
  
  PR = cm_breath_svm_BA[2,2]/(cm_breath_svm_BA[1,2]+cm_breath_svm_BA[2,2]);
  SVM_PR_BA = c(SVM_PR_BA, PR);
  
  cat('SVM BALANCED\n');
  print(cm_breath_svm_BA);
  cat("SVM Accuracy=   ", acc, '\n');
  cat("SVM TN Rate =   ", TNR, "\n");
  cat("SVM TP Rate =   ", TPR, "\n");
  cat("SVM PR Rate =   ", PR, "\n");
  cat('-------------\n\n');
}

cat("FINAL SUMMARY - SPLIT TEST\n\n");
cat("UNBALANCED DATASET:\n");
cat("\tDT Average Accuracy = ", mean(DT_acc_UN));
cat("\tDT Accuracy Variance = ", var(DT_acc_UN));
cat("\tDT Average TP Rate = ", mean(DT_TPR_UN));
cat("\tDT TP Rate Variance = ", var(DT_TPR_UN));
cat("\tDT Average TN Rate = ", mean(DT_TNR_UN));
cat("\tDT TN Rate Variance = ", var(DT_TNR_UN));
cat("\tDT Average PR Rate =", mean(DT_PR_UN));
cat("\tDT PR Rate Variance =", var(DT_PR_UN));


cat("\tSVM Mean Accuracy = ", mean(SVM_acc_UN));
cat("\tSVM Variance Accuracy = ", var(SVM_acc_UN));
cat("\tSVM Average TP Rate = ", mean(SVM_TPR_UN));
cat("\tSVM TP Rate Variance = ", var(SVM_TPR_UN));
cat("\tSVM Average TN Rate = ", mean(SVM_TNR_UN));
cat("\tSVM TN Rate Variance = ", var(SVM_TNR_UN));
cat("\tSVM Average PR Rate =", mean(SVM_PR_UN));
cat("\tSVM PR Rate Variance =", var(SVM_PR_UN));

cat("\n\nBALANCED DATASET:\n");
cat("\tDT Average Accuracy = ", mean(DT_acc_BA));
cat("\tDT Accuracy Variance = ", var(DT_acc_BA));
cat("\tDT Average TP Rate = ", mean(DT_TPR_BA));
cat("\tDT TP Rate Variance = ", var(DT_TPR_BA));
cat("\tDT Average TN Rate = ", mean(DT_TNR_BA));
cat("\tDT TN Rate Variance = ", var(DT_TNR_BA));
cat("\tDT Average PR Rate =", mean(DT_PR_BA));
cat("\tDT PR Rate Variance =", var(DT_PR_BA));


cat("\tSVM Mean Accuracy = ", mean(SVM_acc_BA));
cat("\tSVM Variance Accuracy = ", var(SVM_acc_BA));
cat("\tSVM Average TP Rate = ", mean(SVM_TPR_BA));
cat("\tSVM TP Rate Variance = ", var(SVM_TPR_BA));
cat("\tSVM Average TN Rate = ", mean(SVM_TNR_BA));
cat("\tSVM TN Rate Variance = ", var(SVM_TNR_BA));
cat("\tSVM Average PR Rate =", mean(SVM_PR_BA));
cat("\tSVM PR Rate Variance =", var(SVM_PR_BA));


