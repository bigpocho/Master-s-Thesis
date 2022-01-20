#!/bin/bash
#loads the fsl program 
#export FSLDIR=/usr/local/packages/fsl 
#.  ${FSLDIR}/etc/fslconf/fsl.sh 

SOURCEDIR=/home/zamorano/img2/
DESTDIR=/home/zamorano/coregister/

for file in MLD_*_0000.nii ; do
    echo "currently working in $file"
    flirt -ref $file -in ${file/_0000.nii/_0001.nii} -out ${DESTDIR}${file/_0000.nii/_0001.nii} -dof 6
    cp $file    $DESTDIR
done


