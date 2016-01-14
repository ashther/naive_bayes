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
    prop_table <- by(df, df[, n], 
                     function(x)sapply(x, function(y)prop.table(table(y))))
    
    ctg <- prop.table(table(df[, n]))
    prop_result <- sapply(names(ctg), function(c){
        Map(function(x, y)return(x[y]), prop_table[[c]][-n], con) %>% 
            do.call('rbind', .) %>% 
            apply(2, prod) %>% 
            `*`(ctg[c])
    }) 
    return(names(ctg)[apply(prop_result, 1, which.max)])
}


