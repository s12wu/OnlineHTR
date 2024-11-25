# Handwriting input panel

https://github.com/user-attachments/assets/7994263e-e8bd-441d-aef8-2c4c7feedb03

Enter text on your Linux desktop using handwriting recognition.
This is based on PellelNitram's handwriting recognition implementation - all credits should go to them. (see below)

All I did was modify the UI to be a floating window and type out the detected text.


This is built for, but probably not limited to, the Pine64 PineNote running the Debian trixie GNOME image.
It **works on wayland** by using ydotool and its root daemon to enter the text.

To work with a German QWERTZ layout, this program simply swaps "Y" with "Z" and vice-versa. Other special characters are of course still messed up. Disable this by setting `QWERTZ=False` in `src/draw_and_type.py`.

This is still a very early quick and dirty test.

## usage
 - Write into the drawing area. Click "Predict" to recognize the text and type it out.
 - "Reset strokes" to clear the drawing area.
 - click and drag the "drag" button to move the window. This is necessary since it has no title bar
 - click "exit" to quit the program
 - "Return", "Space" and "Backspace" to type these keys

## future features
 - minimize / hide the window
 - Maybe add a function edit the text before typing to correct misspellings?
 - Run a spell checker?
 - ...



## installation
The original project recommended the use of conda, but I had success just using the system Python 3.12 (trixie repos November 2024) and a venv.

### build + install ydotool
```bash
sudo apt install cmake scdoc
git clone https://github.com/ReimuNotMoe/ydotool
cd ydotool
mkdir build
cd build
cmake .. -DSYSTEMD_SYSTEM_SERVICE=ON -DSYSTEMD_USER_SERVICE=OFF
sudo make install
sudo mv /usr/local/lib/systemd/user/ydotoold.service /lib/systemd/system/

# edit the service file.
sudo nano /lib/systemd/system/ydotoold.service
# change
ExecStart=/usr/local/bin/ydotoold
# to
ExecStart=/usr/local/bin/ydotoold -p /tmp/.ydotool_socket -P 666
# this specifies the socked ydotool can use to communicate. -P 666 sets the necessary permissions

sudo systemctl start ydotoold.service # enable as well if you want it to run it on system startup

# verify ydotool is working
YDOTOOL_SOCKET=/tmp/.ydotool_socket ydotool type "hello world" 
 > hello world
```

### setup the handwriting input panel

Clone this repo and cd to it

```bash
sudo apt install python3-pip python3-venv python3-tk
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

> Download the model weights [here](https://lellep.xyz/blog/online-htr.html?utm_campaign=githubWeights#the-model-weights) and place it in `models/dataIAMOnDB_featuresLinInterpol20DxDyDtN_decoderGreedy/` after unpacking it.

### run
cd to the repo folder
```bash
source venv/bin/activate # if not done yet
python src/draw_and_type.py
```

---

# original README

<div align="center">

# Online Handwritten Text Recognition with PyTorch

[![python](https://img.shields.io/badge/-Python_3.10-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pytorch](https://img.shields.io/badge/PyTorch_2.0+-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/get-started/locally/)
[![lightning](https://img.shields.io/badge/-Lightning_2.0+-792ee5?logo=pytorchlightning&logoColor=white)](https://pytorchlightning.ai/)
[![hydra](https://img.shields.io/badge/Config-Hydra_1.3-89b8cd)](https://hydra.cc/) <br>
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ashleve/lightning-hydra-template/pulls)
<a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a>
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](#license) <br>
[![Paper](http://img.shields.io/badge/paper-Carbune_et_al._(2020)-B31B1B.svg)](https://doi.org/10.1007/s10032-020-00350-4)

A clean PyTorch implementation of ["Fast multi-language LSTM-based online handwriting recognition"](https://doi.org/10.1007/s10032-020-00350-4) by Carbune *et al.* (2020) 🚀⚡🔥.<br>

_Contributions are always welcome!_

</div>

<br>

## 📌 Introduction

In this repository I provide a clean [PyTorch](https://pytorch.org/) model implementation of the paper "Fast multi-language [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory)-based online handwriting recognition" by Carbune *et al.* (2020) from Google; see [this paper](http://doi.org/10.1007/s10032-020-00350-4).

This model lets you predict handwritten text as shown in the project demo below.

The present work is part of my attempt to build a handwriting recognition system for [Xournal++](https://github.com/xournalpp/xournalpp), a fabulous open-source handwriting notetaking software. Most of this aforementioned attempt is captured in the [Xournal++ HTR](https://github.com/PellelNitram/xournalpp_htr) repository where I publish working solutions based on models like the one implemented in this repository.

## 📺 Project Demo

<div align="center">

<a href="https://youtu.be/H62bjwNkMvc?utm_source=github&utm_medium=readme&utm_campaign=github_readme">
    <img src="docs/static/demo.gif" width="700">
</a>

*([Click on GIF or here to get to video](https://youtu.be/H62bjwNkMvc?utm_source=github&utm_medium=readme&utm_campaign=github_readme).)*

</div>

## 🚀 Quickstart

The following explanation sets you up to use the scripts `src/draw_and_predict_sample.py` and `src/draw_and_store_sample.py` to predict your own handwritten text as shown in the 📺 project demo and to store the written sample, respectively:

1. Install the project according to [the installation section](#installation) in this README and activate the corresponding environment.
2. Download the model weights [here](https://lellep.xyz/blog/online-htr.html?utm_campaign=githubWeights#the-model-weights) and place it in `models/dataIAMOnDB_featuresLinInterpol20DxDyDtN_decoderGreedy/` after unpacking it.
3. Invoke the following command from the root of this repository: `python src/draw_and_predict_sample.py`.

If you want to store your own handwriting sample in a CSV file, then execute `python src/draw_and_store_sample.py`.

## 🏋️ Training from scratch

1. Follow installation procedure provided in [Installation](#installation).
2. Set up the training data as described [in the training data](#training-data) section.
3. Start training with `bash scripts/train_dataIAMOnDB_featuresLinInterpol20DxDyDtN_decoderGreedy.sh` from repository root directory after you activated the conda environment that you use.

## Installation

This repository uses a conda environment in which packages are installed using pip.

Follow these steps from the root of the repository to install this package:

1. `conda create --prefix <path> python=3.10.11`
2. `conda activate <path>`
3. `pip3 install torch torchvision torchaudio`
4. `pip install -r requirements.txt`
5. `pip install -e .` (do not forget the dot, `.`)
6. `make test-installation` to confirm that installation was successful. Alternatively, you can run `make test-full` to run all tests including the slow ones.

## Training data

[IAM On-Line Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database) is used as training and validation data. Register on their website to download the dataset for free. Afterwards, place the following folders and files from their dataset in this repository's subfolder `data/datasets/IAM-OnDB`:

1. Download the following files that are listed on the above stated dataset website: `data/original-xml-part.tar.gz`, `data/writers.xml`, `data/lineStrokes-all.tar.gz`, `data/lineImages-all.tar.gz`, `data/original-xml-all.tar.gz`, `data/forms.txt` & `ascii-all.tar.gz`.
2. Extract the content of each of those files into the `data/datasets/IAM-OnDB/<file_base_name>` folder where `<file_base_name>` denote the basenames of each of the downloaded files.
3. This is how it should look like:

```
├── data/datasets/IAM-OnDB
│   ├── ascii-all/
│   ├── forms.txt
│   ├── lineImages-all
│   ├── lineStrokes-all
│   ├── original-xml-all
│   ├── original-xml-part
│   └── writers.xml
```

4. Confirm with `make test-training-data` that you placed the training data correctly.

## Available models & their model cards

- [x] `dataIAMOnDB_featuresLinInterpol20DxDyDtN_decoderGreedy`
  - How it was trained: Using the IAM-OnDB dataset, this model is obtained by training on raw stroke data with channels (dx, dy, dt, n) where (dx, dy) are coordinate differences, dt is time difference and n is 1 if a point is the start of a new stroke with 0 otherwise. Prior to computing the differences and n, the raw stroke data is linearly interpolated to feature 20 points per unit length.
  - Download the model weights [here](http://lellep.xyz/blog/online-htr.html#download_weights).
  - Train this model yourself executing `bash scripts/train_dataIAMOnDB_featuresLinInterpol20DxDyDtN_decoderGreedy.sh` after you activated the conda environment that you use.

## ⌛ Open tasks

*All contributions are welcome! :-)*

- [x] Allow inference on own handwriting.
- [ ] Implement CTC beam decoding with language model.
- [ ] Implement Bezier curve fitting algorithm as data preprocessor.
- [ ] Publish trained models on [🤗 Hugging Face](https://huggingface.co/) for easy access.

## 👩‍💻 Contributing

I would love you to contribute! Let's make it a great project that people can benefit from :-).

## 🙏🏼 Acknowledgments

Thanks [Leonard Salewski](https://twitter.com/l_salewski) and [Jonathan Prexl](https://scholar.google.de/citations?user=pqep1wkAAAAJ&hl=de) for super useful discussions on training PyTorch models! Thanks [Harald Scheidl](https://githubharald.github.io/) for providing both great content and code around handwritten text recognition.

I thank the department where I do my PhD, the [School of Physics and Astronomy](https://www.ph.ed.ac.uk/) of [The University of Edinburgh](https://www.ed.ac.uk/), for providing computational resources to train the models.

The scaffold of this code is based on [the awesome lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template) by [ashleve](https://github.com/ashleve) - thank you for providing this!

## License

This repository is licensed under the [MIT License](LICENSE.md).
