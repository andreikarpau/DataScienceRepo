library(RWeka)

adaptor <- read.csv("../Data/competition_data/comp_adaptor.csv")
adaptor[25, ]$overall_length <- adaptor[25, ]$length_1 + adaptor[25, ]$length_2
adaptorPredData <- adaptor[, c(4, 5, 6, 11, 12, 20)]
predAdaptor <- adaptorPredData[c(9, 22), ]
adaptorPredData <- adaptorPredData[-c(9, 22), ]

lr <- LinearRegression(weight ~ ., data = adaptorPredData)
weights <- predict(lr, newdata = predAdaptor)
adaptorInfo <- adaptor[c(1, 4, 20)]
adaptorInfo[9, ]$weight <- weights[1]
adaptorInfo[22, ]$weight <- weights[2]

rm(list = c("adaptor", "adaptorPredData", "predAdaptor", "lr", "weights"))

boss <- read.csv("../Data/competition_data/comp_boss.csv")
boss$weight[103] <- 0.133889867
boss$weight[133] <- 0.005
bossInfo <- boss[c(1, 7, 15)]

rm(list = c("boss"))

elbow <- read.csv("../Data/competition_data/comp_elbow.csv")
elbowInfo <- elbow[c(3, 4, 5, 6, 7, 8, 9, 16)]

elbow$weight[100] <- 0.7389120
elbow$weight[101] <- 0.5830082

elbow$overall_length[97] <- 65.57548
elbow$overall_length[145] <- 104.32181
elbow$overall_length[160] <- 76.18948

elbowInfo <- elbow[c(1, 6, 16)]

rm(list = c("elbow"))


float <- read.csv("../Data/competition_data/comp_float.csv")
floatInfo <- float[c(1, 3, 4, 5, 7)]

rm(list = c("float"))

hfl <- read.csv("../Data/competition_data/comp_hfl.csv")
hflInfo <- hfl[c(1, 3, 9)]

rm(list = c("hfl"))

nut <- read.csv("../Data/competition_data/comp_nut.csv")
nut$weight[49] <- 0.07863636
nutInfo <- nut[c(1, 5, 7, 11)]

rm(list = c("nut"))