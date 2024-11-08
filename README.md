
# OmniParserDeployonAzureML
This repository provides scripts and setup instructions to deploy OmniParser on Azure Machine Learning (Azure ML) or any VM with GPU.
## Prerequisites
- Azure ML Compute instance or any Azure VM with GPU support.
- IDE or terminal access to the GPU VM.
- Here is an example specifications:
  - **Virtual machine size**: Standard_NC12s_v3 (12 cores, 224 GB RAM, 1474 GB disk)
  - **Processing unit**: GPU - 2 x NVIDIA Tesla V100

## Getting Started
1. **Clone the repository**
   Open a terminal on your GPU-enabled VM and run the following commands:
   ```bash
   git clone https://github.com/MoreDhanshri/OmniParserDeployonAzureML.git
   cd OmniParserDeployonAzureML/
   sh setup.sh
   ```
## Set up Conda Environment
After setting up the repository, create and activate a Conda environment with Python 3.12:
```bash
conda create -n omni python==3.12 -y
source ~/anaconda3/etc/profile.d/conda.sh  # Ensure Conda is available in the script
conda activate omni
```
## Install Python Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```
## Run the Application
Execute the required Python scripts to start OmniParser:
```bash
python gradio_updated_demo.py
```

