# AGGREGATE POPULATION DATA
# PULLED ON SEPT. 11, 2021
#
# SOURCE: 5-YEAR AND CUSTOM AGE GROUPS
# http://ghdx.healthdata.org/record/ihme-data/gbd-2019-population-estimates-1950-2019

library(data.table)
library(magrittr)

# READ DATA -----------------------------

files <- list.files("pops/", pattern=".CSV", full.names=T)
df <- lapply(files, fread) %>% rbindlist

# Get just U.S.A.
df <- df[location_id == 102]

# MODIFICATION --------------------------

data <- copy(df)

# SEX
data <- data[sex_name %in% c("male", "female")]
setnames(data, "sex_name", "sex")

# AGE

# Define age start and age end
ages <- c(2:20, 30:32, 235)
age_start <- c(rep(0.00, 3), 1, seq(5, 80, by=5), rep(085, 3))
age_end   <- c(rep(0.99, 3), 4, seq(9, 84, by=5), rep(124, 3))

age_df <- data.table(age_group_id=ages,
                     age_start=age_start,
                     age_end=age_end)

data <- merge(data, age_df, by="age_group_id")

# AGGREGATE OVER AGES AND YEARS
data <- data[, lapply(.SD, sum), .SDcols=c("val"),
             by=c("age_start", "age_end", "sex",
                  "location_name", "location_id", "year_id")]

# FINISH
data <- data[year_id >= 1990]
setnames(data, "year_id", "year")
setnames(data, "val", "population")

write.csv(data, "pops.csv")
