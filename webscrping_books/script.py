import requests
from bs4 import BeautifulSoup
import pandas as pd

Base_Url= "http://books.toscrape.com/catalogue/page-{}.html"

titles =[]
prices = []
stocks =[]

for page in range(1,6):
    url = BASE_URL.format(page)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            # Extract title
            title = book.h3.a["title"]
            titles.append(title)

            # Extract price
            price = book.find("p", class_="price_color").text[1:]  # Remove £ sign
            prices.append(price)

            # Extract stock status
            stock = book.find("p", class_="instock availability").text.strip()
            stocks.append(stock)


df = pd.DataFrame({"Title": titles, "Price (£)": prices, "Availability": stocks})

# Save to CSV
df.to_csv("scraped_books.csv", index=False)

print("✅ Data scraped and saved to scraped_books.csv")