import json
import pandas as pd
import operator
import re
import numpy as np

# Global Constants
Q1_json_file = 'Question1.json'
csv_name = 'Reviews.csv'

# a)

# This function reads in the Question1.json file and exports the 'Reviews' 
# object as a .csv file named 'Reviews.csv' with the desired format 

def read_json(json_file, csv_out):
    # Read in Question1.json
    with open(json_file, 'r') as f:
        JSON_dict = json.load(f)
    
    # Select the 'Reviews' object as a data frame
    Reviews_Df = pd.DataFrame(JSON_dict['Reviews'])
    
    Reviews_Df = Reviews_Df.set_index('Author')
    
    # Format the columns as desired in the question
    Column_format = ['Author_Location','ReviewID','Date','Overall','Content']
    Reviews_Df = Reviews_Df.reindex(columns = Column_format)
     
    Reviews_Df.to_csv(csv_out)
    return

read_json(Q1_json_file, csv_name)

# b)
    
# This function reads in the 'Reviews.csv' from part a and adds a class label 
# who's value is 1 when the overall rating is greater than 3 and 0 otherwise
    
def class_label(csv_in):
    Reviews_Df = pd.read_csv(csv_in)

    # Add a class column and 0 fill
    Reviews_Df['Class'] = 0
    
    # Replace all 0 values with 1 where the overall rating > 3
    Reviews_Df.loc[Reviews_Df.Overall > 3, 'Class'] = 1
    
    Reviews_Df.to_csv(csv_in)
    return 

class_label(csv_name)
    
# c)
    
# This function consumes a data frame of reviews and returns two dictionaries, 
# positive and negative, which contain the words used in positive and negative 
# reviews respectively
    
def split_review(Reviews_df):
    #Initialize empty dictionaries to fill with words as keys and their counts as values
    positive = {}
    negative = {}
    
    # Loop over each row in the data frame to get the words contained in the reviews
    for index, row in Reviews_df.iterrows():
        # Spilt the review on the following characters: ., ", ', ,, (, ), !, ?, :, *, and whitespace
        list_of_words = re.split(r'[.' + "'" + ',"()!?:*\s]',row['Content'])
        
        # Check if review is positive or negative then alias the appropriate dictionary
        if (row['Class'] == 1):
            dictionary = positive
        else:
            dictionary = negative
            
        # Set the count of each word in the review to 1, or increase it by 1 if it already exists
        for word in list_of_words:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1
            
    return positive, negative
    
# This function finds and outputs (prints) the top ten words associated with 
# positive and negative reviews. 

def find_top_ten(csv_in):
    Reviews_df = pd.read_csv(csv_in)
    
    positive, negative = split_review(Reviews_df)

    positive_words = []
    negative_words = []
    
    # Keep track of the words already looped through
    used_words = []
    
    # Loop until both lists have 10 words
    while ((len(positive_words) < 10) or (len(negative_words) < 10)):
        
        # Get the word with the maximum word count in each dictionary
        max_positive = ''
        max_negative = ''
        
        # Loop until we find a string this is completely alphabetic
        while (not (max_positive.isalpha())):
            max_positive = max(positive.items(), key=operator.itemgetter(1))[0]
            positive.pop(max_positive)
            
        while (not (max_negative.isalpha())):
            max_negative = max(negative.items(), key=operator.itemgetter(1))[0]
            negative.pop(max_negative)
        
        # Avoid appending the same word
        if (max_positive == max_negative):
            continue

        # Check if positive word is not in negative dictionary and not already used
        if (max_positive not in negative and max_positive not in used_words \
            and len(positive_words) < 10):
            positive_words.append(max_positive)
            
        # Check if negative word is not in positive dictionary and not already used 
        if (max_negative not in positive and max_negative not in used_words \
            and len(negative_words) < 10):
            negative_words.append(max_negative)
            
        used_words.append(max_negative)
        used_words.append(max_positive)

    print(positive_words,'\n',negative_words)
    return

find_top_ten(csv_name)

# d)

Ex_Review = """Maybe the high expectations but really the food was ok.Best dishes 
            were liver with jelly and eggplant casserole.Other than that it was 
            bbq with a little twist.Just for the food I would have given 3 stars 
            but the service was a genuine 1.5 stars so thus the 2 stars.They were 
            very pushy to get us out within an hour or so.Staff were snooty and 
            felt I was at a restaurant in manhattan."""
            
# This function consumes a Review, two dictionaries for positive and negative 
# words, the counts of the values of those dictionaries, the probability a review 
# is positive or negative and the log of the quotient of that probability. This 
# function returns 1 if the review should be positive and 0 otherwise.
    
def eval_review_help(Review, positive, negative, pos_sum, neg_sum, prob_1, prob_0, log_prob):
    Review = re.split(r'[.' + "'" + ',"()!?:*\s]',Review)
    
    prob_sum = 0
    
    # Compute the second term in the calculation of f(X)
    for word in Review:
        # Find the amount of times word appears in positive and negative 
        if word in positive:
            pos_count = positive[word]
        else: 
            pos_count = 0
        if word in negative:
            neg_count = negative[word]
        else:
            neg_count = 0
        
        # Calcualte the conditional probabilities for positive and negative
        prob_w_given_1 = (pos_count/pos_sum) / prob_1
        prob_w_given_0 = (neg_count/neg_sum) / prob_0
        
        # Avoid log evaluated at 0 errors
        if prob_w_given_1 == 0 and prob_w_given_0 == 0:
            continue
    
        elif prob_w_given_1 == 0:
            prob_sum -= np.log(prob_w_given_0)
            continue
    
        elif prob_w_given_0 == 0:
            prob_sum += np.log(prob_w_given_1)
            continue
        
        prob_sum += (np.log(prob_w_given_1) - np.log(prob_w_given_0))
    
    retval = log_prob + prob_sum
    if retval >= 0:
        return 1
    return 0

# This function consumes a Review and returns 1 if the Review should be considered 
# positive and 0 otherwise.

def evaluate_review(csv_in, Review):
    Reviews_df = pd.read_csv(csv_in)
    
    positive, negative = split_review(Reviews_df)
                
    num_of_reviews = len(Reviews_df.index)
    
    # Calculate the probability of getting a positive and negative review
    prob_y_equals_1 = len(Reviews_df[Reviews_df['Class'] == 1]) / num_of_reviews
    prob_y_equals_0 = len(Reviews_df[Reviews_df['Class'] == 0]) / num_of_reviews
    
    # Compute the first term in the calculation of f(X)
    log_of_prob = np.log(prob_y_equals_1 / prob_y_equals_0)
    
    num_of_pos_words = sum(positive.values())
    num_of_neg_words = sum(negative.values())
    
    
    retval = eval_review_help(Review, positive, negative, num_of_pos_words, num_of_neg_words, \
                     prob_y_equals_1, prob_y_equals_0, log_of_prob)

    return retval

print(evaluate_review(csv_name, Ex_Review))

# e)

# This function returns true if Reviews with an overall rating of 3 should be 
# positive and false otherwise.

def should_3_be_positive(csv_in):
    Reviews_df = pd.read_csv(csv_in)
    
    positive, negative = split_review(Reviews_df)
                
    num_of_reviews = len(Reviews_df.index)
    
    # Calculate the probability of getting a positive and negative review
    prob_y_equals_1 = len(Reviews_df[Reviews_df['Class'] == 1]) / num_of_reviews
    prob_y_equals_0 = len(Reviews_df[Reviews_df['Class'] == 0]) / num_of_reviews
    
    # Compute the first term in the calculation of f(X)
    log_of_prob = np.log(prob_y_equals_1 /prob_y_equals_0)
    
    num_of_pos_words = sum(positive.values())
    num_of_neg_words = sum(negative.values())
    
    count = 0
    result = 0
    
    # Loop over each row in the data frame to get the words contained in the reviews
    for index, row in Reviews_df.iterrows():
        # Check only reviews with rating 3
        if (not (row['Overall'] == 3)):
            continue
        else: 
            count += 1
            # Determine if the Review should be positive or negative
            result += eval_review_help(row['Content'], positive, negative, num_of_pos_words, \
                                       num_of_neg_words, prob_y_equals_1, prob_y_equals_0, log_of_prob)
    
    # Check if at least half of the reviews were considered positive
    if (2*result >= count):
        return True
    return False

print(should_3_be_positive(csv_name))
            
    
