from huggingface_hub import upload_file, HfApi
import os
from get_matches import find_matches


os.chdir('../')
os.chdir(os.getcwd() + '/tree')

model_path = os.getcwd() + 'rf1_bin_model.pkl'

api = HfApi()
upload_file(
    path_or_fileobj='rf1_bin_model.pkl',
    path_in_repo='rf1_bin_model.pkl',
    repo_id='parthdiwane/sportly-random-forest',
    repo_type='model'
)

os.chdir('../')
os.chdir(os.getcwd() + '/scripts_main')



