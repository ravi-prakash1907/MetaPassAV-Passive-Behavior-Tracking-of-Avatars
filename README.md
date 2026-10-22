# **MetaPassAV:** Passive Behavior Tracking of Avatars

<!------------------------------------------------------------------------------>

<p align="center">
  <img src="./assets/metapassav_logo.png" alt="MetaPassAV Logo" width="850">
</p>

<p align="center">
  An anonymized behavioral authentication dataset based on **passive avatar** kinematics
  in a **metaverse** environment.
</p>

<!------------------------------------------------------------------------------>



## Overview

This repository provides an anonymized behavioral authentication dataset collected in a custom virtual art gallery using Meta Quest 2. This timeseries data was collected by tracking the passive behavioral kinematics of avatars (AVs) in custom immersive metaverse environment. The participants were seated and allowed to freely explore the virtual gallery without any assigned task. The dataset is intended for research in behavioral authentication, user identification, and related fields.  

### Dataset Summary

| Property | Value |
|---|---:|
| Participants | 16 |
| Sessions | 123 |
| Total Duration | 4 h 53 min |
| Average Session Length | 2 min 23 sec |
| Sampling Rate | 0.25 Hz |
| Raw Features | 14 |
| Engineered Features | 28 |
| Sliding Windows | 16,291 |
| Window Length | 44 s |
| Window Stride | 2 s |

## Collection

- Custom Unity virtual art gallery
- Meta Quest 2 headset
- Seated interaction
- Passive exploration (no assigned task)
- Navigation via controllers
- Natural head movement recorded
- One sample every 4 seconds plus image-view events

## Repository

```
.
├── README.md
├── MetaPassAV-v1.pdf
├── DataPrep/
|   ├── 1 Data Preparation.ipynb
|   ├── 2 EDA and Split.ipynb
|   ├── data/
|   └── scripts/
└── UnifiedAVDTAuth/
    ├── README.md
    └── unifiedAuthFramework/
        ├── 01_KAN_AE.ipynb
        ├── 02_BiGRU_Classifier.ipynb
        └── 03_UBM_Template_Auth.ipynb
```

## Steps to Reproduce

> 1. Clone the repository
> 2. Navigate to the `DataPrep` folder
> 3. Run the notebooks in order:
>    - `1 Data Preparation.ipynb`
>    - `2 EDA and Split.ipynb`
> 4. The exported data will be available in the `DataPrep/data/raw_split` folder.

The final dataset is available in the `DataPrep/data/raw_split` folder as a CSV file. The dataset contains 14 raw features and 28 engineered features, with a total of 16,291 sliding windows of 44 seconds each, sampled every 2 seconds. It also consits of 2 identifiers (`UserID` and `SampleID`) for each sliding window, make complete column count as 30.  

> _The final dataset can be used for developoing the proposed template-based deep-UBM inspired behavioral authentication model, as described in the paper ([DOI](https://doi.org/10.1016/j.asoc.2026.116714)). The core code and implementation of the model is available in the [`UnifiedAVDTAuth`](./UnifiedAVDTAuth/) directory._  

## Citation

While using this dataset or the proposed model, please cite the following accompanying publication titled _"A Unified Framework for Behavior-Based Identification and Authentication of Avatars and Digital Twins"_:

```tex
@article{PRAKASH2026116714,
 title={A unified framework for behavior-based identification and authentication of avatars and digital twins},
 journal={Applied Soft Computing},
 pages={116714},
 year={2026},
 issn={1568-4946},
 doi={https://doi.org/10.1016/j.asoc.2026.116714},
 url={https://www.sciencedirect.com/science/article/pii/S1568494626021629},
 author={Ravi Prakash and Tony Thomas},
}
```

## License

This dataset is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** License.

You are free to share and adapt the dataset for any purpose, provided appropriate attribution is given.

See the [LICENSE](LICENSE) file for complete details.
