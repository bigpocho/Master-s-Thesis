import os
import shutil

path='/home/zamorano/study2'
train_label_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task102_MLD/labelsTr'
train_image_dir='/home/zamorano/nnUNet-container/data/nnUNet_raw/nnUNet_raw_data/Task102_MLD/imagesTr'

def nii_to_gz(path):
    print('begining...')
    c_dl=0
    c_t1=0
    c_t2=0
    for subdir, dirs, files in os.walk(path):
        # print(subdir, dirs ,files)

        for filename in files:
            filepath = subdir + os.sep + filename   
        
            if filepath.endswith("dl_sg2.nii.gz") :
                new_name='MLD_'+str("{:03}".format(c_dl))
                shutil.move(filepath, (train_label_dir+ os.sep +new_name+'.nii.gz'))
                c_dl+=1

            elif filepath.endswith("t1_3d.nii.gz"):
                new_name='MLD_'+str("{:03}".format(c_t1))+'_0000'
# Modality 1 and 2 = xxx_0000 and xxx_0001
                shutil.move(filepath, (train_image_dir+ os.sep +new_name+'.nii.gz'))
                c_t1+=1

            elif filepath.endswith('t2ax.nii.gz'):
                new_name='MLD_'+str("{:03}".format(c_t2))+'_0001'
                shutil.move(filepath, (train_image_dir+ os.sep +new_name+'.nii.gz'))
                c_t2+=1 
#Check that no file is missing
        if c_dl == c_t1 and c_dl == c_t2 and c_t1 == c_t2:
            continue

			
        else:
            print("Missing file in: " + subdir)  	
            break
    print('ending...')




if __name__ == '__main__':
    nii_to_gz(path)
