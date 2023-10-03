from pycocotools.coco import COCO
import os
import shutil
import numpy as np
import tqdm # can be remvoe
from PIL import Image
import requests

def annotation2text(image_info, dst_path, dataset):

    buffer = ''
    boxes = np.zeros((0, 5))

    file_name = image_info['file_name'].replace('/', '_').split('.')[0] + '.txt'
    save_path = f"{dst_path}/{file_name}"

    width, height = image_info['width'], image_info['height']

    annotation_ids = dataset.getAnnIds(image_info['id'])
    annotations = dataset.loadAnns(annotation_ids) if len(annotation_ids) != 0 else []

    for annotation in annotations:
        box = annotation['bbox']

        if box[2] < 1 or box[3] < 1:
            continue

        box[0] = ((box[0] + box[2] / 2) / width)
        box[1] = ((box[1] + box[3] / 2) / height)
        box[2] = (box[2] / width)
        box[3] = (box[3] / height)

        label = (annotation["category_id"] - 1)
        buffer = buffer + str(label)
        for i in box:
            buffer += ' ' + str(i)

        buffer += '\n'
    
    with open(save_path, 'w') as fp:
        fp.writelines(buffer)

    return 

def json2texts(annotation_file, dst):
    '''
    annotation_file: the annotation file
    src: Path to source images
    dst: Path to place the data
    '''
    
    # if the dst folder exists, delete it
    if os.path.isdir(dst):
        shutil.rmtree(dst)

    # create the dst dir
    os.makedirs(dst)

    labels_save_path = f'{dst}/labels/'
    images_save_path = f'{dst}/images/'

    # create Images & Lables folder in dst folder
    os.mkdir(labels_save_path)
    os.mkdir(images_save_path)

    dataset = COCO(annotation_file=annotation_file)
    image_ids = dataset.getImgIds()

    for image_id in tqdm.tqdm(image_ids, desc='change .json file to .txt file'):

        image_info = dataset.loadImgs(image_id)[0]
        try:
            file_name = image_info['file_name'].replace('/', '_') #f"{image_info['id']}.{image_info['flickr_640_url'].split('.')[-1]}"
            save_path = f"{images_save_path}/{file_name}"
            
            raw_image = Image.open(requests.get(image_info['flickr_url'], stream=True).raw)
            with open(save_path, 'wb') as file:
                raw_image.save(file)

            annotation2text(image_info, labels_save_path, dataset)

        except Exception as e:
            continue

    return dst