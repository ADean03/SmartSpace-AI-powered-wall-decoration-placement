import os
from ultralytics import YOLO
import gradio as gr
from PIL import Image
from prometheus_client import start_http_server, Summary, Counter


# ---------------------------
# PROMETHEUS METRICS
# ---------------------------

output_counter = Counter('gradio_predictions_total', 'Total number of predictions')

feedback_counter = Counter(
    'gradio_feedback_total', 
    'Total number of feedback entries received', 
    ['Prediction_quality', 'Input_excerpt', 'Number_info', 'Location_info']
)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


# ---------------------------
# MODEL LOADING
# ---------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "models", "best (2).pt")

model = YOLO(model_path)

# Start Prometheus Metrics Server
start_http_server(8000)


# ---------------------------
# YOLO PROCESSING FUNCTION
# ---------------------------

@REQUEST_TIME.time()
def run_yolo(image, conf):
    try:
        conf = float(conf)
    except:
        conf = 0.5

    conf = max(0.0, min(1.0, conf))

    results = model.predict(
        source=image,
        classes=[11],
        imgsz=416,
        conf=conf
    )

    output_counter.inc()

    result_img = Image.fromarray(results[0].plot())
    return result_img


# ---------------------------
# FEEDBACK COLLECTION
# ---------------------------

def collect_feedback(Input_info, Prediction_quality, Number_info, Location_info):

    Input_excerpt = Input_info[:12] if Input_info else "No room info"

    feedback_counter.labels(
        Prediction_quality=Prediction_quality,
        Input_excerpt=Input_excerpt,
        Number_info=Number_info,
        Location_info=Location_info
    ).inc()

    print(f"Feedback: {Prediction_quality} | for room: {Input_excerpt}")
    return "Thank you for your feedback!"


# ---------------------------
# GRADIO INTERFACE
# ---------------------------

interface = gr.Interface(
    fn=run_yolo,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Number(label="Confidence (0.0 to 1.0)", value=0.0007)
    ],
    outputs=gr.Image(label="Detection Result"),
    title="SmartSpace Painting Detector/Placement Predictor",
    description="Upload an image and set the detection confidence threshold."
)

feedback_interface = gr.Interface(
    fn=collect_feedback,
    inputs=[
        gr.Textbox(label="Input Info", placeholder="Type of room predicted on"),
        gr.Radio(choices=["Good", "Bad"], label="Prediction Quality"),
        gr.Radio(
            choices=["None (Good)", "None (Bad)", "Too little", "Just right", "Too many"],
            label="Number of predicted locations"
        ),
        gr.Radio(choices=["Bad", "Mixed", "Good"], label="Quality of locations predicted")
    ],
    outputs="text",
    title="Feedback Collector",
    description="Provide feedback on the model's prediction."
)

gr.TabbedInterface([interface, feedback_interface], ["Predict", "Feedback"]).launch(
    server_name="0.0.0.0", 
    server_port=7860, 
    share=True
)
