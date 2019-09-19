import json
import os
import urllib.request
from app import app
from client import pre_process, post_process, load_image_into_numpy_array, format_mask 
from flask import Flask, flash, request, redirect, render_template, send_from_directory
import requests
from werkzeug.utils import secure_filename
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import label_map_util
from PIL import Image

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
	 # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# flash('File successfully uploaded')
			image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			base=os.path.basename(image_path)
			output_directory = "./object_detection/test_images/"
			input_filename = os.path.splitext(base)[0]
			output_filename = "out_" + os.path.splitext(base)[0]
			output_json_path = output_directory + os.path.splitext(base)[0] + ".json"  
			output_image_path = output_directory + output_filename + ".jpeg"  
			save_output_image = True
			json_resp = detect_objects(image_path, output_json_path, output_image_path, save_output_image)
			return send_from_directory(output_directory, (output_filename + ".jpeg"))
			# return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def detect_objects(image_path, output_json_path, output_image_path, save_output_image):
	# Map args to var
	server_url = app.config['SERVER_URL'] # args.server_url
	path_to_labels = app.config['PATH_TO_LABELS'] # args.label_map

	# Build input data
	print(f'\n\nPre-processing input file {image_path}...\n')
	formatted_json_input = pre_process(image_path)
	print('Pre-processing done! \n')

	# Call tensorflow server
	headers = {"content-type": "application/json"}
	print(f'\n\nMaking request to {server_url}...\n')
	server_response = requests.post(server_url, data=formatted_json_input, headers=headers)
	print(f'Request returned\n')

	# Post process output
	print(f'\n\nPost-processing server response...\n')
	image = Image.open(image_path).convert("RGB")
	image_np = load_image_into_numpy_array(image)
	output_dict = post_process(server_response, image_np.shape)
	print(f'Post-processing done!\n')

	# Save output on disk
	print(f'\n\nSaving output to {output_json_path}\n\n')
	with open(output_json_path, 'w+') as outfile:
		json_resp = json.loads(server_response.text)
		json.dump(json_resp, outfile)
	print(f'Output saved!\n')

	if save_output_image:
		# Save output on disk
		category_index = label_map_util.create_category_index_from_labelmap(path_to_labels, use_display_name=True)

		# Visualization of the results of a detection.
		vis_util.visualize_boxes_and_labels_on_image_array(
			image_np,
			output_dict['detection_boxes'],
			output_dict['detection_classes'],
			output_dict['detection_scores'],
			category_index,
			instance_masks=output_dict.get('detection_masks'),
			use_normalized_coordinates=True,
			line_thickness=8,
			)
		Image.fromarray(image_np).save(output_image_path)
		print('\n\nImage saved\n\n')
	return json_resp

if __name__ == "__main__":
	app.run()
