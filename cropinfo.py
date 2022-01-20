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
labels_dir = Path('nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task105_MLD/labelsTr')
image_paths_t1 = sorted(images_dir.glob('*_0000.nii'))
image_paths_t2 = sorted(images_dir.glob('*_0001.nii.gz'))
label_paths = sorted(labels_dir.glob('*.nii'))
reori_img='imagesTr'
reori_labels='labelsTr'
assert len(image_paths_t1) == len(label_paths) 
assert len(image_paths_t1) == len(image_paths_t2)
print('t1: ', len(image_paths_t1),'label: ',len(label_paths),'t2: ',len(image_paths_t2))

subjects = []
target_shape=128,512,512


for (image_path_t1,label_path) in zip(image_paths_t1, label_paths):
	l_id=str(label_path)
	t1_id=str(image_path_t1)
	#t2_id=str(image_path_t2)

	subject = tio.Subject(

        mri_t1 = tio.ScalarImage(image_path_t1),
        #mri_t2 = tio.ScalarImage(image_path_t2),
        label_roi = tio.LabelMap(label_path),

		label_id = (r'{}'.format(l_id)).split(r'/')[-1],
		imaget1_id = (r'{}'.format(t1_id)).split(r'/')[-1],
		#imaget2_id = (r'{}'.format(t2_id)).split(r'/')[-1]

    )
	subjects.append(subject)
dataset = tio.SubjectsDataset(subjects)
print('Dataset size:', len(dataset), 'subjects')





print('beginingt1')
cnt=0

crop_pad = tio.CropOrPad(target_shape, mask_name='label_roi')
for subject in dataset.dry_iter():
	print('working on: ',cnt)
	print(subject.imaget1_id, subject.mri_t1.spatial_shape ,subject.mri_t1.orientation)
#apply crop/pad to each images from each subject independenly
	croped_paded=crop_pad(subject)
	#croped_paded1=crop_pad(subject.mri_t1)
	#croped_paded2=crop_pad(subject.mri_t2)
	#set output 
	output_t1=reori_img + os.sep + subject.imaget1_id 
	#output_t2=reori_img + os.sep + subject.imaget2_id 
	output_l=reori_labels + os.sep + subject.label_id 
#print to check changes
#	print(subject.imaget1_id, subject.mri_t1.spatial_shape ,subject.mri_t1.orientation)
#	print(subject.imaget2_id, subject.mri_t2.spatial_shape ,subject.mri_t2.orientation)
#	print(subject.label_id, subject.label_roi.spatial_shape ,subject.label_roi.orientation)
#save results
	croped_paded.mri_t1.save(output_t1)
	croped_paded.label_roi.save(output_l)
	#croped_paded.save(output_l)
	print(croped_paded.imaget1_id, croped_paded.mri_t1.spatial_shape ,croped_paded.mri_t1.orientation)
#	print(subject.imaget1_id, croped_paded1.spatial_shape ,subject.mri_t1.orientation)	
#	print(subject.imaget2_id, croped_paded2.spatial_shape ,subject.mri_t2.orientation)
#	print(subject.label_id, croped_paded.spatial_shape ,subject.label_roi.orientation)
	cnt+=1
	

subjects = []
target_shape=128,512,512
for (image_path_t2,label_path) in zip(image_paths_t2, label_paths):
	l_id=str(label_path)
	#t1_id=str(image_path_t1)
	t2_id=str(image_path_t2)

	subject = tio.Subject(

        #mri_t1 = tio.ScalarImage(image_path_t1),
        mri_t2 = tio.ScalarImage(image_path_t2),
        label_roi = tio.LabelMap(label_path),

		label_id = (r'{}'.format(l_id)).split(r'/')[-1],
		#imaget1_id = (r'{}'.format(t1_id)).split(r'/')[-1],
		imaget2_id = (r'{}'.format(t2_id)).split(r'/')[-1]

    )
	subjects.append(subject)
dataset = tio.SubjectsDataset(subjects)
print('Dataset size:', len(dataset), 'subjects')

print('begining t2')
cnt=0

crop_pad = tio.CropOrPad(target_shape, mask_name='label_roi')
for subject in dataset.dry_iter():
	print('working on: ',cnt)
	print(subject.imaget2_id, subject.mri_t2.spatial_shape ,subject.mri_t2.orientation)
#apply crop/pad to each images from each subject independenly
	croped_paded=crop_pad(subject)

	#set output 

	output_t2=reori_img + os.sep + subject.imaget2_id 
	output_l=reori_labels + os.sep + subject.label_id 
#print to check changes

#save results
	croped_paded.mri_t2.save(output_t2)
	#croped_paded.label_roi.save(output_l)
	#croped_paded.save(output_l)

#	print(subject.imaget1_id, croped_paded1.spatial_shape ,subject.mri_t1.orientation)	
#	print(subject.imaget2_id, croped_paded2.spatial_shape ,subject.mri_t2.orientation)
#	print(subject.label_id, croped_paded.spatial_shape ,subject.label_roi.orientation)
	cnt+=1

print('finished')



