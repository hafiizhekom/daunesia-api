"""from os import walk
path = "../data/temporary/predict_image"
mypath = path
destinationpath = path
id_predict = "2019-04-15 22:07:47.822360"
filenames_plant = []
for (dirpath, dirnames, filenames) in walk(mypath):
    filenames_plant = filenames
    print(dirpath.split("/")[-1])
    if(dirpath.split("/")[-1]==id_predict):
        print("ok")
        """
import json


def genapin(n):
    return round(n*100,4)

def adjust(results):
    hasil = {}
    with open('./data/spesies.json') as json_file:
        data = json.load(json_file)


        for index, result in enumerate(results):
            tempdata = {}
            tempdata['hasil_predict']=results[index]
            index = str(index+1)
            tempdata['kode'] = data['spesies'][index]['kode']
            tempdata['genus'] = data['spesies'][index]['genus']
            tempdata['nama_indonesia'] = data['spesies'][index]['nama_indonesia']
            tempdata['nama_english'] = data['spesies'][index]['nama_english']
            tempdata['description'] = data['spesies'][index]['description']

            hasil[index] = tempdata

    return hasil





