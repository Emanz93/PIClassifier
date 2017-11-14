# I want to see if the oversampling approach is better than a random k-fold.
# I do this with k-fold with k=6, testing the model on all dataset wich I have.

library(rpart);
source("functions.R");

breath_names = list("dataset1.csv", "dataset2.csv", 
                    "dataset3.csv","dataset4.csv", 
                    "dataset4.csv", "dataset5.csv", 
                    "dataset6.csv");

# normal dataset
breath = read.csv(breath_names[[1]]);
for (i in 2:length(breath_names)) {
  breath = rbind(breath, read.csv(breath_names[[i]]));
}

# Accumulators
DT_acc = c();
DT_TPR = c();
DT_TNR = c();
DT_mode = c();

k = 6;
for(i in 1:k) {
  breath_test = read.csv(breath_names[[i]]);
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                        resp_rate+rr_over_tv+etco2+first_value+last_value+
                        intercetta+integral_after_max+before_concavity_counter+
                        before_area_1+before_area_2+before_area_3+
                        after_concavity_counter+after_area_1+after_area_2+after_area_3, data = breath[,1:20],
                      method = 'class');
  
  breath_res_dt = predict(breath_dt, breath_test[, 2:20], type='class');
  cm_breath_dt = get_confusion_matrix(breath_test, breath_res_dt);
  
  # print UNBALANCED PART
  cat('iteration ', i, '\n\n');
  # Decision tree summary UNBALANCED
  print(cm_breath_dt);
  acc = (cm_breath_dt[1,1]+cm_breath_dt[2,2]) / nrow(breath_test[,]);
  DT_acc = c(DT_acc, acc);
  cat("DT Accuracy= ", acc, '\n');
  TPR = cm_breath_dt[2,2]/(cm_breath_dt[2,1] + cm_breath_dt[2,2]);
  TNR = cm_breath_dt[1,1]/(cm_breath_dt[1,1] + cm_breath_dt[1,2]);
  DT_TPR = c(DT_TPR, TPR);
  DT_TNR = c(DT_TNR, TNR);
  cat("TN Rate =   ", TNR, "\n");
  cat("TP Rate =   ", TPR, "\n");
  cat('\n');
}

cat("FINAL SUMMARY:\n\n");
cat("UNBALANCED DATASET:\n");
cat("\tDT Average Accuracy = ", mean(DT_acc));
cat("\tDT Accuracy Variance = ", var(DT_acc));
cat("\tDT Average TP Rate = ", mean(DT_TPR));
cat("\tDT TP Rate Variance = ", var(DT_TPR));
cat("\tDT Average TN Rate = ", mean(DT_TNR));
cat("\tDT TN Rate Variance = ", var(DT_TNR));
