## DATA CLEANING


## What Is Recency, Frequency, Monetary Value (RFM)?
Recency, frequency, monetary value (RFM) is a model used in marketing analysis that segments a company's consumer base by their purchasing patterns or habits. In particular, it evaluates customers' recency (how long ago they made a purchase), frequency (how often they make purchases), and monetary value (how much money they spend).

RFM is then used to identify a company's or an organization's best customers by measuring and analyzing spending habits in order to improve low-scoring customers and maintain high-scoring ones.

## Recency
First, let’s calculate the value of recency - the latest date and time a purchase was made on the platform. This can be achieved in two steps:

i) Assign a recency score to each customer
We will subtract every date in the dataframe from the earliest date. This will tell us how recently a customer was seen in the dataframe. A value of 0 indicates the lowest recency, as it will be assigned to the person who was seen making a purchase on the earliest date.

ii) Select the most recent purchase
One customer can make multiple purchases at different times. We need to select only the last time they were seen buying a product, as this is indicative of when the most recent purchase was made: 

## LINK TO READ ABOUT PySpark JOINS
https://sparkbyexamples.com/pyspark/pyspark-join-explained-with-examples/

## Frequency
Let’s now calculate the value of frequency - how often a customer bought something on the platform. To do this, we just need to group by each customer ID and count the number of items they purchased:

## Monetary value
1. Find the total amount spent in each purchase:
Each customerID comes with variables called “Quantity” and “UnitPrice” for a single purchase

2. Find the total amount spent by each customer:
To find the total amount spent by each customer overall, we just need to group by the CustomerID column and sum the total amount spent:

## Standardization
Before building the customer segmentation model, let’s standardize the dataframe to ensure that all the variables are around the same scale:

## Building the Machine Learning Model
Now that we have completed all the data analysis and preparation, let’s build the K-Means clustering model. 

The algorithm will be created using PySpark’s machine learning API.

i) Finding the number of clusters to use
When building a K-Means clustering model, we first need to determine the number of clusters or groups we want the algorithm to return. 

The most popular technique used to decide on how many clusters to use in K-Means is called the “elbow-method.”

This is done simply running the K-Means algorithm for a wide range of clusters and visualizing the model results for each cluster. The plot will have an inflection point that looks like an elbow, and we just pick the number of clusters at this point.

## Interptetation
Here is an overview of characteristics displayed by customers in each cluster:

1. Cluster 0: Customers in this segment display low recency, frequency, and monetary value. They rarely shop on the platform and are low potential customers who are likely to stop doing business with the ecommerce company. 
2. Cluster 1: Users in this cluster display high recency but haven’t been seen spending much on the platform. They also don’t visit the site often. This indicates that they might be newer customers who have just started doing business with the company.
3. Cluster 2: Customers in this segment display medium recency and frequency and spend a lot of money on the platform. This indicates that they tend to buy high-value items or make bulk purchases.
4. Cluster 3: The final segment comprises users who display high recency and make frequent purchases on the platform. However, they don’t spend much on the platform, which might mean that they tend to select cheaper items in each purchase.

