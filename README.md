# DSCI551
FinalProject


**aggregate_by_neighborhood.ipynb**
Script that reads the databases in MySQL and uses PySpark to process and merge them into a single tabular dataset, that is then converted to JSON format and uploaded to Firebase.

**average_scores.ipynb**
Script that calculates the average score for each of the features stored in the Firebase dataset.

**Crime_Data_from_2010_to_2019.csv**
The original crime dataset obtain from the Los Angeles open data portal.

**Crime_Data_2019_Neighborhoods_v1.csv  - Crime_Data_2019_Neighborhoods_v5.csv**
Intermediary results from processing the crime data, with the last CSV being the one uploaded to MySQL.

**crime_statistics.ipynb**
Feature engineering on the crime data.

**Min_Max_Neighborhoods.ipynb**
Querying the best and worst performing neighborhoods in each of the features existent in the Firebase database.

**MySQL_Connection_Test.ipynb / Tester.py**
Testing connection from PySpark to MySQL.

**predict_missing_neighborhoods.ipynb**
Usage of KNN algorithm to predict neighborhoods that could not be obtained from the google maps API due to usage limitations.

**retrieve_neighborhood.ipynb**
Script using google maps API to obtain the neighborhood associated with each crime register.

**Search.ipynb / Search.py**
Functions to query Firebase from a set of neighborhoods and/or features.


