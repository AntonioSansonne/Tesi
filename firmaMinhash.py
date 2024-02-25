from datasketch import MinHash

def custom_intersection_hash(intersection_data):
    minhash = MinHash()
    # Aggiungi i dati dell'incrocio alla firma Minhash
    for word in intersection_data.split():
        minhash.update(word.encode('utf8'))
    return minhash

input_data = "Via Calo"
input_data2 = "Via Calò"
output1 = custom_intersection_hash(input_data)
output2 = custom_intersection_hash(input_data2)

# Calcola la similarità tra le firme Minhash
similarity = output1.jaccard(output2)
print(f"Input 1: {input_data}, Input 2: {input_data2}, Jaccard Similarity: {similarity}")
print(f"Output 1: {output1}, Output 2: {output2}")
