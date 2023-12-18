from flask import Flask, render_template, request

app = Flask(__name__,
            template_folder='/Users/lisayan/Documents/DemoBuddy/')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    # Save the file to a desired location
    file.save('uploads/' + file.filename)

    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run()