## Compute the inverse of a matrix. 
## During computing the results are cached in order
## to optimize the computation process. Thus, if 
## the input matrix was not changed the previously 
## cached result (if exists) will be returned.


## Creates the cache matrix object which contains
## matrix data and results cache.
## x: is an invertible matrix

makeCacheMatrix <- function(x = matrix()) {
  cachedInverse <- NULL
  
  setMatrix <- function(matrixObj) {
    x <<- matrixObj
    cachedInverse <<- NULL
  }
  
  getMatrix <- function() x
  setInverse <- function(inverse) cachedInverse <<- inverse
  getInverse <- function() cachedInverse
  
  list(setMatrix = setMatrix, 
       getMatrix = getMatrix,
       setInverse = setInverse,
       getInverse = getInverse)
}


## Returns the inverse matrix.
## x: is a cache matrix object

cacheSolve <- function(x, ...) {
  cachedInverse <- x$getInverse()
  
  if(!is.null(cachedInverse)) {
    message("getting cached data")
    return(cachedInverse)
  }
  
  matrixObj <- x$getMatrix()
  inversedMatrix <- solve(matrixObj, ...)
  x$setInverse(inversedMatrix)
  inversedMatrix
}
