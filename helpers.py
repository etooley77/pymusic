

def check_file_name_length(file_path):
    # Get the file name
    file_name = file_path.split('/')[-1]

    # Check if the file path is longer than the limit
    if len(file_name) > 40:
        adj_file_name = file_name.split('.')[0][0:35] + ".wav"
        return adj_file_name
    else:
        return file_name