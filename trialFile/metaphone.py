import metaphone

def custom_intersection_hash(intersection_data):
    metaphone_code = metaphone.doublemetaphone(intersection_data)
    return metaphone_code

input_data = "Via Calò"
output = custom_intersection_hash(input_data)
print(f"Input: {input_data}, Metaphone Code: {output}")
