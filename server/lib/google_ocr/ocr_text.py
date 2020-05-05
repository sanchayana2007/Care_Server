import sys
#sys.path.append('Users/sahana/Desktop/ocr_for_actyv(4/03)')
import cv2
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, 'preprocessing')
import gray_scaling
import scaling
import noise_removal
import text_preprocessing
#from preprocessing import gray_scaling, scaling, noise_removal,text_preprocessing
sys.path.insert(0, 'adhar')
import get_adhar_front, get_adhar_back
#from adhar import get_adhar_front, get_adhar_back
#from ocr import ocr
import config as cfg
import gc_vision as gv


#CHECKING IF THE IMAGE IS ADHAR BACK OR NOT
def is_adhar_back(processed_img_text, raw_image_text):
    return get_adhar_back.check_adhar_back(processed_img_text, raw_image_text)


#CHECKING IF THE IMAGE IS ADHAR FRONT OR NOT
def is_adhar_front(processed_img_text, raw_image_text):
    return get_adhar_front.check_adhar_front(processed_img_text, raw_image_text)




#CHECKING THE TYPE OF DOC AND GETTING FIELDS
def steps(image_file):
    #Getting text from ocr (preprocessed image text & raw image text)
    #processed_img_text = ocr.image_preprocess_ocr(image_file)
    #raw_image_text = ocr.raw_ocr(image_file)
    raw_image_text = gv.extract_text(image_file)
    processed_img_text = raw_image_text
    #print(raw_image_text)


    adhar_back_text = get_adhar_back.get_details_adhar_back(raw_image_text)
    if('address' in adhar_back_text):
      return adhar_back_text

    adhar_front_text = get_adhar_front.get_details_adhar_front(processed_img_text, raw_image_text)
    return adhar_front_text

    #CHECKING AND GETTINGS FIELDS FROM ADHAR BACK
    if is_adhar_back(processed_img_text, raw_image_text):
        adhar_back_text = get_adhar_back.get_details_adhar_back(raw_image_text)
        return adhar_back_text


    #CHECKING AND GETTINGS FIELDS FROM ADHAR FRONT
    if is_adhar_front(processed_img_text, raw_image_text):
        adhar_front_text = get_adhar_front.get_details_adhar_front(processed_img_text, raw_image_text)
        return adhar_front_text


    return cfg.ERROR_MESSAGE



#if __name__ == "__main__":
#im = np.fromfile('/home/deb/Pictures/adhar_back.png', dtype=np.uint8)
#print(im.shape)
#file = cv2.imdecode(im, cv2.IMREAD_COLOR)
#extracted_text = steps(file)
#  extracted_text = steps('./adhar_front.png')
#  print(extracted_text)
