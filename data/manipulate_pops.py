# Take as input "pops.csv" that contains population data for age/sex cohorts in the US by year. 
# Output a csv with the following columns:
# sex (0 for female, 1 for male)
# age (midpoint age for the age range)
# year (midpoint year from a 5-year window)
# sample_size (total population across those five years)
# offset (log sample_size)
# seatbeltUse_synethetic (A uniform(0,1) random variable that will be used to predict reporting rate)
# (Intercept): a column of 1's

import pandas as pd
import numpy as np

popsData = pd.read_csv("./pops.csv")

popsData['sexID'] = [1 if s=="male" else 0 for s in popsData.sex]
popsData['age'] = np.mean([popsData["age_start"], popsData["age_end"]], axis=0)

# Remove ages over 85
popsData = popsData[popsData.age <= 85]

# Round age to the closest 0.5
popsData['age'] = np.round(popsData.age * 2)/2.0


def yearMap(year):
    """Divide the years as they were in the original road injuries data"""
    if 1993 <= year and year <= 1997:
        return 1995
    elif 1998 <= year and year <= 2002:
        return 2000
    elif 2003 <= year and year <= 2007:
        return 2005
    elif 2008 <= year and year <= 2012:
        return 2010
    else:
        return None

popsData['yearGroupID'] = [yearMap(y) for y in popsData.year]

finalTable = pd.concat([popsData["age"], popsData["sexID"], popsData["yearGroupID"], popsData["population"]],
                       axis=1, 
                       keys=['age', 'sex', 'year', 'sample_size'])

grouped = finalTable.groupby(["age", "sex", "year"], as_index=False).sum()

# Add seatbelt use as a synthetically generated variable
grouped["seatbeltUse_synthetic"] = np.random.uniform(0, 1, size=len(grouped))

grouped["offset"] = np.log(grouped.sample_size)
grouped["(Intercept)"] = 1

# Write to CSV
grouped.to_csv("roadInj_data.csv", index=False)