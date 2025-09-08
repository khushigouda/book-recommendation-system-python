
# 🧾 Book Recommender System

_Popularity and Collaborative Filtering based book recommendation system. Predicts whether a user will like a particular book from collaborative-neighborhood features derived from item–item similarity_

---

##  Table of Contents
- <a href="#overview">Overview</a>
- <a href="#applications">Applications</a>
- <a href="#dataset">Dataset</a>
- <a href="#tools--technologies">Tools & Technologies</a>

- <a href="#data-cleaning--preparation">Data Cleaning & Preparation</a>
- <a href="#project-description">Project Description</a>

- <a href="#conclusions">Conclusions</a>
- <a href="#contact">Contact</a>

---
<h2><a class="anchor" id="overview"></a>Overview</h2>

This project builds a book recommender that combines a popularity-based model with a collaborative filtering model using the Book-Crossing dataset of books, users, and ratings. It  performs exploratory statistics, and then generates recommendations from both overall popularity and user–item similarity computed.

---
<h2><a class="anchor" id="applications"></a>Applications</h2>

- Enhances user experience on e-commerce or online library platforms
- Helps users discover books they might enjoy based on their reading history
- Supports personalized content delivery in educational or entertainment apps

---
<h2><a class="anchor" id="dataset"></a>Dataset</h2>


- Book data – (ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher, Image-URL-S, Image-URL-M, Image-URL-L)
- Users data - (User-ID, Location, Age)
- Ratings data - (User-ID, ISBN, Book-Rating)
- Dataset link: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

---

<h2><a class="anchor" id="tools--technologies"></a>Tools & Technologies</h2>

- Python (Pandas, NumPy, Scikit-learn)
- GitHub

---
<h2><a class="anchor" id="data-cleaning--preparation"></a>Data Cleaning & Preparation</h2>

- Dropped missing values, duplicate and unique values were found and analysed.
- Performed EDA

---
<h2><a class="anchor" id="project-description"></a>Project Description</h2>

1. **Popularity model:**
- Groupby/aggregate to compute counts and mean ratings, then rank to identify top books by engagement and quality signals. Gives top 50 vendors by mean ratings.
2. **Collaborative filtering:**
- Builds a sparse user–item matrix via pivot, then applies cosine similarity and k-nearest neighbors from scikit-learn to find and recommend similar items.
- Implemented RapidFuzz to handle typos, whitespace variations, and capitalization differences in order to accurately match user inputs to the correct book title.
- Recommend() function to recommend similar books based on user ratings.
3. **Logistic regression classifiers:** 
- One uses metadata and ID features to predict whether a user’s rating is a “like” (rating ≥ 7), and another predicts “will like” from collaborative-neighborhood features derived from item–item similarity, with decision made by a tuned probability threshold.
- The metadata model predicts like-probability for any row with the required features, enabling bulk scoring of user–book pairs from the merged table.
- The neighborhood model exposes will_like(book_name, user_id), which resolves a title to a known ISBN, computes features for that user–item, and returns “Yes” if the predicted probability exceeds the tuned threshold

---

<h2><a class="anchor" id="conclusions"></a>Conculsions</h2>

- Lists of top 10 popular books with rating counts and average ratings include the Harry Potter series, The Fellowship of the Ring, The Two Towers and To Kill a Mocking Bird.
- Ratings are highly sparse and skewed: many entries are zeros, with median rating at 0 and the 75th percentile at 7, indicating an implicit/explicit split that motivates filtering and robust thresholding for “like” definitions.

---
<h2><a class="anchor" id="contact"></a>Contact</h2>

**Khushi Gouda**

📧 Email: khushiriyadh@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/khushi-s-84b08b28b/)  

