from flask import Flask, render_template, request

import filimo

app = Flask(__name__)

# Route for the form page
@app.route('/')
def index():
    return render_template('input_page.html')

# Route for handling the form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get the URLs from the form
    urls = []
    for key, value in request.form.items():
        if key.startswith('url'):
            urls.append(value)

    # Print the URLs
    print(f"Received the following URLs: {urls}")
   
    # Collect data from the URLs
    try:
        filimo_instance = filimo.Filimo(urls) 
        filimo_instance.collect_reviews()
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('errorPage.html', message=error_message), 500
    
    # Display the results
    return render_template('result_page.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)