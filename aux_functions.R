# Kernel Smooth function
# Translated from python
# http://www.adeveloperdiary.com/data-science/computer-vision/applying-gaussian-smoothing-to-an-image-using-python-from-scratch/
# https://stackoverflow.com/questions/22747916/how-to-generate-a-discrete-2d-gaussian-smoothing-kernel-using-r
# INPUTS: 
# x (m x n) matrix, 
# kern (i x i) the smoothing kernel matrix, 
# norm (bool) normalizes the kernel by the mean of its values
kernelsmooth = function(x, kern, norm=TRUE) {
  # how many rows/cols of zeroes are used to pad.
  width = dim(kern)[1]
  pad = floor(width / 2)
  
  # record the width and height the input data matrix
  x_w = ncol(x)
  x_h = nrow(x)
  
  # Are we normalizing the kernel?
  if (norm == TRUE) {
    k = kern / sum(abs(kern))
  } else {
    k = kern
  }
  
  # pad all around the matrix an equal width of zeros
  x_pad = t(ptw::padzeros(data=x, nzeros=pad, side="both"))
  x_pad = t(ptw::padzeros(data=x_pad, nzeros=pad, side="both"))
  
  # Pre-allocate the final (smoothed) data matrix
  s = matrix(0, nrow = x_h, ncol = x_w)
  
  # Pre-allocate a temporary matrix for the iterative calculations
  temp = matrix(0, width, width)
  
  # Loop through the data to apply the kernel.
  for (col in 1:x_w ) {
    for (row in 1:x_h ) {
      temp = x_pad[row:(row + width - 1), col:(col + width - 1)]
      s[row,col] =  sum(k * temp, na.rm = T)
    }
  }
  
  # return the smoothed data
  return(s)
}

# Normalizing function
min_max_norm = function(x) {
  (x - min(x)) / (max(x) - min(x))
}
