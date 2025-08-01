import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ['Trillium Trading']
usernames = ['ttrading']
passwords = ['XXX']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent/ "hash_pw.pl"

with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)


print(file_path)



