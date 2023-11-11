import os


def get_path(file_name) -> str:
    '''
    Создает путь к файлу file_name в папке preprocessing_data
    '''
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, file_name)
