# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# 
# app = Flask(__name__)
# 
# UPLOAD_FOLDER = 'source_documents'
# ALLOWED_EXTENSIONS = {'pdf', 'csv', 'docx'}
# 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # Check if the POST request has the file part
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
# 
#     file = request.files['file']
# 
#     # If user does not select file, browser also submits an empty part without filename
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
# 
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return jsonify({'message': 'File uploaded successfully'}), 200
# 
#     return jsonify({'error': 'File type not allowed'}), 400
# 
# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request
# from werkzeug.utils import secure_filename
# import os
# import subprocess
# 
# app = Flask(__name__)
# 
# UPLOAD_FOLDER = 'source_documents'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 
# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# 
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         
#         # Call `ingest.py`
#         subprocess.run(['python3', 'ingest.py'], check=True)
#         
#         # Call `privateGPT.py`
#         subprocess.run(['python3', 'privateGPT.py'], check=True)
# 
#         return 'File uploaded and scripts executed'
# 
# if __name__ == '__main__':
#     app.run(port=5001, debug=True)
    
from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import subprocess 

app = Flask(__name__)

UPLOAD_FOLDER = 'source_documents'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Call `ingest.py` and wait for it
        print('Starting ingest.py...')
        process = subprocess.Popen(['python3', 'ingest.py'], stdout=subprocess.PIPE)
        for line in process.stdout:
            print(line.decode().strip())
            if line.decode().strip() == "Ingestion complete! You can now run privateGPT.py to query your documents":
                break
        process.wait()

        # Call `privateGPT.py` after ingest.py
        print('Starting privateGPT.py...')
        subprocess.run(['python3', 'privateGPT.py'], check=True)

        return 'File uploaded and scripts executed'

if __name__ == '__main__':
    app.run(port=5001, debug=True)