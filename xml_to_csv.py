import os
import random
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np

def train_test_split(path):
    xml_list = []
    all_xml_file = []
    for xml_file in glob.glob(path + '/*.xml'):
        all_xml_file.append(xml_file)

    total_length = len(all_xml_file)
    random.shuffle(all_xml_file)
    training_xml_len = int(np.round(total_length * 0.7))
    training_xmls = all_xml_file[:training_xml_len]
    testing_xmls = all_xml_file[training_xml_len:]
    print(len(training_xmls), len(testing_xmls))
    xml_df = xml_to_csv(training_xmls, '/train_images')
    xml_df.to_csv(('train.csv'), index=None)

    xml_df = xml_to_csv(testing_xmls, '/test_images')
    xml_df.to_csv(('test.csv'), index=None)

def xml_to_csv(path, image_path_t):

    # for xml_file in glob.glob(path + '/*.xml'):
    xml_list = []
    for xml_file in path:
        dirname = os.path.dirname(xml_file)
        filename = os.path.basename(xml_file).split('.')[0] + '.jpeg'

        source_filename = dirname + '/' + filename
        destination_filename = dirname + image_path_t + '/' + filename
        os.replace(source_filename, destination_filename)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):

            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height',
                   'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def remove_unnessary_files(path):

    image_files = glob.glob(path + '/*.jpeg')
    all_xml_files = glob.glob(path + '/*.xml')
    print(len(image_files))
    print(len(all_xml_files))
    for img_file in image_files:
        xml_file = img_file.split('.')[0] + '.xml'
        if os.path.isfile(xml_file):
            pass
        else:
            print("File remove")
            os.remove(img_file)

    # all_wanted_images = []
    # for xml_file in glob.glob(path + '/*.xml'):
    #     jpeg_file = xml_file.split('.')[0] + '.jpeg'
    #     if jpeg_file in image_files:
    #     else:
    #         import pdb; pdb.set_trace()

     

def main():
    image_path = os.path.join(os.getcwd(), ('BloodRBC/'))
    remove_unnessary_files(image_path)
    # print(image_path)
    image_path = os.path.join(os.getcwd(), ('BloodRBC/'))
    train_test_split(image_path)
    # xml_df = xml_to_csv(image_path)
    # xml_df.to_csv(('images_labels.csv'), index=None)
    # print('Successfully converted xml to csv.')


main()
