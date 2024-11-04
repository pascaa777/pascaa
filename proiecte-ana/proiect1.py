from collections import Counter

# Word list (masked words and actual words)
word_pairs = [
    ("******RA**", "ICONOGRAFĂ"), ("*A**C****", "FAGOCITUL"), ("*P*C******", "APICOLILOR"),
    ("H**O******", "HIPOPLAZII"), ("**OHO**", "PROHODI"), ("***PL**", "CIOPLEA"),
    ("**V***I*****", "COVÂRȘITELOR"), ("P***U*****", "PÂRGUIRILE"), ("**R***ER**E", "BURGHIERILE"),
    ("**M*****I*II", "SAMAVOLNICII"), ("*Ă*Ă***T*", "CĂȘĂIEȘTE"),
    ("******UR**", "MÂNJITURII"), ("T***R*", "TĂIERI"), ("****IL**IL**", "GENTILEȚILOR"), ("******CI***", "NENOROCITUL"), ("***I*T*", "ÎNAINTĂ"),
    ("******UL", "ISTMICUL"), ("**CU***U****CU*", "ASCUȚITUNGHICUL"), ("O******Ă***O*", "OBNUBILĂRILOR"),
    ("****ĂC******", "BUMBĂCELULUI"), ("****Ă*ĂR****", "POSTĂVĂRIILE"), ("*E********L", "CENTROZOMUL"),
    ("*****U**S*", "DEBAVURASE"), ("V***I**", "VRAMIȚE"), ("**T**I", "RETORI"), ("**I***L***L**", "EPISTOLARELOR"),
    ("***H**B******", "ÎNCHIABUREAȚI"), ("L*********E*", "LAMINATOAREA"), ("******EZ", "PLATINEZ"),
    ("***D*R****", "ȚĂNDĂRELEI"), ("***A**R*", "TEVATURI"), ("****P**E*", "STÂLPISEM"), ("EL**L**", "ELFILOR"), ("**C**C***A*****", "DECONCERTANTELE"),
    ("***I*U*UI", "GAGICULUI"), ("A**LA***", "APELARĂM"), ("*******OF****O*", "SPERMATOFITELOR"),
    ("***R******O***OR", "NECREDINCIOȘILOR"), ("***ST****", "CINSTEȚUL"), ("P*G*******", "PEGMATITUL"), ("***T**E*TE", "PLUTUIEȘTE"), ("*I**E*II", "CINTEZII"), ("*O***I***", "FOLFĂIESC"),
    ("E**E***A**E*", "ESTETIZANTEI"),  ("B*********Ă", "BALAOACHEȘĂ"), ("*O*Ă***Ă", "NOTĂRIȚĂ"), ("D*L***", "DULEȚI"),
    ("****E**S***E*", "RICKETTSIOZEI"), ("C***Ș*", "CIREȘE"), ("*****D*N*", "ARIERDUNĂ"), ("***CI**I", "FLACIDEI"), ("******Ț****L*", "CONVENȚIONALI"),
    ("******ȚĂ", "CUCONIȚĂ"),  ("B********R***", "BIHINDISIRILE"),
    ("***L*N****", "ÎMPLINIREA"), ("I*S*I****", "INSTIGÂND"), ("R*C****", "RECENTE"), ("E***E*Ă", "EMBLEMĂ"),
    ("***G***Ș**", "SINGURAȘUL"), ("****E**ET******", "SUBSECRETARULUI"), ("*E*********E*Ă*", "DEVITALIZASERĂM"),
    ("*****R**I**", "SUBAPRECIEZ"), ("CL*****L**", "CLASATULUI"), ("**R**N****", "FARAONICUL"),
    ("**RO**R**OR", "ÎNROLĂRILOR"), ("*R*****U", "PRIMEZIU"), ("C**C*A*****", "CRUCIATULUI"),
    ("P*O********", "PRODIGATELE"), ("**NA", "VINA"), ("**FR*R**", "CIFRARĂM"),
    ("********S*M", "ÎNFRUNTASEM"), ("**OȘ***", "VIOȘELI"), ("********ĂȚ*", "AMUȘISERĂȚI"),
    ("*E*E*R****R*", "TELEGRAFIARĂ"), ("******AD***", "CITRONADELE")
]

# Romanian language vowel set
vowels = set("AEIOUĂÎ")


# Step 1: Calculate letter frequencies based on word lengths
def calculate_letter_frequencies_by_length(words):
    length_based_frequencies = {}
    for _, word in words:
        word_length = len(word)
        if word_length not in length_based_frequencies:
            length_based_frequencies[word_length] = Counter()
        length_based_frequencies[word_length].update(word)
    return length_based_frequencies


# Step 2: Function to simulate guessing for each word
def play_hangman(word_pairs):
    total_guesses = 0
    letter_frequencies_by_length = calculate_letter_frequencies_by_length(word_pairs)

    for masked_word, actual_word in word_pairs:
        guessed_letters = set()
        current_guess = list(masked_word)  # The current state of guessed letters
        tries = 0

        # Separate vowels and consonants in the letter frequency list
        word_length = len(actual_word)
        freq_by_length = letter_frequencies_by_length[word_length]
        sorted_vowels = [item[0] for item in freq_by_length.most_common() if item[0] in vowels]
        sorted_consonants = [item[0] for item in freq_by_length.most_common() if item[0] not in vowels]

        # Step 3: Guess vowels first
        for letter in sorted_vowels + sorted_consonants:
            if letter in actual_word and letter not in guessed_letters:
                guessed_letters.add(letter)
                for i, char in enumerate(actual_word):
                    if char == letter:
                        current_guess[i] = letter
            tries += 1

            # Stop if the word is fully guessed
            if ''.join(current_guess) == actual_word:
                break

        # Log progress for each word
        print(f"Guessed word: {''.join(current_guess)} in {tries} tries.")
        total_guesses += tries

    return total_guesses


# Step 4: Play the hangman game and calculate total guesses
total_tries = play_hangman(word_pairs)
print(f"Total tries: {total_tries}")
