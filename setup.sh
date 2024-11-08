# Clone the main OmniParser repository
git clone https://github.com/microsoft/OmniParser.git

# Navigate to the weights directory
cd OmniParser/weights/ || exit
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
# Move best.pt to the icon_detect folder
mv best.pt OmniParser/weights/icon_detect/
# Move gradio_updated_demo.py to the OmniParser folder
mv gradio_updated_demo.py OmniParser/
