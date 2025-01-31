# Setup Environment Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

# Setup Environment Shell/Terminal
mkdir dicoding-data-analyst-sub
cd dicoding-data-analyst-sub
pipenv install
pipenv shell
pip install -r requirements.txt

# Run Streamlit App
streamlit run dashboard.py 