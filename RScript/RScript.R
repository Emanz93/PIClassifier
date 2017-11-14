library(rpart);

# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)

# path of the dataset to classify
path = myArgs[1];
#path = "/home/emanuele/DATA/Development/Python/PIClassifier/data/p_03_01_nava_08/dataset.csv";

# dataset to classify
dataset = read.csv(path);

# changing working directory
setwd(paste(getwd(), "/RScript/learning_files/", sep = ""));

# list of all learning dataset names
learning_dataset_names = list.files(pattern = "*.csv");

# breath variable contains all of the learning datasets.
breath = read.csv(learning_dataset_names[1]);
for (i in 2:length(learning_dataset_names)) {
  breath = rbind(breath, read.csv(learning_dataset_names[i]));
}

#split the dataset in 0 (anomaly) dataset and 1 (ok) dataset
ok_breath_dataset = NULL; # 0 (anomaly) dataset
an_breath_dataset = NULL; # 1 (ok) dataset
for(i in 1:nrow(breath)){
  if(breath[i,1] == 0) {
    an_breath_dataset = rbind(an_breath_dataset, breath[i,]);
  } else {
    ok_breath_dataset = rbind(ok_breath_dataset, breath[i,]);
  }
}

# generate the indexes of the two classes with a sampling over the ok class and a oversampling on the anomaly class.
# oversampling = sampling with replacement.
# I want that the classes are equal in cardinality. so I extract the number of ok class.
an_idxs = sample(1:nrow(an_breath_dataset), nrow(ok_breath_dataset), replace = TRUE);
ok_idxs = sample(1:nrow(ok_breath_dataset), nrow(ok_breath_dataset));

# creating the final BALANCED learning dataset.
learning_dataset = NULL;
for(i in 1:length(an_idxs)) {
  learning_dataset = rbind(learning_dataset, an_breath_dataset[an_idxs[i],]);
  learning_dataset = rbind(learning_dataset, ok_breath_dataset[ok_idxs[i],]);
}

# creating and construct the decision tree
breath_dt <- rpart(classification ~ picco+integral+pi_index+tidal_volume+
                     resp_rate+rr_over_tv+etco2+first_value+last_value+
                     intercetta+integral_after_max+before_concavity_counter+
                     before_area_1+before_area_2+before_area_3+
                     after_concavity_counter+after_area_1+after_area_2+after_area_3, data = learning_dataset,
                     method = 'class');
#breath_res_dt = predict(breath_dt, dataset[, 2:20], type='class');
breath_res = predict(breath_dt, dataset[, 2:20], type='prob');
breath_res_2 = matrix(breath_res, ncol = 2 , byrow = FALSE);

res = c();
for(i in 1:length(breath_res_2[,2])) {
  res = c(res, breath_res_2[i,2]);
}

# cat will write the result to the stdout stream
cat(res)
