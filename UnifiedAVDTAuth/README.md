# A Unified Framework for Behavior-Based Identification and Authentication of Avatars and Digital Twins

This framework provides a unified approach for identifying and authenticating avatars and digital twins based on their behavioral patterns. 

## Setup Instructions

To setup and test the proposed framework, run the files in the following order:

1. **Update paths in all three files.** Replace the placeholder paths with paths on your machine:
	- `01_KAN_AE.ipynb`: set `BASE_PATH`, `MODEL_DATA_PATH`, `MODEL_PATH`, and `ENC_DATA_PATH`.
	- `02_BiGRU_Classifier.ipynb`: set `BASE_PATH`, `MODEL_DATA_PATH`, and `MODEL_PATH`.
	- `03_UBM_Template_Auth.py`: set `DIR_PREFIX`, `MODEL_DIR`, `SAMPLE_PATH`, and `EXP_PATH`.

	Confirm that each input directory contains the expected `.npy` files and that each export directory is writable.

2. **Learn spatial behavior representations.** Open `01_KAN_AE.ipynb` and run the cells from top to bottom. The notebook converts the time-series signals into timestamp-level spatial samples, trains the KAN autoencoder, and exports the KAN-AE model and encoded data.

3. **Learn temporal behavior representations.** Open `02_BiGRU_Classifier.ipynb` and run the cells from top to bottom. It loads the encoded data from the KAN-AE step, trains the bidirectional GRU classifier, evaluates it, and exports the trained model.

4. **Enroll and test authentication.** Run `03_UBM_Template_Auth.ipynb` after the BiGRU model and encoded data have been exported. The notebook creates one prototype/template per enrolled user, tunes the verification threshold on development data, and evaluates the held-out authentication test data.


_**NOTE:** Results are written into the configured experiment output directory. The export includes templates/prototypes, trial scores, summary and per-user metrics, threshold/configuration JSON files, ROC and enrollment-size arrays, and ROC/enrollment-size plots._ 

