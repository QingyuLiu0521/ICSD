## ICSD: An Open-source Dataset for Infant Cry and Snoring Detection
[![arXiv](https://img.shields.io/badge/arXiv-Paper-COLOR.svg)]() 
[![hf](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Dataset-yellow)](https://huggingface.co/datasets/QingyuLiu1/ICSD) 
[![demo](https://img.shields.io/badge/WebPage-Demo-red)]()

This is the official repository for the **ICSD** dataset. 

## About ⭐️
🎤 **ICSD** is a comprehensive audio event dataset for infant cry and snoring detection with the following features:
- containing over *3.3* hours of strongly labeled data and *1* hour of weakly labeled data;
- containing foreground events and background events for generating synthetic data

The figure below shows the organized structure of the ICSD dataset where audio files are stored in the audio folder and event time-stamp annotations in the metadata folder, each further categorized into train, validation, and test subfolders. Moreover, source materials for generating synthetic strongly labeled data are also provided. You can use *[Scaper](https://github.com/justinsalamon/scaper)* to generate your own synthetic data.

<div style="margin: 0 auto; width: 50%;">
  <img src="folder.png" alt="folder">
</div>
  
Detailed description for the dataset could be found in our [paper](https://arxiv.org/abs/2407.05361).

*To use the ICSD dataset, you can download the audio files and metada from our provided source URL list on [HuggingFace](https://huggingface.co/datasets/QingyuLiu1/ICSD).*

*Please note that ICSD doesn't own the copyright of the audios; the copyright remains with the original owners of the video or audio.*

<!-- This following README will introduce the usage guide of the corresponded code. -->

## Run the Baseline system 👨‍💻
...

## Acknowledgement 🔔
We acknowledge the wonderful work by these excellent developers!
- Audioset: [agkphysics/AudioSet](https://huggingface.co/datasets/agkphysics/AudioSet)
- Baby Chillanto Database
- Donate A Cry: [gveres/donateacry-corpus](https://github.com/gveres/donateacry-corpus)
- Female and Male Snoring: [orannahum/female-and-male-snoring](https://www.kaggle.com/datasets/orannahum/female-and-male-snoring)
- Snoring: [tareqkhanemu/snoring](https://www.kaggle.com/datasets/tareqkhanemu/snoring)
- ESC-50: [karolpiczak/ESC-50](https://github.com/karolpiczak/ESC-50)
- SINS: [KULeuvenADVISE/SINS_database](https://github.com/KULeuvenADVISE/SINS_database)
- MUSAN: [MUSAN-openslr.org](https://www.openslr.org/17/)
- Scaper: [justinsalamon/scaper](https://github.com/justinsalamon/scaper)


## Reference 📖
If you use the ICSD dataset, please cite the following papers:
```bibtex
@article{ICSD,
      title={ICSD: An Open-source Dataset for Infant Cry and Snoring Detection},
      author={Qingyu Liu, Longfei Song, Dongxing Xu, Yanhua Long},
      journal={arXiv},
      volume={}
      year={2024}
}
```
