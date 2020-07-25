from hashlib import sha256
import os


def get_hash_name(raw_data):
    '''The hashing function. raw_data is file content'''
    return sha256(raw_data).hexdigest()


def find_correct_dir(hash_name):
    '''The required path for file'''
    return os.path.join(hash_name[:2], hash_name)
