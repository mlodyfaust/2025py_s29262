# =============================================
# CEL PROGRAMU I KONTEKST ZASTOSOWANIA
# =============================================
# Program służy do generowania losowej sekwencji DNA zapisanej w formacie FASTA.
# Użytkownik podaje długość sekwencji, nazwę (ID), opis i imię.
# Imię zostaje wstawione w losowym miejscu w sekwencji, ale nie wpływa na jej statystyki.
# Program oblicza procentową zawartość każdego nukleotydu (A, C, G, T) oraz %CG.
# Dane są zapisywane w pliku *.fasta, a wyniki wyświetlane użytkownikowi.

import random  # Importuje bibliotekę random do losowego wyboru liter z listy

# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length):
    """Generuje losową sekwencję DNA o zadanej długości.""" # Print "Generuje losową sekwencję DNA o zadanej długości."
    nucleotides = ['A', 'C', 'G', 'T']  # Lista możliwych nukleotydów w DNA
    return ''.join(random.choice(nucleotides) for _ in range(length))  # Losuje znaki i skleja je w łańcuch

# Funkcja do wstawienia imienia do sekwencji
def insert_name(sequence, name):
    """Wstawia imię użytkownika w losowym miejscu w sekwencji DNA.""" # Print "Wstawia imię użytkownika w losowym miejscu w sekwencji DNA."
    if not name:  # Sprawdza, czy imię nie jest puste
        return sequence  # Zwraca oryginalną sekwencję, jeśli brak imienia
    insert_pos = random.randint(0, len(sequence))  # Wybiera losową pozycję do wstawienia imienia
    return sequence[:insert_pos] + name + sequence[insert_pos:]  # Wstawia imię do sekwencji w wybranym miejscu

# Funkcja do liczenia statystyk nukleotydów
def calculate_stats(sequence):
    """Oblicza procentową zawartość A, C, G, T oraz sumę C+G w sekwencji (ignorując inne znaki).""" # Print "Oblicza procentową zawartość A, C, G, T oraz sumę C+G w sekwencji (ignorując inne znaki)."
    clean_sequence = ''.join([c for c in sequence if c in ['A', 'C', 'G', 'T']])  # Usuwa znaki inne niż ACGT
    total = len(clean_sequence)  # Oblicza długość oczyszczonej sekwencji

    if total == 0:  # Zapobiega dzieleniu przez zero
        return {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'CG': 0}  # Zwraca 0% dla wszystkich

    counts = {  # Tworzy słownik z liczbą wystąpień każdego nukleotydu
        'A': clean_sequence.count('A'), # slownik z A (adenina)
        'C': clean_sequence.count('C'), # slownik z C (cytozyna)
        'G': clean_sequence.count('G'), # slownik z G (guanina)
        'T': clean_sequence.count('T') # slownik z T (tymina)
    }

    stats = {  # Przelicza liczby na wartości procentowe
        'A': (counts['A'] / total) * 100, # Przelicza liczby na wartości procentowe A
        'C': (counts['C'] / total) * 100, # # Przelicza liczby na wartości procentowe C
        'G': (counts['G'] / total) * 100, # # Przelicza liczby na wartości procentowe G
        'T': (counts['T'] / total) * 100, # # Przelicza liczby na wartości procentowe T
        'CG': ((counts['C'] + counts['G']) / total) * 100 # # Przelicza liczby na wartości procentowe C oraz G
    }

    return stats  # Zwraca słownik z wartościami procentowymi

# Funkcja zapisująca sekwencję do pliku FASTA
def save_to_fasta(seq_id, description, sequence, filename):
    """Zapisuje dane w formacie FASTA do pliku.""" # Print  "Zapisuje dane w formacie FASTA do pliku."
    with open(filename, 'w') as f:  # Otwiera plik do zapisu
        f.write(f">{seq_id} {description}\n{sequence}\n")  # Zapisuje dane w formacie FASTA (nagłówek + sekwencja)

# Funkcja główna – główny przebieg programu
def main():
    print("Generator sekwencji DNA w formacie FASTA")  # Wyświetla tytuł programu

    try:
        user_input = input("Podaj długość sekwencji: ")  # Pobiera długość sekwencji od użytkownika
        # MODIFIED: dodano obsługę pustego ciągu oraz wartości domyślnej
        length = int(user_input) if user_input.strip() else 20  # Jeśli pusty ciąg, ustaw 20
        if length <= 0:  # Sprawdza, czy długość > 0
            print("Długość musi być dodatnia. Ustawiam 20.")  # Komunikat o błędzie
            length = 20  # Ustawia wartość domyślną
    except ValueError:  # Obsługuje niepoprawny format (np. litery)
        print("Nieprawidłowa wartość. Ustawiam domyślną długość 20.")  # Komunikat o błędzie
        length = 20  # Domyślna długość

    # MODIFIED: ograniczenie długości sekwencji do maksymalnie 10000
    if length > 10000:  # Sprawdza, czy długość nie przekracza 10 000
        print("Zbyt długa sekwencja. Ograniczam do 10000 znaków.")  # Komunikat o limicie
        length = 10000  # Ustawia długość na 10000

    seq_id = input("Podaj ID sekwencji: ").strip()  # Pobiera identyfikator sekwencji
    description = input("Podaj opis sekwencji: ").strip()  # Pobiera opis sekwencji
    name = input("Podaj imię: ").strip()  # Pobiera imię do wstawienia

    # MODIFIED: sprawdzenie, czy ID i opis nie są puste
    if not seq_id:  # Jeśli ID jest puste
        print("ID nie może być puste. Ustawiam domyślne 'unknown_id'.")  # Komunikat
        seq_id = "unknown_id"  # Ustawienie domyślnego ID

    if not description:  # Jeśli opis jest pusty
        print("Opis nie może być pusty. Ustawiam 'brak opisu'.")  # Komunikat
        description = "brak opisu"  # Ustawienie domyślnego opisu

    # MODIFIED: sprawdzenie poprawności imienia – tylko litery
    if name and not name.isalpha():  # Jeśli imię zawiera znaki inne niż litery
        print("Imię powinno zawierać tylko litery. Pomijam wstawianie imienia.")  # Komunikat
        name = ""  # Pomijamy imię

    dna_sequence = generate_dna_sequence(length)  # Generuje losową sekwencję DNA
    final_sequence = insert_name(dna_sequence, name)  # Wstawia imię w losowym miejscu
    stats = calculate_stats(final_sequence)  # Oblicza statystyki nukleotydów

    filename = f"{seq_id}.fasta"  # Tworzy nazwę pliku wynikowego
    save_to_fasta(seq_id, description, final_sequence, filename)  # Zapisuje sekwencję do pliku

    # Wyświetla statystyki i komunikaty użytkownikowi
    print(f"\nSekwencja zapisana do pliku {filename}")  # Komunikat o zapisie pliku
    print("Statystyki sekwencji:")  # Nagłówek statystyk
    print(f"A: {stats['A']:.1f}%")  # Procentowa zawartość A
    print(f"C: {stats['C']:.1f}%")  # Procentowa zawartość C
    print(f"G: {stats['G']:.1f}%")  # Procentowa zawartość G
    print(f"T: {stats['T']:.1f}%")  # Procentowa zawartość T
    print(f"%CG: {stats['CG']:.1f}")  # Procentowa zawartość C + G

# Sprawdzenie, czy plik został uruchomiony bezpośrednio
if __name__ == "__main__":  # Jeśli uruchamiamy plik bezpośrednio, a nie importujemy
    main()  # Wywołuje funkcję główną

    # =============================================
    # INFORMACJA O MODYFIKACJACH WZGLĘDEM KODU LLM
    # =============================================

    # MODIFIED (dodano obsługę pustego wejścia dla długości, aby uniknąć błędu konwersji):
    # Gdy użytkownik naciśnie Enter bez wpisywania liczby, kod LLM rzuca wyjątkiem przy konwersji do int.
    # Dodano sprawdzenie `if user_input.strip()` i przypisanie domyślnej wartości (20), co pozwala programowi działać płynnie.

    # MODIFIED (dodano sprawdzenie czy długość > 0, aby uniknąć bezsensownej sekwencji):
    # Sekwencja o długości zero lub mniejszej nie ma sensu biologicznego ani technicznego – dodano komunikat i przywrócenie wartości 20.

    # MODIFIED (ograniczono maksymalną długość sekwencji do 10000, aby zabezpieczyć przed przeciążeniem):
    # Bardzo długie sekwencje mogą doprowadzić do dużego obciążenia pamięci lub opóźnienia działania – dodano limit oraz komunikat.

    # MODIFIED (dodano domyślne wartości ID i opisu, aby uniknąć pustych danych w pliku FASTA):
    # Kod LLM zapisywał dane do pliku nawet gdy ID/opis były puste, co prowadziło do nieczytelnych plików – teraz są wartości zastępcze.

    # MODIFIED (dodano walidację imienia, aby nie wstawiać znaków innych niż litery do sekwencji DNA):
    # Jeśli imię zawiera znaki specjalne (np. cyfry, znaki interpunkcyjne), mogą one zaburzyć analizę DNA – teraz dopuszczalne są tylko litery.
