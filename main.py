import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Label, Entry, Button, Text, END

# Data Preparation
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
path = r'C:\Users\theam\Downloads\file.tsv'
df = pd.read_csv(path, sep='\t', names=column_names)

movie_titles = pd.read_csv(r'C:\Users\theam\Downloads\Movie_Id_Titles.csv')
data = pd.merge(df, movie_titles, on='item_id')

# Calculate mean and count of ratings
ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
ratings['num of ratings'] = data.groupby('title')['rating'].count()

# Create pivot table
moviemat = data.pivot_table(index='user_id', columns='title', values='rating')

# GUI Implementation
def recommend_movies():
    movie_name = movie_entry.get()
    output_text.delete(1.0, END)  # Clear previous results

    if movie_name in moviemat.columns:
        movie_ratings = moviemat[movie_name]
        similar_movies = moviemat.corrwith(movie_ratings)
        corr_movies = pd.DataFrame(similar_movies, columns=['Correlation'])
        corr_movies.dropna(inplace=True)
        corr_movies = corr_movies.join(ratings['num of ratings'])

        recommendations = corr_movies[corr_movies['num of ratings'] > 100].sort_values('Correlation', ascending=False).head()

        output_text.insert(END, f"Recommendations for '{movie_name}':\n\n")
        for title, row in recommendations.iterrows():
            output_text.insert(END, f"{title} (Correlation: {row['Correlation']:.2f}, Ratings: {int(row['num of ratings'])})\n")
    else:
        output_text.insert(END, f"'{movie_name}' not found in the dataset. Please try another movie.")

# Create GUI window
root = Tk()
root.title("Movie Recommendation System")

# GUI Components
Label(root, text="Enter a movie name:").grid(row=0, column=0, padx=10, pady=10)
movie_entry = Entry(root, width=40)
movie_entry.grid(row=0, column=1, padx=10, pady=10)

recommend_button = Button(root, text="Recommend", command=recommend_movies)
recommend_button.grid(row=0, column=2, padx=10, pady=10)

output_text = Text(root, height=15, width=80)
output_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()
