from sklearn.neighbors import NearestNeighbors

# Example data
data = [[0, 0], [1, 0], [0, 1], [2, 2], [3, 3]]

# Create a NearestNeighbors model
neigh = NearestNeighbors(n_neighbors=5)

# Fit the model to the data
neigh.fit(data)

# Query for neighbors of a point
query_point = [[1, 1]]
distances, indices = neigh.kneighbors(query_point)

# Print the results
print("Indices of nearest neighbors:", indices)
print("Distances to nearest neighbors:", distances)
