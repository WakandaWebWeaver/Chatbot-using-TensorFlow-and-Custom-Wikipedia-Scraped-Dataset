  # Chatbot using TensorFlow and Custom Wikipedia-Scraped Dataset


### Getting Started

#### Prerequisites
- Python 3.x (3.10 preferred)
- Install dependencies using:
  ```
  pip install requests beautifulsoup4 tqdm
  ```
- To install Tensorflow, using pip or pip3 sometimes throws false negatives, instead run:
  ```
  python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/your-os/cpu/tensorflow-1.12.0-py3-none-any.whl
  ```
- Check out this [SO post](https://stackoverflow.com/questions/38896424/tensorflow-not-found-using-pip) for more info

#### Running the Script (run this file first, to ensure data.txt is updated)
1. Clone the repository:
   ```
   git clone https://github.com/devjoshua312/response-generation-using-wikipidia-scraped-language-model.git > directory_name
   cd directory_name
   ```

2. Run the script:
   ```
   python wiki.py
   ```

3. The scraped and cleaned text will be added to the `data.txt` file.

#### Running the main file

1. While in the project directory, run:
   ```
   python train.py
   ```


   Keep in mind that this is a crude version of what a practical chatbot might be. The program may fail to run, or in most cases, run without generating the required output.
