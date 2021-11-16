import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os
from numpy.lib.function_base import _delete_dispatcher
import time

#directory
dir_path='/home/zamorano/study2'
train_label_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task103_MLD/labelsTr'
train_image_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task103_MLD/imagesTr'

#filename to save modified masks with MLD part substracted to ensure each voxel correspond to unique value
file_mask_hwm="mask_hwm.nii.gz"
file_mask_hgm="mask_hgm.nii.gz"


def mask_combiner(dir_path):
    print('begining...')
    start_time = time.time()
    c_dl=0
    c_gm=0
    c_wm=0
    for subdir, dirs, files in os.walk(dir_path):
        
        for filename in files:
            masks=[]
            filepath = subdir + os.sep + filename   
            if filepath.endswith("dl_sg2.nii") :
                masks.append(filepath)
                c_dl+=1
            elif filepath.endswith("WM.nii"):
                masks.append(filepath)
                c_wm+=1
            elif filepath.endswith("GM.nii"):
                masks.append(filepath)
                c_gm+=1

    	    if len(masks)==3:
                #load
                load_mask_dl = nib.load(masks[0])
                load_mask_wm = nib.load(masks[1])
                load_mask_gm = nib.load(masks[2])
                #getting data as array 
                data_dl=load_mask_dl.get_fdata()
                data_wm=load_mask_wm.get_fdata()
                data_gm=load_mask_gm.get_fdata()
                #New mask array of WM and GM withouth dissease part from dl_mask
                data_hwm=np.subtract(data_wm,data_dl)
                data_hgm=np.subtract(data_gm,data_dl)
                data_hgm=data_hgm.clip(min=0)
                #headers
                dl_hdr=load_mask_dl.header  
                wm_hdr=load_mask_wm.header
                gm_hdr=load_mask_gm.header
                #make newmasks with only healthy part of white matter and grey matter
                mask_hwm= nib.Nifti1Image(data_hwm, load_mask_wm.affine, wm_hdr)
                mask_hgm= nib.Nifti1Image(data_hgm, load_mask_gm.affine, gm_hdr)
                mask_dl = load_mask_dl
                #save new mask
                nib.save(mask_hwm, os.path.join(subdir, file_mask_hwm))  
                nib.save(mask_hgm, os.path.join(subdir, file_mask_hgm)) 
                #getting data in numpy array using nib for the new combined mask
                data_dl=mask_dl.get_fdata()
                data_hwm=mask_hwm.get_fdata()
                data_hgm=mask_hgm.get_fdata()
                #new copy of healthy white matter =1
                fc=np.copy(data_hwm)
                fc[np.where(data_hgm)]=2   #helathy grey matter =2
                fc[np.where(data_dl)]=3    #disease labeled region =3
                finalmask= nib.Nifti1Image(fc, mask_dl.affine, dl_hdr)
                #save new mask
                new_name='MLD_'+str("{:03}".format(c_dl))+'.nii'
                nib.save(finalmask, os.path.join(subdir, new_name ))  
                print("saved")

        if c_dl == c_gm == c_wm:
            continue
		
        else:
            print("Missing file in: " + subdir)  	
            break

    print('ending...')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    mask_combiner(path)
