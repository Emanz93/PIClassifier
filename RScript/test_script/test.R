library(caret);
library(rpart);
library(e1071);

breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");
breath = read.csv(breath_names[[1]]);
for (i in 2:length(breath_names)) {
  breath = rbind(breath, read.csv(breath_names[[i]]));
}

k=10;
k_folds <- createFolds(1:nrow(breath), k, list = TRUE, returnTrain = FALSE);

DT_acc = c();
SVM_acc = c();

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
                       intercetta+integral_after_max, data = breath[train_indexes,1:12],
                       method = 'class');
  # before_concavity_counter+  before_area_1+before_area_2+before_area_3+after_concavity_counter+after_area_1
  breath_svm <- svm(breath[train_indexes, 2:12], y = breath[train_indexes, 1])
  
  # testing
  breath_res_dt = predict(breath_dt, breath[test_indexes, 2:12], type='class');
  cm_breath_dt = table(pred=breath_res_dt, true=breath[test_indexes,1]);
  
  breath_res_svm = predict(breath_svm, breath[test_indexes, 2:12]);
  cm_breath_svm = table(pred=round(breath_res_svm), true=breath[test_indexes,1]);
  
  
  # print
  cat('iteration ', i, '\n\n');
  cat('Decision Tree\n');
  print(cm_breath_dt);
  acc = (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(breath[test_indexes,]);
  DT_acc = c(DT_acc, acc);
  cat("DT Accuracy= ", acc, '\n');
  cat("DT Error Rate= ", (1 - (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(breath[test_indexes,])), '\n');
  cat("SVM TN Rate =   ", cm_breath_dt[1,1]/(cm_breath_dt[1,1] + cm_breath_dt[1,2]), "\n");
  cat("SVM TP Rate =   ", cm_breath_dt[2,2]/(cm_breath_dt[2,1] + cm_breath_dt[2,2]), "\n");
  cat('\n');
  cat('SVM\n');
  print(cm_breath_svm);
  acc = (cm_breath_svm[1,1]+cm_breath_svm[2,2]) / nrow(breath[test_indexes,]);
  SVM_acc = c(SVM_acc, acc);
  cat("SVM Accuracy=   ", acc, '\n');
  cat("SVM Error Rate= ", (1 - (cm_breath_svm[1,1]+cm_breath_svm[2,2]) / nrow(breath[test_indexes,])), '\n');
  cat("SVM TN Rate =   ", cm_breath_svm[1,1]/(cm_breath_svm[1,1] + cm_breath_svm[1,2]), "\n");
  cat("SVM TP Rate =   ", cm_breath_svm[2,2]/(cm_breath_svm[2,1] + cm_breath_svm[2,2]), "\n");
  cat('-------------\n\n');
}

cat("DT Average Accuracy = ", mean(DT_acc));
cat("DT Accuracy Variance =", var(DT_acc));

cat("SVM Mean Accuracy = ", mean(SVM_acc));
cat("SVM Variance Accuracy =", var(SVM_acc));
