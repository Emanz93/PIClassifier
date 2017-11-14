data("iris")
head(iris)
str(iris)
names(iris)
summary(iris)

iris_test = sample(1:nrow(iris),50)
iris_train = setdiff(1:nrow(iris),iris_test)

# using rpart package http://cran.r-project.org/web/packages/rpart/rpart.pdf
install.packages("rpart",dependencies =TRUE)
library(rpart)

#The splitting index can be gini or information, defaults to gini index

iris_dt <- rpart(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, data = iris[iris_train,], method = 'class')

# to use information gain
# iris_dt <- rpart(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, data = iris, method = 'class', parms = list(split = "information") )

# explore model

printcp(iris_dt)	# Prints a table of optimal prunings based on a complexity parameter
summary(iris_dt)	# summary of the decision tree with splitting decisions
plotcp(iris_dt)
x11();
plot(iris_dt)	# p graphical lot decision tree
text(iris_dt, use.n=TRUE) # add label to decision tree

# use model

# predict method parameter type defines the output type. With value 'class' the output is a vector of classes, with value 'raw' the output for each test item we have a score of membership for each class
# example with type = 'raw'
#predict(iris_dt,iris[iris_test,att_col],type = 'raw')
#    setosa versicolor  virginica
#23       1 0.00000000 0.00000000
#6        1 0.00000000 0.00000000
#56       0 0.90740741 0.09259259
# example with type = 'class'
#predict(iris_dt,iris[iris_test,att_col],type = 'class')
# [1] setosa setosa versicolor ...

res = predict(iris_dt,iris[iris_test,1:4],type='class')
cm_iris = table(res,iris[iris_test,5])
correct  = sum(diag(cm_iris))
accuracy = correct / sum(cm_iris)


#############################################################
# HouseVotes dataset
# https://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Records
install.packages("mlbench")
library(mlbench)
data(HouseVotes84)
str(HouseVotes84)
# warning: missing values!

house_test_indexes = sample(1:nrow(HouseVotes84), 75)
house_train_indexes = setdiff(1:nrow(HouseVotes84), house_test_indexes)

house_dt <- rpart(Class ~ V1+V2+V3+V4+V5+V6+V7+V8+V9+V10+V11+V12+V13+V14+V15+V16, data = HouseVotes84[house_train_indexes,], method = 'class')

printcp(house_dt)	# Prints a table of optimal prunings based on a complexity parameter
summary(house_dt)	# summary of the decision tree with splitting decisions
plotcp(house_dt)
x11();
plot(house_dt)	# p graphical lot decision tree
text(house_dt, use.n=TRUE) # add label to decision tree

res_house = predict(house_dt,HouseVotes84[house_test_indexes,1:4],type='class')
cm_house = table(res_house,HouseVotes84[house_test_indexes,5])
correct  = sum(diag(cm_house))
accuracy = correct / sum(cm_house)

########################################################
# Breast Cancer
data("BreastCancer")
BreastCancer = BreastCancer[, 2:11]
breast_test_indexes = sample(1:nrow(BreastCancer), 100)
breast_train_indexes = setdiff(1:nrow(BreastCancer), breast_test_indexes)
breast_dt <- rpart(Class ~ Cl.thickness+Cell.size+Cell.shape+Marg.adhesion+Epith.c.size+Bare.nuclei+Bl.cromatin+Normal.nucleoli+Mitoses, data=BreastCancer[breast_train_indexes,], method = 'class')
res_breast = predict(breast_dt, BreastCancer[breast_test_indexes, 1:9], type='class')
cm_breast = table(res_breast, BreastCancer[breast_test_indexes,10])
correct=sum(diag(cm_breast))
accuracy = correct / sum(cm_breast)

#######################################################
breath_learning_1 = read.csv("dataset1.csv")
breath_learning_2 = read.csv("dataset2.csv")
breath_learning_3 = read.csv("dataset3.csv")
breath_learning_4 = read.csv("dataset4.csv")
breath_learning_5 = read.csv("dataset5.csv")
breath_learning_6 = read.csv("dataset6.csv")

breath_learning = rbind(breath_learning_1, breath_learning_2)

breath_test = read.csv("dataset3.csv")

breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                     resp_rate+rr_over_tv+etco2+first_value+last_value+
                     intercetta+integral_after_max+before_concavity_counter+
                     before_area_1+before_area_2+before_area_3+
                     after_concavity_counter+after_area_1+
                     after_area_2+after_area_3,data = breath_learning, method = 'class')
breath_res = predict(breath_dt, breath_test[, 2:20], type='class')
cm_breath = table(breath_res, breath_test[,1])

########
# K-FOLD BREATH on the singles datasets.
b_list = list(breath_learning_1, breath_learning_2, breath_learning_3, 
              breath_learning_4, breath_learning_5, breath_learning_6)
breath_names = list("dataset1.csv","dataset2.csv","dataset3.csv","dataset4.csv","dataset5.csv","dataset6.csv")

for (i in 1:3) {
  breath_test = read.csv(breath_names[[i]]);
  breath_learning = NULL;
  for(j in 1:3) {
    if (j != i) {
      if (is.null(breath_learning)) {
        breath_learning = read.csv(breath_names[[j]]);
      } else {
        breath_learning = rbind(breath_learning, breath_names[[j]])
      }
    }
  }
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1+
                       after_area_2+after_area_3,data = breath_learning, method = 'class');
  breath_res = predict(breath_dt, breath_test[, 2:20], type='class');
  cm_breath = table(breath_res, breath_test[,1]);
  cat("interation ", i);
  print(cm_breath);
  cat("Accuracy= ", (cm_breath[1,1]+cm_breath[2,2]) / nrow(breath_test));
  print();
  cat("Error Rate= ", (1 - (cm_breath[1,1]+cm_breath[2,2]) / nrow(breath_test)));
  print();
  print("==============");
  
}

###############
# Breath Script
breath_names = list("dataset1.csv", "dataset2.csv", "dataset3.csv","dataset4.csv", "dataset4.csv", "dataset5.csv", "dataset6.csv");
breath = read.csv(breath_names[[1]]);

for (i in 2:length(breath_names)) {
  breath = rbind(breath, read.csv(breath_names[[i]]));
}

library(caret);
library(rpart);
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
  breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                       resp_rate+rr_over_tv+etco2+first_value+last_value+
                       intercetta+integral_after_max+before_concavity_counter+
                       before_area_1+before_area_2+before_area_3+
                       after_concavity_counter+after_area_1+
                       after_area_2+after_area_3, data = breath[train_indexes,], method = 'class');
  breath_res = predict(breath_dt, breath[test_indexes, 2:20], type='class');
  cm_breath = table(pred=breath_res, true=breath[test_indexes,1]);
  cat('iteration ');
  print(i);
  print(cm_breath);
  print('-------------');
}

