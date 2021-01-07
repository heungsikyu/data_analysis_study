install.packages("UsingR")
library(UsingR)


data(cfb)
head(cfb)
print(cfb)


summary(cfb$INCOME)
hist(cfb$INCOME, breaks = 500, freq = TRUE)

## 로그 변환 
cfb <- transform(cfb, INCOME_log = log(INCOME + 1))
hist(cfb$INCOME_log, breaks = 500, freq = TRUE)


##제곱근 변환
cfb <- transform(cfb, INCOME_sqrt = sqrt(INCOME + 1))
hist(cfb$INCOME_sqrt, breaks = 500, freq=TRUE)


##Q-Q plot
par(mfrow = c(1, 3))
qqnorm(cfb$INCOME, main="Q-Q plot of INCOME")
qqline(cfb$INCOME)

qqnorm(cfb$INCOME_log, main="Q-Q plot of INCOME_log")
qqline(cfb$INCOME_log)

qqnorm(cfb$INCOME_sqrt, main="Q-Q plot Of INCOME_sqrt")
qqline(cfb$INCOME_sqrt)

par(mfrow = c(1,1))
