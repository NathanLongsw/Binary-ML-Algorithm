# Binary-ML-Algorithm

This Python project will read data in JSON format and create a binary ML system.

## About the Data

The RawData.json file contains samples of Yelp restaurant review in JSON format. The JSON file contains JSON objects ‘RestaurantInfo’ and ‘Reviews’. In the ‘RestaurantInfo’ object, it contains the basic information of the restaurant (Address, ImgURL, Name etc.). In the ‘Reviews’ object, there are 1445 different reviews on this restaurant. The JSON object ‘Reviews’ is defined as the following:  
    • Author: name of the reviewer  
    • Author_Location: location of the reviewer  
    • Content: review  
    • Date: date when the review was registered  
    • Overall: rating of the restaurant in numerical format  
    • ReviewID: system ID for the review  
  
## Implementation Details

The implementation of this project is split up into 5 section. Each section below will outline the purpose of each section.

### Section A

The JSON file used in this program is named ‘RawData.json’. This section parses all the reviews in the file, and reconstructs all the information in a table with the following headers in order: Author, Author Location, ReviewID, Data, Overall, Content.

### Section B

This section adds an additional column to the table created in section A named 'class label'. Reviews with overall rating above 3 are labelled as positive (class label =1), while the rest are labelled as negative (class label=0).

### Section C

The functions in this section are used to list the top 10 words that are associated with positive and negative reviews. 

The split_review function consumes a data frame of reviews and returns two dictionaries, positive and negative, which contain the words used in positive and negative reviews respectively. This function is used as a helper for the function discussed below.

The second function, find_top_ten, finds and outputs (prints) the top ten words associated with positive and negative reviews. 

### Section D

For this section we must first establish some definitions. 

Let w represent a word in the review documents and y represent the class label created in section B. This function consumes the data in RawData.json as a training set and a review as a string. It predicts if a given review should be considered as positive or negative based off of the training set. The calculation is described in detail below.

$P ( w \mid y = 1)$ represents the conditional probability that given the positive label, word w occurs in the reviews.  
$P ( w \mid y = 0)$ represents the conditional probability that given the negative label, word w occurs in the reviews.  

Considering all 1445 reviews as a single training set, we us the following classifier to predict the class label for the review:
    • f (X) = $\log(P(y=1)/P(y=0))$ + $\sum_{w}$ ( $\log(P(w \mid y=1))$ – $\log(P(w \mid y=0))$ )
    • Predicted class label y = 1 if f(X) ≥ 0, otherwise y = 0. 	\equiv
  
The new review being considered in the program is as follows:

Review:
“Maybe the high expectations but really the food was ok.Best dishes were liver with jelly and eggplant casserole.Other than that it was bbq with a little twist.Just for the food I would have given 3 stars but the service was a genuine 1.5 stars so thus the 2 stars.They were very pushy to get us out within an hour or so.Staff were snooty and felt I was at a restaurant in manhattan.”

### Section E

This final section determines if reviews with an overall rating equal to 3 should be considered as positive reviews or negative reviews. This is done by checking if the review with rating equal to 3 are usually percieved as positive or negative by the function in section D.

