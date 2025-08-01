from huggingface_hub import upload_file, HfApi
import os
from get_matches import find_matches


os.chdir('../')
os.chdir(os.getcwd() + '/tree')

model_path = os.getcwd() + 'rf_model.pkl'

api = HfApi()
upload_file(
    path_or_fileobj='rf_model.pkl',
    path_in_repo='rf_model.pkl',
    repo_id='parthdiwane/sportly-random-forest',
    repo_type='model'
)
upload_file(
    path_or_fileobj='rf1_model.pkl',
    path_in_repo='rf1_model.pkl',
    repo_id='parthdiwane/sportly-random-forest',
    repo_type='model'
)

os.chdir('../')
os.chdir(os.getcwd() + '/scripts_main')



