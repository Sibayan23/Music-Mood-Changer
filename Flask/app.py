from flask import Flask, render_template, flash, redirect
from flask import request
from PIL import Image
import glob, os
import cv2, boto3
from pygame import mixer #install
import shutil, random
webapp=Flask("name")
webapp.secret_key='secret key'
	

@webapp.route("/home")
def home():
	return "home page"


@webapp.route("/",methods=['GET'])
def form():
	html=render_template("index.html")
	return html


@webapp.route("/result",methods=['POST'])
def compare():
	uploaded_file = request.files['file']
	if uploaded_file.filename != '':
		uploaded_file.save(uploaded_file.filename)
	X=uploaded_file.filename
	photo=X
	imageSource=open(photo,'rb') 
	img = glob.glob('C:/Users/admin/Desktop/Flask/images1/*.jpeg')
	imageTarget=open(img[0],'rb')
	client=boto3.client('rekognition')
	response=client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    
	if(len(response['FaceMatches'])==1):
		for faceMatch in response['FaceMatches']:
			if faceMatch['Similarity']>90:
				return (render_template("return_compare_pass.html",name=str(faceMatch['Similarity'])))
	else :
		return (render_template("return_compare_fail.html",name="FACE DOES NOT MATCH"))
	imageSource.close()
	imageTarget.close()


@webapp.route("/result1",methods=['POST'])
def mood():
	X=request.form.get("name")
	if X[0]=='y' or X[0]=='Y':
		cap =cv2.VideoCapture(0)
		ret, photo = cap.read() # to click the photo
		Photo="sibayan.jpg"
		cv2.imwrite(Photo,photo) # save the photo
		cap.release() # disconnect the camera
		region='ap-south-1'
		bucket_name='sibayan'
		u_photo='photo.jpeg'
		S3=boto3.resource('s3')
		S3.Bucket(bucket_name).upload_file(Photo,u_photo)
		rek = boto3.client('rekognition' , region )
		res = rek.detect_faces(
     		Image={
          		'S3Object': {
              		'Bucket': bucket_name,
              		'Name': u_photo,
          		}
      		},
    		Attributes = ['ALL']
		)
		if res['FaceDetails'][0]['Smile']['Value'] == False:
			dirpath = "music"
			filename = random.sample(os.listdir(dirpath),1)
			for fname in filename:
				srcpath = os.path.join(dirpath, fname)
			mixer.init() #Initialzing pyamge mixer
			mixer.music.load(srcpath) #Loading Music File
			mixer.music.play() #Playing Music with Pygame
		return (render_template("mood2.html"))
	elif X[0]=='n' or X[0]=='N':
		return (render_template("input1.html"))

@webapp.route("/result2",methods=['POST'])
def mood1():
	uploaded_file = request.files['file']
	X=uploaded_file.filename
	photo=X
	region='ap-south-1'
	bucket_name='sibayan'
	u_photo='photo.jpeg'
	S3=boto3.resource('s3')
	S3.Bucket(bucket_name).upload_file(photo,u_photo)
	rek = boto3.client('rekognition' , region )
	response = rek.detect_faces(
     	Image={
          'S3Object': {
              'Bucket': bucket_name,
              'Name': u_photo,
          }
      	},
    	Attributes = ['ALL']
	)
	if response['FaceDetails'][0]['Smile']['Value'] == False:
		dirpath = "music"
		filename = random.sample(os.listdir(dirpath),1)
		for fname in filename:
			srcpath = os.path.join(dirpath, fname)
		mixer.init() #Initialzing pyamge mixer
		mixer.music.load(srcpath) #Loading Music File
		mixer.music.play() #Playing Music with Pygame
		return (render_template("mood2.html"))

@webapp.route("/result3",methods=['POST'])
def mood2():
	X=request.form.get("name")
	if X[0]=='c' or X[0]=='C':
		dirpath = "music"
		filename = random.sample(os.listdir(dirpath),1)
		for fname in filename:
			srcpath = os.path.join(dirpath, fname)
		mixer.init() #Initialzing pyamge mixer
		mixer.music.load(srcpath) #Loading Music File
		mixer.music.play() #Playing Music with Pygame
		return (render_template("mood2.html"))
	elif X[0]=='P' or X[0]=='p':
		mixer.music.pause()
		return(render_template("mood2.html"))
	elif X[0]=='R' or X[0]=='r':
		mixer.music.unpause()
		return(render_template("mood2.html"))
	else:
		mixer.music.stop()
		return(render_template("mood3.html"))		

webapp.run(debug=True)

