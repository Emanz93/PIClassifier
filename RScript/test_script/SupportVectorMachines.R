# CLASSIFICATION METHOD 2: SUPPORT VECTOR MACHINES
data("iris")
install.packages('e1071',dependencies=TRUE)
library(e1071)

iris_test_indexes = sample(1:nrow(iris), 50)
iris_train_indexes = setdiff(1:nrow(iris), iris_test_indexes)

iris_svm <- svm(iris[iris_train_indexes,1:4],iris[iris_train_indexes,5])

# alternative way of using "svm" function
# i.e. 1st argument is a formula of the form "OutputAttribute ~ InputAttribute1 + InputAttribute2 + ...
# 2nd argument is a training set, containing both input and labels
iris_svm <- svm(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, iris[iris_train,])
#or previous notation iris_scm = svm(iris[iris_train,1:4],iris[iris_train,5])

# look at the internal structure of the SVM model

iris_svm$...

res = predict(iris_svm,iris[iris_test_indexes,1:4])
cm_iris = table(res,iris[iris_test_indexes,5])

# again, try with different train/test and compute accuracy
correct  = sum(diag(cm_iris))
accuracy = correct / sum(cm_iris)


##########################################
breath_learning = read.csv("dataset1.csv")

breath_test = read.csv("dataset2.csv")

breath_svm <- svm(classification ~ picco+integral+pi_index+tidal_volume+
                    resp_rate+rr_over_tv+etco2+first_value+last_value+
                    intercetta+integral_after_max+before_concavity_counter+
                    before_area_1+before_area_2+before_area_3+
                    after_concavity_counter+after_area_1+
                    after_area_2+after_area_3,data = breath_learning)
breath_res = predict(breath_svm, breath_test[,2:18])
cm_breath = table(breath_res, breath_test[,1])

###########################################
# Breath Script
breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");
breath = read.csv(breath_names[[1]]);
for (i in 2:length(breath_names)) {
  breath = rbind(breath, read.csv(breath_names[[i]]));
}

library(caret);
library(e1071);
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
  #breath_svm <- svm(classification ~ picco+integral+pi_index+tidal_volume+
  #                     resp_rate+rr_over_tv+etco2+first_value+last_value+
  #                     intercetta+integral_after_max+before_concavity_counter+
  #                     before_area_1+before_area_2+before_area_3+
  #                     after_concavity_counter+after_area_1+
  #                     after_area_2, data = breath[train_indexes,]);
  breath_svm <- svm(breath[train_indexes, 2:19], y = breath[train_indexes, 1])
  breath_res = predict(breath_svm, breath[test_indexes, 2:19]);
  cm_breath = table(pred=round(breath_res), true=breath[test_indexes,1]);
  cat('iteration ');
  print(i);
  print(cm_breath);
  print('-------------');
}
  
