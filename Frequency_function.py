def most_frequent(word):
    letter_freq={}
    for char in word:
        if char.isalpha():
            char=char.lower()
            letter_freq[char]=letter_freq.get(char,0)+1
    sorted_freq=sorted(letter_freq.items(), key=lambda x: x[1],reverse=True)
    for letter,freq in sorted_freq:
        print(f"{letter}:{freq}")

str=input("Please enter a string=")
most_frequent(str)
