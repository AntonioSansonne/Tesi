def tokenStem(input):
    from nltk.stem import PorterStemmer
    import re
    output = []
    def custom_intersection_hash(intersection_data):
        # Tokenizzazione
        tokens = re.findall(r'\w+', intersection_data.lower())
        # Stemming
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return " ".join(stemmed_tokens)
    # controllo per ogni elemento
    for i in input:
        _output = custom_intersection_hash(i)
        print(f"Input: {i}, Stemmed Text: {_output}")
        output.append(_output)
    return output

def levenstein(output):
    from Levenshtein import distance
    # controllo per ogni elemento
    for i in range(len(output) - 1):
        print("output i ", output[i])
        l_dist = distance(output[i], output[i + 1])
        # qui al posto del controllo può andarci un algoritmo più elaborato per indicare che effettivamente si stia percorrendo una strada diversa
        # come per esempio:
        # se distanzaLev > 3 allora sono certo che si tratta di parole diverse
        if l_dist == 0:
            print("La distanza di Levenshtein tra " + output[i] + " & " + output[i + 1] + " è " + str(l_dist) + "\nStai percorrendo la stessa strada")
        else:
            print("La distanza di Levenshtein tra " + output[i] + " & " + output[i + 1] + " è " + str(l_dist) + "\nStai percorrendo una strada diversa")


#input_data = ["Via 1 Calò", "Via I Calo", "Via 1° Calo'"]
#output_data = tokenStem(input_data)
#print("A: ",output_data)
#levenstein(output_data)
