get_confusion_matrix <- function(orig, pred) {
  matr = matrix(0, nrow = 2, ncol = 2);
  
  for(i in 1:nrow(orig)) {
    if(orig[i,1] == 0) {
      if(pred[[i]] == 0) {
        matr[1,1] = matr[1,1] + 1;
      } else {
        matr[1,2] = matr[1,2] + 1;
      }
    } else {
      if(pred[[i]] == 0) {
        matr[2,1] = matr[2,1] + 1;
      } else {
        matr[2,2] = matr[2,2] + 1;
      }
    }
  }

  colnames(matr) = c("0", "1");
  rownames(matr) = c("0", "1");
  return(matr);
}

# Create the function.
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

