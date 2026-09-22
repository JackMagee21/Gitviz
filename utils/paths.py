import posixpath

def figure_path(current_path, target_path):
    # work out the full path of the target path, relative to the current path.
    combined = None

    if target_path.startswith("/"):  # absolute path
        combined = target_path
    else:  # relative path
        combined = posixpath.join("/", current_path, target_path)    

    normalised = posixpath.normpath(combined) # resolves "..", "." and "//"

    # normalised comes out with a / at the end and github doesn't expect that=
    return normalised.strip("/")