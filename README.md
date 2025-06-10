# Daunesia API

An API for leaf classification based on images using deep learning and image processing. This project uses Flask as the backend and provides endpoints to predict leaf species from uploaded images.

## Features

- Upload leaf images and automatically predict their species.
- Image preprocessing with two methods: binarize and multicolor.
- Deep learning models (CNN) with several architectures (AlexNet, LeNet5, ResNet50, etc).
- Prediction results include species information from a JSON database.

## Configuration

- Deep learning models and supporting files are placed in the `data/neural_network/` folder.
- Leaf species file is located at `data/spesies.json`.
- Uploaded images are temporarily stored in `data/temporary/predict_image/`.

## Usage

- Main endpoint: `/predict` (POST)
- Send the leaf image file with the `file` field via form-data.
- The response will contain the predicted species, preprocessed image, and species information.

## Deployment

- Ready for deployment on platforms like Heroku (see `Procfile` and `runtime.txt`).

## Main Dependencies

- Flask
- Flask-RESTful
- OpenCV (opencv-python)
- Keras
- Numpy
- TinyDB
- Werkzeug

## Model Training Repository

Code and documentation for model training can be found at [https://gitlab.com/hafiizhekom-belajar/daunesia-cnn](https://gitlab.com/hafiizhekom-belajar/daunesia-cnn).