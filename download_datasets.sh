#!/bin/bash

root_dir=$PWD

cd data
mkdir MiddleBury_2021
cd MiddleBury_2021
wget https://vision.middlebury.edu/stereo/data/scenes2021/zip/all.zip
unzip all.zip && rm all.zip
mv data/* . && rm -rf data