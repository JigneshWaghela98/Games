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
#Highest Score is 1 by Jignesh & Jayendra, 2 attempts by Jayendra Yadav(3),2 attempts by Jignesh(4) and Madhuri!!

'''from flask_cors import CORS
CORS(app) 
@app.route('/', methods=['POST'])
def handle_user_input_route():
    data = request.get_json()
    if 'text' in data:
        text = data['text'].lower()
        r = query_llm(text).strip()  # Strip whitespace from both ends
        print(r)  # Check the value of r
        
        # Adjusted conditional check
        commands =['open dao', 'open game', 'open marketplace', 'open whitepaper', 'open start exploring', 'open blog', 'open with wallet', 'open with guest', 'open culture', 'open culture store', 'open homepage', 'open glamour', 'open glamour store', 'open ram mandir', 'open Khatushyam mandir', 'open tirupati mandir', 'open prem mandir', 'open mahakaleshwar mandir', 'open saibaba mandir', 'open moreshwar mandir', 'open siddhivinayak mandir', 'open burjkhalifa', 'open cupid hub', 'open celebrity palace', 'open dwood shop', 'open gold souk', 'open restaurant', 'open villa', 'open nude museum', 'open nexus game', 'open roulette game', 'open cricket stadium', 'open ariba zone', 'open indus zone', 'open login']
        if r in commands:
            response_text = handle_user_input(r)
            return response_text
        else:
            res = user_inputs(text)
            return jsonify({'response_text': res})
    else:
        return jsonify({'response_text': 'please say it again'})'''