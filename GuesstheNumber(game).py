import random

def guess_the_number():
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")
    secret_number = random.randint(1, 100)
    attempts = 0
    
    while True:
        guess = input("Enter your guess (or 'q' to quit): ")
        
        if guess.lower() == 'q':
            print("Thanks for playing! The secret number was", secret_number)
            break
        
        try:
            guess = int(guess)
            attempts += 1
            
            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print("Congratulations! You've guessed the secret number in", attempts, "attempts!")
                break
                
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    guess_the_number()
