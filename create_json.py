from collections import OrderedDict
import json
import os

train_label_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task102_MLD/labelsTr'
train_image_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task102_MLD/imagesTr'
task_folder_name='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task102_MLD/'
test_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task102_MLD/imagesTs'
overwrite_json_file = True #make it True if you want to overwrite the dataset.json file in Task_folder
json_file_exist = False

if os.path.exists(os.path.join(task_folder_name,'dataset.json')):
    print('dataset.json already exist!')
    json_file_exist = True

if json_file_exist==False or overwrite_json_file:

    json_dict = OrderedDict()
    json_dict['name'] = "MLD"
    json_dict['description'] = "Metachromatic leukodystrophy MRI dataset study2"
    json_dict['tensorImageSize'] = "3D"
    json_dict['reference'] = "see challenge website"
    json_dict['licence'] = "see challenge website"
    json_dict['release'] = "0.0"

    #you may mention more than one modality
    json_dict['modality'] = {
        "0": "MRI t1", 
        "1": "MRI t2"
    }
    #labels+1 should be mentioned for all the labels in the dataset
    json_dict['labels'] = {
        "0": "background",
        "1": "white matter",
        "2": "grey matter",
        "3": "MLD label"
    }
    
    train_ids = os.listdir(train_label_dir)
    test_ids = os.listdir(test_dir)
    json_dict['numTraining'] = len(train_ids)
    json_dict['numTest'] = len(test_ids)

    #no modality in train image and labels in dataset.json 
    json_dict['training'] = [{'image': "./imagesTr/%s" % i, "label": "./labelsTr/%s" % i} for i in train_ids]

    #removing the modality from test image name to be saved in dataset.json
    json_dict['test'] = ["./imagesTs/%s" % (i[:i.find("_0000")]+'.nii.gz') for i in test_ids]

    with open(os.path.join(task_folder_name,"dataset.json"), 'w') as f:
        json.dump(json_dict, f, indent=4, sort_keys=True)

    if os.path.exists(os.path.join(task_folder_name,'dataset.json')):
        if json_file_exist==False:
            print('dataset.json created!')
        else: 
            print('dataset.json overwritten!')
