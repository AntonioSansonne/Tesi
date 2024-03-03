# Documentazione
# https://maxbachmann.github.io/Levenshtein/

from Levenshtein import distance

string1 = "Via Calo'"
string2 = "Via Calò"

l_dist = distance(string1, string2)

print("Levenshtein Distance between "+string1+" & "+string2+" is " + str(l_dist))

def custom_intersection_hash(intersection1, intersection2):
    from fuzzywuzzy import fuzz
    similarity = fuzz.ratio(intersection1, intersection2)
    return similarity

input_data1 = "Via Patriota"
input_data2 = "Via patriota"
output = custom_intersection_hash(input_data1, input_data2)
print(f"Input 1: {input_data1}, Input 2: {input_data2}, Similarity: {output}")

