from flask import Flask, render_template, request
import os, shutil

from detector.Detector import make_prediction, load_image
from detector.Detector import ankle_ap_view, ankle_oblique_view, ankle_lateral_view
from detector.Detector import foot_ap_view, foot_lateral_view, foot_oblique_view
from detector.GradCam import GradCAM
import cv2
import imutils
import numpy as np

app = Flask("__name__")

uploads_dir = 'static\images'
outputs_dir = 'static\outputs'

def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def precess_predictions(model, img_path):
    '''
        read, preprocess, predict, generate, return
    '''
    # read
    orig = cv2.imread(img_path)

    # preprocess
    img = load_image(img_path, (500,400))

    # predict
    label, i = make_prediction(model, img)

    # generate
    cam = GradCAM(model, i)
    heatmap = cam.compute_heatmap(img)
    
    print(f"GradCAM initialized!")

    heatmap = cv2.resize(heatmap, (orig.shape[1], orig.shape[0]))
    (heatmap, output) = cam.overlay_heatmap(heatmap, orig, alpha=0.5)
    
    cv2.rectangle(output, (0, 0), (340, 40), (0, 0, 0), -1)
    cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    Output = imutils.resize(output, height=1500)

    print("Heatmap Created!")
    
    return Output, label

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/process_images', methods=['POST'])
def process_images():
    # read post request files
    xray_type = request.form['xray_type']
    ap_view = request.files['ap_view']
    lateral_view = request.files['lateral_view']
    oblique_view = request.files['oblique_view']
    
    # Clear Folder content
    clear_folder(os.path.join(uploads_dir, "foot"))
    clear_folder(os.path.join(uploads_dir, "ankle"))
    
    # Save images
    if xray_type == "foot":
        ap_view.save(os.path.join(uploads_dir, fr"foot\ap.{ap_view.filename.split('.')[1]}"))
        lateral_view.save(os.path.join(uploads_dir, fr"foot\lateral.{lateral_view.filename.split('.')[1]}"))
        oblique_view.save(os.path.join(uploads_dir, fr"foot\oblique.{oblique_view.filename.split('.')[1]}"))

        ap_out, ap_label = precess_predictions(foot_ap_view, os.path.join(uploads_dir, fr"foot\ap.{ap_view.filename.split('.')[1]}"))
        lateral_out, lateral_label = precess_predictions(foot_lateral_view, os.path.join(uploads_dir, fr"foot\lateral.{lateral_view.filename.split('.')[1]}"))
        oblique_out, oblique_label = precess_predictions(foot_oblique_view, os.path.join(uploads_dir, fr"foot\oblique.{oblique_view.filename.split('.')[1]}"))

        status = cv2.imwrite(os.path.join(outputs_dir, fr"ap.{ap_view.filename.split('.')[1]}"), ap_out)
        print("ap-view output status: ", status)
        status = cv2.imwrite(os.path.join(outputs_dir, fr"lateral.{lateral_view.filename.split('.')[1]}"), lateral_out)
        print("lateral-view output status: ", status)
        status = cv2.imwrite(os.path.join(outputs_dir, fr"oblique.{oblique_view.filename.split('.')[1]}"), oblique_out)
        print("oblique-view output status: ", status)



    else:
        ap_view.save(os.path.join(uploads_dir, fr"ankle\ap.{ap_view.filename.split('.')[1]}"))
        lateral_view.save(os.path.join(uploads_dir, fr"ankle\lateral.{lateral_view.filename.split('.')[1]}"))
        oblique_view.save(os.path.join(uploads_dir, fr"ankle\oblique.{oblique_view.filename.split('.')[1]}"))

        ap_out, ap_label = precess_predictions(ankle_ap_view, os.path.join(uploads_dir, fr"ankle\ap.{ap_view.filename.split('.')[1]}"))
        lateral_out, lateral_label = precess_predictions(ankle_lateral_view, os.path.join(uploads_dir, fr"ankle\lateral.{lateral_view.filename.split('.')[1]}"))
        oblique_out, oblique_label = precess_predictions(ankle_oblique_view, os.path.join(uploads_dir, fr"ankle\oblique.{oblique_view.filename.split('.')[1]}"))

        status = cv2.imwrite(os.path.join(outputs_dir, fr"ap.{ap_view.filename.split('.')[1]}"), ap_out)
        print("oblique-view output status: ", status)
        status = cv2.imwrite(os.path.join(outputs_dir, fr"lateral.{lateral_view.filename.split('.')[1]}"), lateral_out)
        print("oblique-view output status: ", status)
        status = cv2.imwrite(os.path.join(outputs_dir, fr"oblique.{oblique_view.filename.split('.')[1]}"), oblique_out)
        print("oblique-view output status: ", status)

    print("ap-view: ", ap_label)
    print("lateral-view: ", lateral_label)
    print("oblique-view: ", oblique_label)
    
    return render_template('results.html', xray_type=xray_type)

if __name__ == '__main__':
    app.run(debug=True)
