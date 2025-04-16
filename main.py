from nltk.corpus.reader import reviews

from src.scraping import comments_extraction, web_page_extraction
from src.analysis import review_comments_cleaning, visualisation, clusters
from src.analysis.visualisation import generate_wordcloud

generate_wordcloud()

def main_meniu():
    print("\nPasirinkite veiksmą:")
    print("1. Extracting restaurants")
    print("2. Extracting reviews")
    print("3. Cleaning data")
    print("4. Visualisation")
    print("5. Clustering")
    print("6. Exit")
    choice = input("Choose number between 1 and 6: ")
    return choice

def restaurant_scraping():
    print("\nStarting WebSraping and review extraction...")
    web_page_extraction.main()
    print("WebSraping complete.")

def reviews_scraping():
    print("\nStarting review extraction...")
    comments_extraction.main()
    print("Review extraction complete.")

def data_cleaning():
    print("\nCleaning data...")
    review_comments_cleaning.main()
    print("Data cleaned.!")

def visualisation_main():
    print("\nStarting visualisation...")
    visualisation.main()
    print("Data visualisation completed.!")

def clustering():
    print("\nStarting Clustering...")
    clusters.main()
    print("Clustering complete.!")


def main():
       while True:
        choise = main_meniu()
        if choise == "1":
            restaurant_scraping()
        elif choise == "2":
            reviews_scraping()
        elif choise == "3":
            data_cleaning()
        elif choise == "4":
            visualisation_main()
        elif choise == "5":
            clustering()
        elif choise == "6":
            print("Exiting...!")
            break
        else:
            print("Wrong input, please try again.")

if __name__ == '__main__':
    main()