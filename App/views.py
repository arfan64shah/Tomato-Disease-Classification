from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
import base64
from PIL import Image
import json
from tensorflow import Graph
from django.contrib import messages
from keras.models import Sequential, load_model
# from tensorflow.keras.utils import img_to_array, load_img
import numpy as np
import tensorflow as tf




def index(request):
    context = {'a': 1}
    return render(request, 'main.html', context)

# def predictImage(request):
#     print(request)
#     print(request.POST.dict())
#     fileObj = request.FILES['filePath']
#     fs = FileSystemStorage()
#     filePathName = fs.save(fileObj.name, fileObj)
#     filePathName = fs.url(filePathName)
#import pickle


#     context = {'filePathName': filePathName}
#     return render(request, 'main.html', context)

model_graph = Graph()

with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model1=load_model('./models/binary_CNN.h5')
        model2 = load_model('./models/multi_CNN.h5')
# with open ('CNN_Classifier','rb') as f:
#     model2= pickle.load(f)

def viewDataBase(request):
    import os
    listOfImages=os.listdir('./media/')
    listOfImagesPath=['./media/'+i for i in listOfImages]
    context={'listOfImagesPath':listOfImagesPath}
    return render(request,'viewDB.html',context)

def binaryClassification(request):
	return render(request, "binaryClassification.html")

def multiClassification(request):
	return render(request, "multiClassification.html")

def predictBinary(request):
    print (request)
    #print (request.POST.dict())
    try:
        fileObj=request.FILES['filePath']
        img_name = default_storage.save(fileObj.name, fileObj)
        
        fs=FileSystemStorage()
        # img_path = default_storage.path(img_name)
        # print(img_path)
        filePathName=fs.save(fileObj.name,fileObj)
        # print("4")
        filePathName=fs.path(filePathName)
        # print(filePathName)
        # testimage='.'+filePathName
        # print("6")
        img = image.load_img(filePathName, target_size=(64, 64))
        pil_img = Image.open(filePathName, mode='r')
        buf = BytesIO()
        pil_img.save(buf, format='PNG')
        img_str = base64.b64encode(buf.getvalue())
        img_str = img_str.decode('utf-8')
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        with model_graph.as_default():
            with tf_session.as_default():
                prediction = model1.predict(x, batch_size=10)
                #print(prediction)    

        context={'filePathName':img_str,'prediction1':prediction[0][0],'prediction2':"pred2"}
        return render(request,'binaryResults.html',context)
    except Exception as e:
        #print(e)
        messages.info(request, 'Please upload an image!')
        return render(request, 'binaryClassification.html')


def predictMulti(request):
    try:
        fileObj=request.FILES['filePath']
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)
        testimage='.'+filePathName
        img = image.load_img(testimage, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        with model_graph.as_default():
            with tf_session.as_default():
                prediction = model2.predict(x)
                print(prediction)
        #with graph.as_default():
        #prediction = model.predict(x, batch_size=10)
        classificationList = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        list_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        x = prediction
        for i in range(10):
            for j in range(10):
                if x[0][list_index[i]] > x[0][list_index[j]]:
                    temp = list_index[i]
                    list_index[i] = list_index[j]
                    list_index[j] = temp

        context={'filePathName':filePathName,'prediction1':classificationList[list_index[0]]}
        return render(request,'multiResults.html',context)
    except:
        

        messages.info(request, 'Please upload an image!')
        return render(request, 'multiClassification.html')