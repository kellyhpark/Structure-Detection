# Structure Detection: Identifying Electrical Structure through Fine-tuning DETR

By training the DETR (End-to-End Object Detection with Transformers) objected detection model with a custom dataset collected from Google Street View, we aim to fine-tune to model to detect overhead (OH) and underground (UG) electrical structures when given an image. In doing so, the project's goal is to lay the foundation for mitigating wildfire risks through public image data available to us.

## Data Sources
Data for this project is collected from [Google Street View Static API](https://developers.google.com/maps/documentation/streetview/overview). 

In order to collect all images, please navigate to the [streetwatch repository](https://github.com/pdashk/streetwatch), and follow instruction there to download image data.

## Setup

### Conda Environment
After cloning repo, navigating to root level and run:
```
conda env create -f environment.yml
```

### Before Fine-tuning DETR
As fine-tuning cannot be run without a GPU, the finetune_detr.ipynb notebook **must** be run on Google Colab or a PC with a GPU. Running the notebook on Google Colab may be done by downloading the finetuning notebook and uploading. If running the notebook on a PC with a GPU, additional steps listed within the notebook.

When prompted to do so within the notebook, please upload the image training and validation data to their respective directories. Training images are denoted by all image names that do not begin with 'kevin_'. Validation images are characterized by images beginning with 'kevin_'. Additionally locate the custom_train.json and custom_val.json files in the 'annotation' directory and upload/move accordingly as instructued in the notebook.

# Project Structure

```
├── annotation/         <- Contains custom_train.json and custom_val.json to be used as annotation JSONS
│
├── finetune_detr.ipynb <- Jupyter notebook for fine-tuning (run in Google Colab)
|
├── .env                <- Environment variables for the project
│
├── .gitignore          <- Git ignore file
│
├── environment.yml     <- Conda environment file
│
└── README.md           <- The top-level README for repo
```
