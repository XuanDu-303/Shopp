import numpy as np

# Định nghĩa các hàm cần thiết
def cosine_similarity_manual(matrix):
    similarity = np.dot(matrix, matrix.T)
    norms = np.array([np.sqrt(np.diagonal(similarity))])
    return (similarity / (norms * norms.T))

def knn_predict(user_id, item_id, user_item_matrix, k=5):
    user_index = user_item_matrix.index.get_loc(user_id)
    item_index = user_item_matrix.columns.get_loc(item_id)
    
    similarity_matrix = cosine_similarity_manual(user_item_matrix.values)
    similar_users = np.argsort(similarity_matrix[user_index])[-(k+1):-1]
    
    sum_similarities = np.sum(similarity_matrix[user_index][similar_users])
    weighted_sum = 0.0
    for neighbor in similar_users:
        weighted_sum += similarity_matrix[user_index][neighbor] * user_item_matrix.values[neighbor, item_index]
    
    if sum_similarities == 0:
        return 0
    predicted_rating = weighted_sum / sum_similarities
    return predicted_rating

def recommend_products(user_id, user_item_matrix, k=5, top_n=10):
    userId = str(user_id)
    user_index = user_item_matrix.index.get_loc(userId)
    user_ratings = user_item_matrix.iloc[user_index]
    
    unrated_products = user_ratings[user_ratings == 0].index.tolist()
    
    recommendations = []
    for item_id in unrated_products:
        predicted_rating = knn_predict(userId, item_id, user_item_matrix, k=k)
        itemId = int(item_id)
        recommendations.append((itemId, predicted_rating))
    
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]

def main():
    cosine_similarity_manual()
    knn_predict()
    recommend_products()

if __name__ == "__main__":
    main()