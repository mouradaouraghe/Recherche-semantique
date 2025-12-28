# Define a function to combine the relevant features into a single string
def create_product_text(product):
  return f"""Title: {product["title"]}
Description: {product["short_description"]}
Category: {product["category"]}
Features: {', '.join(product["features"])}"""

# Combine the features for each product
product_texts = [create_product_text(product) for product in products]
def create_embeddings(texts):
response = openai.Embedding.create(
model="text-embedding-3-small",
input=texts
)
response_dict = response.model_dump()
return [data['embedding'] for data in response_dict['data']]


# Create the embeddings from product_texts
product_embeddings = create_embeddings(product_texts)
def find_n_closest(query_vector, embeddings, n=3):
  distances = []
  for index, embedding in enumerate(embeddings):
    # Calculate the cosine distance between the query vector and embedding
    dist = distance.cosine(query_vector,embedding)
    # Append the distance and index to distances
    distances.append({"distance": dist, "index": index})
  # Sort distances by the distance key
  distances_sorted = sorted(distances,key=lambda x: x["distance"])
  # Return the first n elements in distances_sorted
  return distances_sorted[0:n]
  # Create the query vector from query_text
query_text = "computer"
query_vector = create_embeddings(query_text)[0]

# Find the five closest distances
hits = find_n_closest(query_vector, product_embeddings,n=5)
print(f'Search results for "{query_text}"')
for hit in hits:
  # Extract the product at each index in hits
  product = products[hit["index"]]
  print(product["title"])



######################
# Combine the features for last_product and each product in products
last_product_text = create_product_text(last_product)
product_texts = [create_product_text(product) for product in products]

# Embed last_product_text and product_texts
last_product_embeddings = create_embeddings(last_product_text)[0]
#print(last_product_embeddings)
product_embeddings = create_embeddings(product_texts)

# Find the three smallest cosine distances and their indexes
hits = find_n_closest(last_product_embeddings, product_embeddings)

for hit in hits:
  product = products[hit['index']]
  print(product['title'])
