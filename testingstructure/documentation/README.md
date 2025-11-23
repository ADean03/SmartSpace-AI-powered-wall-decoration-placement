# SmartSpace-AI-powered-wall-decoration-placement

This is a project meant to predict the best place to hang paintings in an image to help with room decoration. It outputs
predicted bounding boxes for paintings over an image within specific confidence range. Worth noting confidence level
works best at very low decimal values currently and best changes on an image by image basis

# Running

To run the project, first navigate the the docker compose file in the deployment folder and edit the grafana paths based on where
the files are located on your system

Next, in a ternminal navigate to the deployment folder and run "docker-compose build" and "docker-compose up"
Recommend using very low confidence intervals when predicting, like 0.007 or 0.0007 and playing around to see what number gives most
accurate predictions

## Data
main data tested on not included due to size, included one image of apartment used for real world prediction testing

# Folder Structure

## testingstructure/

Folder I used to test running with the recomended structure. Keeping this folder made it a lot easier to move stuff around on
local machine before uploading to github, so I kept it in

## testingstructure/src/ 

contains requirements.txt and main project main.py. Models folder contains model used for inference

## testingstructure/src/utils

contains various files including:

gradioproject.ipynb: Basic jupyter notebook file to deploy gradio project
SmartSpaceModel.ipynb: Where dataset images were converted into masked files, and augmented further + class balancing
SmartSpaceModelTrain.ipynb: Contains last few attempts to train model, as well as final model training pipeline
wallseg.ipynb: Contains earliest failed versions of models, specifically attempts at making custom transformer model that 
used bounding boxes as inputs to make predictions

## testingstructure/deployment

Contains docker file and docker-compose yaml file. Note that docker-compose file must be changed to included absolute
path of grafana subfolders in order for grafana dashboard to be auto loaded. More information about this mention in video

## testingstructure/monitoring

Contains grafana and prometheus subfolders, along with the needed configuration files to save metrics in a dashboard

## testingstructure/ocumentation

Folder for project docs

## testingstructure/videos 

Folder for demo video

# Deployment strategy

Deployed in docker container, more information in running section along with commands to run project

## Monitoring and Metrics

Grafana and Prometheus used to monitor metrics. Metrics monitored are number predictions, prediction time
number of predictions rated good, number predictions rated bad.
To set up monitoring, update docker compose file for correct absolute paths for specified folders there
After that, grafana dashboard should automatically be loaded from json file. Metrics can take some
time to update.

## Version control

Done through github, and google collab. Files from collab were pushed to github for updates.
Copies of older versions of files exist on google collab and local machine