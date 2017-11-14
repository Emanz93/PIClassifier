library(rpart);
source("functions.R");

breath_names_learn = list("dataset1.csv", "dataset2.csv", "dataset3.csv",
                          "dataset4.csv", "dataset5.csv", "dataset6.csv");

breath_names_test = list("p_03_01_nava_08.csv", "p_04_01_nava_06.csv", "p_05_01_nava_10.csv",
                         "p_06_01_nava_10.csv", "p_07_01_nava_10.csv", "p_08_01_nava_05.csv");

# normal dataset
breath_learning = read.csv(breath_names_learn[[1]]);
for (i in 2:length(breath_names_learn)) {
  breath_learning = rbind(breath_learning, read.csv(breath_names_learn[[i]]));
}

for(i in 1:length(breath_names_learn)) {
  breath_test = read.csv(breath_names_learn[[i]]);
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1+after_area_2+after_area_3, data = breath_learning,
                     method = 'class');
  
  breath_res = predict(breath_dt, breath_test[, 2:20], type='prob');
  breath_res_class = predict(breath_dt, breath_test[, 2:20], type='class');
  breath_res_2 = matrix(breath_res, ncol = 2 , byrow = FALSE);
  res = c();
  for(k in 1:length(breath_res_2[,2])) {
    res = c(res, breath_res_2[k,2]);
  }
  ok_count = 0;
  an_count = 0;
  doub_count = 0;
  tot = 0;
  
  th_1 = 0.2;
  th_2 = 1 - th_1;
  
  class_res = c();
  for(j in 1:length(res)) {
    if(res[j] > 0.8) {
      class_res = c(class_res, 1);
      ok_count = ok_count + 1;
    } else if(res[j] < 0.2) {
      class_res = c(class_res, 0);
      an_count = an_count + 1;
    } else {
      class_res = c(class_res, 2);
      doub_count = doub_count + 1;
    }
    tot = tot + 1;
  }
  
  # 
  
  cm = table(true=breath_test[,1], pred=class_res);
  if(doub_count != 0) {
    print(cm);
  } else {
    cm_breath_dt = get_confusion_matrix(breath_test, class_res);
    print(cm_breath_dt);
    TPR = cm_breath_dt[2,2]/(cm_breath_dt[2,1] + cm_breath_dt[2,2]);
    TNR = cm_breath_dt[1,1]/(cm_breath_dt[1,1] + cm_breath_dt[1,2]);
    cat("TN Rate = ", TNR, "\n");
    cat("TP Rate = ", TPR, "\n");
  }
  
  cat("Dub Count= ", doub_count, "\n");
  cat("Dub Rate = ", doub_count / length(res) ,"\n");
  #cat("TN Rate  = ", TNR, "\n");
  #cat("TP Rate  = ", TPR, "\n");
  cat(" Min.    1st Qu Median  Mean  3rd Qu  Max.\n");
  cat(" ", summary(res), " ", getmode(res), "\n");
  cor(0.2, summary(res)[2]);
  cat("th_1/Q_1  = ", 0.2/summary(res)[2], "\n");
  cat("---------------\n");
}

###########################################################


print("Parametric Analisy:");
library(rpart);
source("functions.R");

breath_names_learn = list("dataset1.csv", "dataset2.csv", "dataset3.csv",
                          "dataset4.csv", "dataset5.csv", "dataset6.csv");

for(t in 1:length(breath_names_learn)) {
  # learning dataset
  breath_test = read.csv(breath_names_learn[[t]]);
  breath_learning = NULL;
  for(i in 1:length(breath_names_learn)) {
    if (i != t) {
      breath_learning = rbind(breath_learning, read.csv(breath_names_learn[[i]]));
    }
  }
  
  # decision tree
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1+after_area_2+after_area_3, data = breath_learning,
                     method = 'class');
  
  breath_res = predict(breath_dt, breath_test[, 2:20], type='prob');
  breath_res_2 = matrix(breath_res, ncol = 2 , byrow = FALSE);
  res = c();
  for(k in 1:length(breath_res_2[,2])) {
    res = c(res, breath_res_2[k,2]);
  }
  
  # Now shifting the th_1, I'll be able to see the tree grade of change in accuracy.
  th = (1:50)/100;
  count = matrix(0, nrow=7, ncol=length(th));
  rates = matrix(0, nrow=4, ncol=length(th));
  
  for(i in 1:length(th)){
    # COUNT INDEXES
    # 1 - ok_correctly_classified_res
    # 2 - ok_count_corr
    # 3 - an_correctly_classified_res
    # 4 - an_count_corr
    # 5 - doub_count
    # 6 - tot
    # 7 - false positive (corr=0, but classified by res 1)
    
    for(j in 1:length(res)) {
      if(res[j] > 1 - th[i]) { # 1 class predict
        if(breath_test[j, 1] == 1) {
          count[1, i] = count[1, i] + 1;
          count[2, i] = count[2, i] + 1;
        } else {
          count[4, i] = count[4, i] + 1;
          count[7, i] = count[7, i] + 1;
        }
      } else if(res[j] < th[i]) { # 0 class predict
        if(breath_test[j, 1] == 1) {
          count[2, i] = count[2, i] + 1;
        } else {
          count[3, i] = count[3, i] + 1;
          count[4, i] = count[4, i] + 1;
        }
      } else { # 2 class
        count[5, i] = count[5, i] + 1; # doub only increment.
      }
      count[6, i] = count[6, i] + 1; # tot increment.
    }
    
    # print results
    rates[1,i] = count[1, i] / count[2, i];
    rates[2,i] = count[3, i] / count[4, i];
    rates[3,i] = (count[5, i] / count[6, i]) * 100;
    rates[4,i] = count[1, i] / (count[1, i]+count[7, i]);
    
    for(k in 1:nrow(rates)) {
      for(h in 1:ncol(rates)) {
        if (is.nan(rates[k,h])) {
          rates[k,h] = 0;
        }
      }
    }
    
    cat("th=", th[i], "\n");
    cat("  (", count[1,i],", ",count[2,i],", ",count[3,i],", ", count[4,i],", ", count[5,i],", ",count[6,i],")\n");
    cat("  TPR= ", rates[1,i], "\n");
    cat("  TNR= ", rates[2,i], "\n");
    cat("  DR=  ", rates[3,i], "%\n");
    cat("  PR=  ", rates[4,i], "\n");
  }
  
  x11();
  plot(th, rates[1,], "l", col="blue", xlab="Threshold Level", ylab = "Rates - TPR, TNR, DR, PR",lwd=2, ylim=c(0,1));
  title(breath_names_learn[[t]]);
  lines(th, rates[2,], "l", col="red", ,lwd=2, ylim=c(0,1));
  lines(th, (rates[3,] / 100), "l", col="magenta",, lwd=2, ylim=c(0,1));
  lines(th, rates[4,], "l", col="green",  lwd=2, ylim=c(0,1));
  legend(0.4, y=0.5, c("TPR", "TNR", "DR", "PR"), lty=c(1,1,1,1), lwd=c(2,2,2,2), col = c("blue", "red", "magenta", "green"));
}


