print("STARTED")

try:
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import pickle

    print("Libraries imported")

    movies = pd.read_csv("movies.csv")
    print("CSV Loaded")

    print(movies.head())  # debug

    movies = movies[['title', 'overview']].dropna()
    print("Columns selected")

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['overview']).toarray()
    print("Vectorization done")

    similarity = cosine_similarity(vectors)
    print("Similarity calculated")

    pickle.dump(movies, open('movies.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))

    print("Model created successfully!")

except Exception as e:
    print("ERROR OCCURRED:")
    print(e)