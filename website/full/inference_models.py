# https://github.com/onnx/models/tree/main/validated/vision/object_detection_segmentation/yolov3

import numpy as np
from PIL import Image
import onnxruntime

class yolo:
    def __init__(self, onnx_model_path = None):
        if onnx_model_path == None: onnx_model_path = 'models/yolov3-12.onnx'
        self.session = onnxruntime.InferenceSession(onnx_model_path)
        pass
    # this function is from yolo3.utils.letterbox_image
    def letterbox_image(self, image, size):
        '''resize image with unchanged aspect ratio using padding'''
        iw, ih = image.size
        w, h = size
        scale = min(w/iw, h/ih)
        nw = int(iw*scale)
        nh = int(ih*scale)

        image = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
        return new_image

    def preprocess(self, img):
        model_image_size = (416, 416)
        boxed_image = self.letterbox_image(img, tuple(reversed(model_image_size)))
        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.
        image_data = np.transpose(image_data, [2, 0, 1])
        image_data = np.expand_dims(image_data, 0)
        return image_data

    def postprocess(self, boxes, scores, indices):
        out_boxes, out_scores, out_classes = [], [], []
        for idx_ in indices:
            out_classes.append(idx_[1])
            out_scores.append(scores[tuple(idx_)])
            idx_1 = (idx_[0], idx_[2])
            out_boxes.append(boxes[idx_1])
        return out_boxes, out_scores, out_classes
        
            
# image = Image.open(img_path)
# # input
    def infer(self, img):
        image= Image.fromarray(img)
        image_data = self.preprocess(image)
        # image_size = np.array([image.size[1], image.size[0]], dtype=np.int32).reshape(1, 2)
        image_size = np.array([image.size[1], image.size[0]], dtype=np.float32).reshape(1, 2)

        boxes, scores, indices = self.session.run(None, {'input_1': image_data, 'image_shape': image_size})
        return self.postprocess(boxes, scores, indices)