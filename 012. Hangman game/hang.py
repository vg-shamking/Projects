import random


def hangman():
    word = random.choice(["water", "tiger", "superman", "pokemon", "avengers",
                          "dark", "earth", "another", "greatest", "winner"])
    valid_letters = 'abcdefghijklmnopqrstuvxyz'
    turns = 10
    guess_made = ''
    while len(word) > 0:
        main = ""
        missed = 0
        for letter in word:
            if letter in guess_made:
                main = main + letter
            else:
                main = main + "_" + ""
        if main == word:
            print(main)
            print("You won!")
            break
        print("Guess the word:", main)
        guess = input()

        if guess in valid_letters:
            guess_made = guess_made + guess
        else:
            print("Enter a valid character: ")
            guess = input()
        if guess not in word:
            turns = turns - 1
            if turns == 9:
                print("9 turns left")
                print("------------")
                print("---\-0-/----")
                print("-----|------")
                print("----/-\-----")
            if turns == 8:
                print("8 turns left")
                print("------------")
                print("---\-0------")
                print("-----|\-----")
                print("----/-\-----")
            if turns == 7:
                print("7 turns left")
                print("------------")
                print("-----0------")
                print("----/|\-----")
                print("----/-\-----")
            if turns == 6:
                print("6 turns left")
                print("------------")
                print("-----0------")
                print("----/-\-----")
                print("----/-\-----")
            if turns == 5:
                print("5 turns left")
                print("-----?------")
                print("-----0------")
                print("----/|\-----")
                print("----/-\-----")
            if turns == 4:
                print("4 turns left")
                print("----???-----")
                print("-----0------")
                print("----/|\-----")
                print("----/-\-----")
            if turns == 3:
                print("3 turns left")
                print("----????----")
                print("-----0------")
                print("----/|\-----")
                print("----/-\-----")
            if turns == 2:
                print("2 turns left")
                print("------------")
                print("---\-0_/----")
                print("-----|------")
                print("----/-\-----")
            if turns == 1:
                print("Last turn left")
                print("------------")
                print("---\-0_|/---")
                print("-----|------")
                print("----/-\-----")
            if turns == 0:
                print("You killed kind man!")
                print("------|-----")
                print("-----0|-----")
                print("----/|\-----")
                print("----/-\-----")


name = input("Enter your gaming name: ")
print("Welcome", name)
print("---------------------------------------!")
print("Try to guess word in less than 10 tries!")
hangman()
print()
