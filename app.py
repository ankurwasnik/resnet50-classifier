from flask import Flask, redirect, url_for , render_template , request , flash
from werkzeug.utils import secure_filename
#from keras.applications.vgg16 import preprocess_input,decode_predictions  , VGG16
from keras.preprocessing.image import load_img , img_to_array
import os
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


          
app = Flask(__name__)
ALLOWDED_EXTENSION = ["png" , "jpg" , "jpeg"]
#model = VGG16()
model = ResNet50(weights='imagenet')

#function 
'''
Name        :allowded_file
Description :A function to know if file uploaded is of valid extension or not
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWDED_EXTENSION

@app.route('/feedback/<msg>/<desc>')
def feedback(msg:str , desc:str=""):
   return f"<h3>{msg}<h3><h5>{desc}</h5>"


@app.route('/')
@app.route('/predict',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      if 'file0' not in request.files :
         flash('No file uploaded')
      userfile = request.files['file0']
      
      if userfile and allowed_file(userfile.filename):
         filepath=f"./static/{secure_filename(userfile.filename)}"
         userfile.save(filepath)
         #return redirect(url_for("feedback", msg="File Uploaded Successfully" , desc="Success"))
         #predict
         image = load_img(filepath , target_size=(224,224))
         image = img_to_array(image)
         image = image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
         image = preprocess_input(image)
         yhat = model.predict(image)
         label = decode_predictions(yhat)
         print(label)
         label = label[0][0]
         classification = '%s (%.2f%%)' %(label[1] , label[2]*100)  
         #srcpath= str(userfile.filename)
         #sendobj = [classification,srcpath]
         print(classification)

         #delete the image
         try :
            os.remove(filepath)
            print(f"file {filepath} deleted successfully")
         except :
            pass
         return render_template('hello.html',prediction=classification )
      else:
         # if file not uploaded or incorrect extension 
         return "Please Upload File with correct extension!"
   else:
      #if get request then serve form to upload image
      return render_template('hello.html')



if __name__ == '__main__':
   app.run(debug = True)

   