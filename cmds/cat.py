

def cmd_cat(repo, parameters):
    file_path = parameters
    file_content = repo.get_file_content(file_path)
    print(file_content)