import pandas as pd

# Read the data from the raw CSV file
df = pd.read_csv("../data/raw_products.csv")

# Drop unnecessary columns
columns_to_drop = ['images', 'thumbnail', 'meta'] 
df = df.drop(columns=columns_to_drop)

# Covert the content of tags to a list
df['tags'] = df['tags'].apply(lambda x: x if isinstance(x, list) else x.split(', '))

# Create a new column 'subcategory' containing only the second tag
df['subcategory'] = df['tags'].apply(lambda x: x[1] if len(x) > 1 else None)

# Remove leading/trailing quotes and spaces
df['subcategory'] = df['subcategory'].astype(str).str.strip().str.replace('"', '').str.replace("'", "").str.replace(']', '').str.replace('[', '').str.replace('womens watches', 'watches')

# Remove tags column as it's no longer needed
df = df.drop(columns=['tags'])

import ast

def safe_eval(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return None
    return x

df['dimensions'] = df['dimensions'].apply(safe_eval)

# Flatten the dictionaries in 'dimensions' into separate columns
dimensions_flat = pd.json_normalize(df['dimensions'])

# Add flattened columns to the main df
df[['width', 'height', 'depth']] = dimensions_flat

# Now you can drop the original nested column
df.drop(columns=['dimensions'], inplace=True)

# Check the result
print(df[['id', 'width', 'height', 'depth']].head())

# Drop columns that are not needed
df.drop(columns=['reviews', 'description'] , inplace=True)

# Fill missing values in 'brand' with 'Unknown'
df['brand'] = df['brand'].fillna('Unknown')

# Save the cleaned data to a new CSV file
df.to_csv("../data/transformed_products.csv", index=False)
