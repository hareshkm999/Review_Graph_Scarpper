from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import re
import nltk
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
from wordcloud import WordCloud
import pymongo
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)  # initialising the flask app with the name 'app'


## function to read and plot graphs using reviews in mongodb and save plots version2 ##





def opinion_graph(PRODUCT, PRODUCT_NAME):
    DB_NAME = "flipKart_Scrapping_DB"  # Specifiy a Database Name
    # Connection URL
    CONNECTION_URL = f"mongodb+srv://harish:haresh2019@cluster0.4ouqh.mongodb.net/DB_NAME?retryWrites=true&w=majority"
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
    # Establish a connection with mongoDB
    client = pymongo.MongoClient(CONNECTION_URL)

    # Create client with  DB
    dataBase = client[DB_NAME]

    # creating connection to the collection
    collection = dataBase[PRODUCT]
    reviews = collection.find({'Product_name': PRODUCT_NAME}, {'CommentHead': 1,
                                                               "_id": 0})  # searching the collection with the name same as the keyword
    result = []
    if reviews.count() > 0:  # if there is a collection with searched keyword and it has records in it
        # Lets Verify all the record at once present in the record with all the fields
        #print(reviews.count())
        all_record = collection.find({}, {'CommentHead': 1, "_id": 0})

    for record in enumerate(all_record):
        result.append(record[1])

    commentheads = [a['CommentHead'] for a in result]  # to filter a key value in list of dictionaries from mongodb

    with open("reviews.txt", "w", encoding='utf8') as output:  # creating text file of commentheads
        output.write(str(commentheads))

    # Joining all the reviews into single paragraph
    review_string = " ".join(commentheads)

    # Removing unwanted symbols incase if exists
    review_string = re.sub("[^A-Za-z" "]+", " ", review_string).lower()
    review_string = re.sub("[0-9" "]+", " ", review_string)
    # print(review_string)

    # here we are splitting the words as individual string
    reviews_words = review_string.split(" ")
    # print(reviews_words)

    with open("stopwords_en.txt", "r") as sw:
        stopwords = sw.read()

    reviews_words = [w for w in reviews_words if not w in stopwords]
    rev_string = " ".join(reviews_words)

    # creating word cloud for all words
    wordcloud_reviews = WordCloud(background_color='black', width=1800, height=1400).generate(rev_string)
    # plt.subplot(1, 2, 1)
    plt.imshow(wordcloud_reviews)
    plt.title("Overall Opinion")
    plt.axis('off')
    plt.savefig('static/overall_opinion.jpeg')
    #plt.show()

    # Positive opnions #
    with open("positive-lexicon.txt", "r") as pos:
        poswords = pos.read().split("\n")
        poswords = poswords[36:]

    reviews_pos_in_pos = " ".join([w for w in reviews_words if w in poswords])
    wordcloud_pos_in_pos = WordCloud(background_color='black', width=1800, height=1400).generate(reviews_pos_in_pos)
    # plt.subplot(1, 2, 2)
    plt.imshow(wordcloud_pos_in_pos)
    plt.title("Positive Reviews")
    plt.axis('off')
    plt.savefig('static/positive_opinion.jpeg')
    #plt.show()

    # fig.savefig('my_plot.png')

    # Nagative opnions #
    with open("negative-words.txt", "r", encoding="ISO-8859-1") as neg:
        negwords = neg.read().split("\n")
        negwords = negwords[37:]
        # negative word cloud
        # Choosing the only words which are present in negwords
        # negative word cloud
        # Choosing the only words which are present in negwords
    reviews_neg_in_neg = " ".join([w for w in reviews_words if w in negwords])
    # print(redmi_neg_in_neg)
    wordcloud_neg_in_neg = WordCloud(background_color='black', width=1800, height=1400).generate(reviews_neg_in_neg)
    # plt.subplot(1, 2, 2)
    plt.imshow(wordcloud_neg_in_neg)
    plt.title("Nagative Reviews")
    plt.axis('off')
    plt.savefig('static/negative_opinion.jpeg')
    #plt.show()

    review = collection.find({'Product': PRODUCT})
    data1 = pd.DataFrame(list(review))
    df = data1[['Product_name', 'Price']].drop_duplicates()
    plt.plot(df['Product_name'], df['Price'])
    plt.xlabel('Product Name')
    plt.ylabel('Price')
    plt.xticks(rotation=90)
    plt.savefig('static/prices.jpeg')

    return PRODUCT_NAME


def graph(PRODUCT, PRODUCT_NAME):
    DB_NAME = "flipKart_Scrapping_DB"  # Specifiy a Database Name
    # Connection URL
    CONNECTION_URL = f"mongodb+srv://harish:haresh2019@cluster0.4ouqh.mongodb.net/DB_NAME?retryWrites=true&w=majority"
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
    # Establish a connection with mongoDB
    client = pymongo.MongoClient(CONNECTION_URL)
    # Create a DB
    dataBase = client[DB_NAME]
    # db = dbConn['flipKart_Scrapping_DB'] # connecting to the database called flipKart_Scrapping_DB
    # Create a Collection Name

    # creating connection to the collection
    collection = dataBase[PRODUCT]
    review = collection.find()
    data = pd.DataFrame(list(review))
    df = data[['Product_name', 'Price']].drop_duplicates()
    plt1.plot(df['Product_name'], df['Price'])
    plt1.xlabel('Product Name')
    plt1.ylabel('Price')
    plt1.title("Price vs models")
    plt1.xticks(rotation=90)
    plt1.savefig('static/prices.jpeg', bbox_inches='tight')

    return PRODUCT_NAME



@app.route('/')
def index_page():
    """
    * method: index_page
    * description: method to call index html page
    * return: index.html
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          23-JAN-2021    1.0      initial creation
    *
    * Parameters
    *   None
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    * method: predict
    * description: method to predict
    * return: index.html
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          20-JAN-2021    1.0      initial creation
    *
    * Parameters
    *   None
    """
    if request.method == 'POST':
        PRODUCT = request.form['PRODUCT']
        PRODUCT_NAME = request.form["PRODUCT_NAME"]


        output = opinion_graph(PRODUCT, PRODUCT_NAME)
        output1 = opinion_graph(PRODUCT, PRODUCT_NAME)


        return render_template('result.html', prediction=output, show_hidden=True, prediction_text='Product name is  {}'.format(output))






if __name__ == "__main__":
    app.run(debug=True)