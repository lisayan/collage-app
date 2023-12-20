from flask import Flask, render_template, request, send_from_directory, jsonify
from PIL import Image
import os

app = Flask(__name__,
            template_folder='/Users/lisayan/Documents/collage_app/')
app.config['TEMPLATES_AUTO_RELOAD'] = True

UPLOAD_FOLDER = 'uploads'
COLLAGE_FOLDER = 'collages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COLLAGE_FOLDER'] = COLLAGE_FOLDER

if not os.path.exists(app.config['COLLAGE_FOLDER']):
    os.makedirs(app.config['COLLAGE_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_collage(image_paths, collage_path):
    images = [Image.open(path) for path in image_paths]

    # Assuming all images have the same size, you may need to resize them if needed
    width, height = images[0].size
    collage = Image.new('RGB', (width * len(images), height), 'white')

    for i, img in enumerate(images):
        collage.paste(img, (i * width, 0))

    collage.save(collage_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print('uploading')
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({'status': 'success', 'filename': file.filename})

    return jsonify({'status': 'error', 'message': 'Invalid file format'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/collage')
def generate_collage():
    upload_folder = app.config['UPLOAD_FOLDER']
    collage_folder = app.config['COLLAGE_FOLDER']
    uploaded_images = [os.path.join(upload_folder, file) for file in os.listdir(upload_folder) if
                       allowed_file(file)]

    if not uploaded_images:
        return jsonify({'status': 'error', 'message': 'No images uploaded for collage.'})

    collage_filename = 'collage.jpg'
    collage_path = os.path.join(collage_folder, collage_filename)
    create_collage(uploaded_images, collage_path)

    return jsonify({'status': 'success', 'collage_filename': collage_filename})

if __name__ == '__main__':
    app.run(debug=True)