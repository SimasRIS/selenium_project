import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud



file_path = 'C:/Users/simas/PycharmProjects/selenium_project/data/processed/cleaned_review_comments.csv'

df = pd.read_csv(file_path)

# Lietuviski stop words
lithuanian_stop_words = [
    "ir", "su", "kad", "yra", "taip", "o", "ne", "į", "jis", "ji", "ar", "tai",
    "es", "buvo", "be", "kaip", "nuo", "prie", "už", "apie", "nors", "nei", "i",
    "uz", "bet"
]

# Reitingu pasiskirstymas
def reiting_destribution():
        # Suskaiciuoja kiek kartu kiekvienas reitingas pasikartoja
        rating_score = df['Star Score'].value_counts().sort_index()

        # Kuriame bar diagrama
        plt.figure(figsize=(8, 6))
        plt.bar(rating_score.index, rating_score.values)
        plt.xlabel('Rating Score')
        plt.ylabel('Count')
        plt.title('Rating Score Distribution')
        plt.show()

# Ieskome dazniausiai vartojamu zodziu atsiliepimuose
def most_used_words():

    # Pasaliname stop words is komentaru
    vectorizer = TfidfVectorizer(stop_words=lithuanian_stop_words)
    cleaned_reviews = vectorizer.fit_transform(df['Comment'])

    # Istraukiame zodzius
    words = vectorizer.get_feature_names_out()

    # Susumuojame zodziu(balus) is visu komentaru
    sumed_words = cleaned_reviews.sum(axis=0)

    # Konvertuojame rezultatus i viena sarasa
    scores = sumed_words.tolist()[0]

    # Sukuriame DataFrame su zodziais ir rezultatais
    words_df = pd.DataFrame({'words': words, 'scores': scores})

    top_words = words_df.sort_values('scores', ascending=False).head(10)

    # Vizualizuojame su matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(top_words['words'], top_words['scores'])
    plt.xlabel('Words')
    plt.ylabel('Scores')
    plt.title('Top 10 Most Used Words in Reviews')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def generate_wordcloud():
    text = " ".join(df['Comment'].values)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Ieskome atsiliepimu kiekio pasiskirstymo pagal datas
def review_count_by_date():
    date_counts = df["Review Date"].value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    plt.plot(date_counts.index, date_counts.values, marker='o')
    plt.xlabel('Review Date')
    plt.ylabel('Review Count')
    plt.title('Review Date Distribution by Review Date')
    plt.xticks(rotation=45)
    plt.tight_layout() # pritaiko maketa, kad data nebutu sutampanti
    plt.show()


def main():
    reiting_destribution()
    most_used_words()
    review_count_by_date()
    generate_wordcloud()

if __name__ == '__main__':
    main()








