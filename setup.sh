# Clone the main OmniParser repository
git clone https://github.com/microsoft/OmniParser.git


# Navigate to the weights directory
cd weights/ || exit

# Update the system package list
sudo apt update

# Install Git Large File Storage (LFS)
sudo apt install -y git-lfs

# Initialize Git LFS
git lfs install

# Clone the OmniParser model weights from Hugging Face
git clone https://huggingface.co/microsoft/OmniParser

# Move all contents from OmniParser to weights directory and remove OmniParser
mv OmniParser/* .
rm -rf OmniParser  # Ensure OmniParser directory is fully removed

# Go back to the main OmniParser directory
cd ..

# Create and activate a Conda environment with Python 3.12
conda create -n omni python==3.12 -y
#source ~/anaconda3/etc/profile.d/conda.sh  # Ensure Conda is available in the script
conda activate omni

# Install required Python packages
pip install -r requirements.txt

# Run the required Python scripts
python gradio_demo.py