import requests
import pandas as pd

def extract_products(total_needed=200, limit=100):
    all_products = []

    for skip in range(0, total_needed, limit):
        url = f"https://dummyjson.com/products?limit={limit}&skip={skip}"
        response = requests.get(url)
        data = response.json()
        all_products.extend(data['products'])
    return pd.DataFrame(all_products)


if __name__ == "__main__":
    df = extract_products()

# print(df.head())
df.to_csv("raw_products.csv", index=False)

print("Raw data saved to ../data/raw_products.csv")
