# RES - mol - Development of a statistics-based IDS for automotive security

This GitHub repository provides some example code for the RES course. The MOL (mini research lab) is the **Development of a statistics-based IDS for automotive security**


## Local install 

* set up a virtual environment
> python3 -m venv venv
* activate virtual environment
> source venv/bin/activate
* install matplotlib in virutal environment
> pip3 install matplotlib
* install pandas in virtual environment
> pip3 install pandas

## Content of the repo

This repository is organised as follows:
  * **/hcrl**: folder that contains the dataset. These files should be downloaded from [this link](https://drive.google.com/drive/folders/1ed2PlvcSu9ONt-8KK3sgG4Qw1Bp0ccOr?usp=sharing)
  * **/images**: placeholder-folder that contains the generated images. However, this folder should stay empty in the repo.
  * a **.gitignore** file to ignore *virtual environments*
  * this **README.md** file
  * the **slides**.pdf as shown in the lab
  * four example files for parsing (w.o. pandas)
    * **hcrl_normal_analyse.py**: analysis of the normal dataset
    * **hcrl_dos_analyse.py**: analysis of the DoS dataset
    * **hcrl_dos_detect_hd.py**: classification of frames of the DoS dataset based on Hamming distance
    * **hcrl_dos_detect_hd.py**: classification of frames of the DoS dataset based on (70%) chance
