from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
import os
from tinydb import TinyDB, Query
import datetime
from module import dev_preprocessing_multicolor
from module import dev_preprocessing
from module import predict
from module import compare_result_preprocessing
from module import adjusting_result
import base64
import cv2

def encode_img(img):
    """Encodes an image as a png and encodes to base 64 for display."""
    success, encoded_img = cv2.imencode('.jpg', img)
    if success:
        return base64.b64encode(encoded_img).decode()
    return ''

UPLOAD_FOLDER = 'data/temporary/predict_image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
db = TinyDB('data/spesies.json')
tableSpesies = db.table('spesies')

app = Flask(__name__)
api = Api(app)

class Leaf(Resource):
    def get(self):
        obj = tableSpesies.all()
        for index, value in enumerate(obj):
            img = cv2.imread(os.path.join('./data/example_leaf', obj[index]['kode']+'.jpg'), cv2.IMREAD_COLOR)
            b64_src = 'data:image/jpg;base64,'
            encoded_img = encode_img(img)
            gambar = b64_src + encoded_img
            obj[index]['image'] = gambar
        return obj


class Leaf_by_code(Resource):
    def get(self, code_leaf):
        genus = Query()
        return tableSpesies.search(genus.kode == code_leaf)

class Predict(Resource):
    def post(self):
        print("============================Start Process============================")
        print("Mengecek request file ke server...")
        if 'file' not in request.files:
            #flash('No file part')
            return {"result":False, "message":"No file part"}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        print("Mengecek file yang diunggah...")
        if file.filename == '':
            #flash('No selected file')
            print("Tidak dapat membaca file")
            return {"result":False, "message":"No selected file"}


        checkExtension = file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

        id_predict = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        print("Mengecek file dan ekstensi")
        if file and checkExtension:
            filename = secure_filename(file.filename)

            print("Membuat folder penyimpanan gambar")
            if not os.path.exists(UPLOAD_FOLDER + "/" + id_predict):
                os.makedirs(UPLOAD_FOLDER + "/" + id_predict)

            print("Menyimpan gambar")
            file.save(os.path.join(UPLOAD_FOLDER+"/"+id_predict, id_predict+"."+file.filename.split('.')[-1].lower()))

            print("============================Preprocesing============================")
            #melakukan preprocessing
            result1 = dev_preprocessing.preprocessing(id_predict, file.filename.split('.')[-1].lower())
            result2 = dev_preprocessing_multicolor.preprocessing(id_predict, file.filename.split('.')[-1].lower())
            print("============================Preprocesing Selesai============================")

            print("Mengecek hasil preprocessing")
            if(
                    (result1 == True)
                    and
                    (result2 == True)
            ):

                print("Memuat hasil preprocessing")
                img1 = cv2.imread(UPLOAD_FOLDER + "/" + id_predict + "/" + id_predict + "-binarize." + file.filename.split('.')[-1].lower())
                img2 = cv2.imread(UPLOAD_FOLDER + "/" + id_predict + "/" + id_predict + "-multicolor." + file.filename.split('.')[-1].lower())

                print("Menghapus gambar sebelum di preprocessing")
                os.remove(os.path.join(UPLOAD_FOLDER+"/"+id_predict, id_predict+"."+file.filename.split('.')[-1].lower()))

                print("Membandingkan hasil preprocessing binarize dan multicolor")
                result_compare = compare_result_preprocessing.compare_result(id_predict, file.filename.split('.')[-1].lower())

                b64_src = 'data:image/jpg;base64,'


                if (result_compare == "binarize"):
                    print("Gambar dipreprocessing dengan metode binarize")
                    imgFix = img1
                    encoded_img = encode_img(imgFix)
                    img_src = b64_src + encoded_img
                else:
                    print("Gambar dipreprocessing dengan metode multicolor")
                    imgFix = img2
                    encoded_img = encode_img(imgFix)
                    img_src = b64_src + encoded_img

                if not os.path.exists(UPLOAD_FOLDER + "/" + id_predict+"/predict"):
                    os.makedirs(UPLOAD_FOLDER + "/" + id_predict+"/predict")

                print("Menetapkan dan menyimpan gambar yang akan di prediksi dengan metode preprocessing yang telah dipilih")
                cv2.imwrite(os.path.join(UPLOAD_FOLDER+"/"+id_predict+"/predict", id_predict + "-fix." + file.filename.split('.')[-1].lower()), imgFix)

                print("Menghapus hasil preprocessing multicolor")
                os.remove(os.path.join(UPLOAD_FOLDER+"/"+id_predict, id_predict + "-multicolor." + file.filename.split('.')[-1].lower()))

                print("Menghapus hasil preprocessing binarize")
                os.remove(os.path.join(UPLOAD_FOLDER+"/"+id_predict, id_predict + "-binarize." + file.filename.split('.')[-1].lower()))

                print("Memprediksi dengan convolutional neural network menggunakan arsitektur")
                print("============================Mulai Prediksi============================")
                result = predict.predict("AlexNet", id_predict)
                print("Mendapatkan hasil prediksi")
                print("============================Prediksi Selesai============================")


                print("Menghapus gambar yang telah diprediksi")
                os.remove(os.path.join(UPLOAD_FOLDER+"/"+id_predict, id_predict + "-fix." + file.filename.split('.')[-1].lower()))

                print("Membersihkan file dan data yang tertinggal pada penyimpanan")
                #shutil.rmtree(UPLOAD_FOLDER+"/"+id_predict)

                result = list(map(adjusting_result.genapin, result[0]))
                result = list(map(str, result))
                result = adjusting_result.adjust(result)
                return {
                    "result":True,
                    "id_predict": id_predict,
                    "result_compare":result_compare,
                    "result_predict":result,
                    "image_after_preprocessing":img_src,
                    "message":"Predict success"}
            else:
                return {"result": False, "message": "Preprocessing image failed"}

        else:
            return {"result":False,"message":"Require file wrong"}


"""
class Predict(Resource):
    def post(self):


        if 'file' not in request.files:
            #flash('No file part')
            return {"result":False, "message":"No file part"}
        file = request.files['file']

        if 'id_openDevToolspredict' not in request.form:
            #flash('No file part')
            return {"result":False, "message":"Can not identify ID Predict"}
        id_predict = request.form['id_predict']
        # if user does not select file, browser also
        # submit an empty part without filename

        if file.filename == '':
            #flash('No selected file')
            return {"result":False, "message":"No selected file"}

        checkExtension = file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

    

        if file and checkExtension:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, id_predict+"-fix."+file.filename.split('.')[-1].lower()))
            os.remove(os.path.join(UPLOAD_FOLDER, id_predict+"-multicolor."+file.filename.split('.')[-1].lower()))
            os.remove(os.path.join(UPLOAD_FOLDER, id_predict + "-binarize." + file.filename.split('.')[-1].lower()))
            result = predict.predict("AlexNet", id_predict)
            os.remove(os.path.join(UPLOAD_FOLDER, id_predict+"-fix."+file.filename.split('.')[-1].lower()))
            return {"result":True,"message":"Predict success", "data":result}
        else:
            return {"result":False,"message":"Upload file failed"}
"""

class Oke(Resource):
    def post(self):
        zzz = [[12231, 12312, 123123, 12312, 12312]]
        gambar = cv2.imread("./data/Rumput Bambu_2.jpg",cv2.IMREAD_COLOR)

        b64_src = 'data:image/jpg;base64,'



        imgFix = gambar
        encoded_img = encode_img(imgFix)
        gambar = b64_src + encoded_img

        id_predict = "123"
        result_compare = "binarize"
        zzz = list(map(adjusting_result.genapin, zzz[0]))
        zzz = list(map(str, zzz))
        zzz = adjusting_result.adjust(zzz)

        return {
            "hasil": "True",
            "id_predict": id_predict,
            "result_compare": result_compare,
            "message": "Predict success",
            "shelalalashe":zzz,
            "gambar":gambar
        }


api.add_resource(Leaf, '/leafclassification/leaf')
api.add_resource(Leaf_by_code, '/leafclassification/leaf/<code_leaf>')
#api.add_resource(Preprocessing, '/leafclassification/preprocessing')
api.add_resource(Oke, '/leafclassification/oke')
api.add_resource(Predict, '/leafclassification/predict')

if __name__ == '__main__':
    app.run(debug=True)


