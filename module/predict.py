from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from keras import callbacks
from keras import backend as K


def predict(arsitektur, id_predict):
    img_width, img_height =300,300

    batch_size=1

    print("Mempersiapkan arsitektur")
    architecure_dir = os.path.join('./data/neural_network/'+arsitektur+'/',arsitektur)

    print("Memuat model arsitektur")
    dir_model = os.path.join(architecure_dir, 'models/model.h5')
    model = load_model(dir_model)

    print("Mempersiapkan file & data yang digunakan untuk prediksi")
    data_val_dir = './data/temporary/predict_image/'+id_predict
    train_datagen = ImageDataGenerator(rescale=1./255)

    print("Mulai #Predict ", data_val_dir)
    train_generator = train_datagen.flow_from_directory(
      data_val_dir,
      target_size=(300, 300),
      batch_size=1,
      class_mode='categorical',
      shuffle=False)
    label_map = (train_generator.class_indices)
    print("label_map:", label_map)

    print("Selesai #Predict")

    print("Memuat hasil prediksi")
    filenames = train_generator.filenames
    nb_samples = len(filenames)
    classes_pred = model.predict_generator(train_generator,steps = nb_samples)

    print("Mengirim hasil prediksi")
    K.clear_session()
    return classes_pred


