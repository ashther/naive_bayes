library(dplyr)
library(e1071)

data <- read.table('weather.txt', sep = ',', 
                   colClasses = rep('factor', 5), 
                   col.names = letters[1:5])
# standard result
naiveBayes(data[, -length(data)], data[, length(data)]) %>% 
    predict(data) %>% 
    mapply(`==`, ., data[, length(data)]) %>% 
    mean()

# df is dataset with all categorical variables and class
naiveBayes_RC <- function(df, con) {
    n <- length(df)
    prop_table <- by(df[, -n], df[, n], 
                     function(x)sapply(x, function(y){
                         temp <- table(y)
                         if (any(temp == 0)) {
                             temp <- temp + 1
                         }
                         prop.table(temp)
                     }))
    
    ctg <- prop.table(table(df[, n]))
    prop_result <- sapply(names(ctg), function(c){
        Map(function(x, y)return(x[y]), prop_table[[c]], con) %>% 
            do.call('rbind', .) %>% 
            apply(2, prod) %>% 
            `*`(ctg[c])
    }) 
    return(names(ctg)[apply(prop_result, 1, which.max)])
}

# df is dataset with numerical variables and categorical class
naiveBayes_RD <- function(df, con) {
    n <- length(df)
    avg_table <- by(df[, -n], df[, n], function(d)lapply(d, mean))
    sd_table <- by(df[, -n], df[, n], function(d)lapply(d, sd))
    ctg <- prop.table(table(df[, n]))
    
    prop_result <- sapply(names(ctg), function(c){
        mapply(function(miu, sigma, x)
            # Gaussian distribution
            return(1 / (sigma * sqrt(2 * pi) * exp((x - miu) ^ 2 / (2 * sigma ^ 2)))), 
            avg_table[[c]], sd_table[[c]], con) %>% 
            apply(1, prod) %>% 
            `*`(ctg[c])
    })
    return(names(ctg)[apply(prop_result, 1, which.max)])
}


