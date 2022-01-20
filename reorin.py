#!/usr/bin/env python
# coding: utf-8

# %%
# Import modules. Test of TorchIO  version.
import copy
import enum
import os
from pathlib import Path
import warnings
import tempfile
import subprocess
import multiprocessing
from pathlib import Path
import torchio as tio
import numpy as np
import nibabel as nib


print('TorchIO version:', tio.__version__)



#the folder in which thus python file is must be home/zamorano
images_dir = Path('nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task105_MLD/imagesTr/')
labels_dir = Path('nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task105_MLD/labelsTr/')
image_paths_t1 = sorted(images_dir.glob('*_0000.nii'))
image_paths_t2 = sorted(images_dir.glob('*_0001.nii'))
label_paths = sorted(labels_dir.glob('*.nii'))
#destination folders
reori_img='imagesTr'
reori_labels='labelsTr'
#check equal number of files
assert len(image_paths_t1) == len(label_paths) 
assert len(image_paths_t1) == len(image_paths_t2)


print('t1: ', len(image_paths_t1),'label: ',len(label_paths),'t2: ',len(image_paths_t2))
#Define subject for the creation of dataset with torchio each subject will have t1 t2 and mask.
subjects = []
for (image_path_t1, image_path_t2, label_path) in zip(image_paths_t1, image_paths_t2,label_paths):
	l_id=str(label_path)
	t1_id=str(image_path_t1)
	t2_id=str(image_path_t2)

	subject = tio.Subject(

        mri_t1 = tio.ScalarImage(image_path_t1),
        mri_t2 = tio.ScalarImage(image_path_t2),
        label_roi = tio.LabelMap(label_path),
		label_id = (r'{}'.format(l_id)).split(r'/')[-1],
		imaget1_id = (r'{}'.format(t1_id)).split(r'/')[-1],
		imaget2_id = (r'{}'.format(t2_id)).split(r'/')[-1]

    )
	subjects.append(subject)
dataset = tio.SubjectsDataset(subjects)
print('Dataset size:', len(dataset), 'subjects')
#orientation 
to_ras = tio.ToCanonical()
#define tarjet shape
target_shape=512,512,128
crop_pad = tio.CropOrPad(target_shape, mask_name='label_roi')



print('begining')
cnt=0
for subject in dataset:
	print('working on: ',cnt)
	print("original")
	print(subject.mri_t1.orientation)
	print(subject.mri_t2.orientation)
	print(subject.label_roi.orientation)
	#croped_paded=crop_pad(subject)
	ori_ras=to_ras(subject)
	output_t1=reori_img + os.sep + subject.imaget1_id 
	output_t2=reori_img + os.sep + subject.imaget2_id 
	output_l=reori_labels + os.sep + subject.label_id 


	ori_ras.mri_t1.save(output_t1)
	ori_ras.mri_t2.save(output_t2)
	ori_ras.label_roi.save(output_l)
	print("final")
	print(ori_ras.mri_t1.orientation)
	print(ori_ras.mri_t2.orientation)
	print(ori_ras.label_roi.orientation)
	cnt+=1
	
print('finished')

