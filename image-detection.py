import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter

def load_labels(path):
    with open(path, 'r') as f:
        return{i: line.strip() for i, line in enumerate(f.readlines())}

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))
  scale, zero_point = output_details['quantization']
  output = scale * (output - zero_point)
  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]]


labels = load_labels("labels.txt")
interpreter = Interpreter("model.tflite")
interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']

image = Image.open("Pictures/image01.jpg").convert('RGB').resize((width, height), Image.ANTIALIAS)
results = classify_image(interpreter, image)
label_id, prob = results[0]
print(labels[label_id])
print(prob)
