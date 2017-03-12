function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

sigmaVals = [0.01; 0.03; 0.1; 0.3; 1; 3; 10; 30];
cVals = [0.01; 0.03; 0.1; 0.3; 1; 3; 10; 30];

%xError = zeros(length(sigmaVals), length(cVals));
xValError = zeros(length(sigmaVals), length(cVals));

minDiff = 100;
minSigma = 0;
minC = 0;

for i = 1:length(sigmaVals)
	for j = 1:length(cVals)
	
		model = svmTrain(X, y, cVals(j), @(x1, x2) gaussianKernel(x1, x2, sigmaVals(i)));
%		pX = svmPredict(model, X); 
		pXVal = svmPredict(model, Xval); 
		
%		xError(i,j) = mean(double(pX ~= y));
		xValError(i,j) = mean(double(pXVal ~= yval));
		
%		diff = (xError(i,j) - xValError(i,j)) .^ 2;
		
		if (xValError(i,j) < minDiff)
			minDiff = xValError(i,j);
			minSigma = sigmaVals(i);
			minC = cVals(j);
		end
			
	end
end

sigma = minSigma;
C = minC;
% =========================================================================

end
