from flask import Flask, render_template, request, url_for
import os
import subprocess
import shutil
import glob


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        image_files = request.files.getlist('image')
        image_paths = []

        # Create a new static directory to store output iamges
        if os.path.exists('static'):
            shutil.rmtree('static')
        os.makedirs('static')

        for image_file in image_files:
            image_path = os.path.join('uploads', image_file.filename)
            image_file.save(image_path)
            image_paths.append(os.path.basename(image_path))

            # Pass the image_path as an argument to detect.py
            output_dir = 'runs/detect'
            command = f'python detect.py --source "{image_path}" --save-txt --save-conf --project {output_dir} --name result --exist-ok'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()


            # Get the output iamge path
            output_image = os.path.join(output_dir, 'result', os.path.basename(image_path))

            # result = process.stdout.read().decode('utf-8')
            
            # Move the out image to the static dir
            shutil.move(output_image, r"static")
        

        return render_template('result.html', image_filenames=image_paths)
        # return render_template('result.html', image_path=output_image, result=result)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)