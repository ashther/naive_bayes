library(dplyr)
library(e1071)

data <- read.table('weather.txt', sep = ',', 
                   colClasses = rep('factor', 5), 
                   col.names = letters[1:5])

naiveBayes(data[, -length(data)], data[, length(data)]) %>% 
    predict(data) %>% 
    mapply(`==`, ., data[, length(data)]) %>% 
    mean()

naiveBayesR <- function(df, con) {
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


