from flask import Flask, request
app = Flask(__name__)

def process_text(input_text):
    # Your Python function to process the text goes here
    # For example, let's just return the input text reversed
    print(f"The text is {input_text[::-1]}")
    return f"The text is {input_text[::-1]}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['userInput']
        processed_text = process_text(user_input)
        # Return processed text wrapped in HTML tags
        return f'<div>{processed_text}</div>'
        return processed_text
    return 'Hello, this is the homepage'

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Use a different port, such as 8000


# # process_text.py

# def process_text(input_text):
#     # Your Python function to process the text goes here
#     # For example, let's just return the input text reversed
#     return f"The text is {input_text[::-1]}"

# if __name__ == "__main__":
#     import sys
#     input_text = sys.argv[1]
#     processed_text = process_text(input_text)
#     print(processed_text)
