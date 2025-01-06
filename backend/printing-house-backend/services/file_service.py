from werkzeug.utils import secure_filename

from db.models import File


def handle_uploaded_files(files):
    uploaded_files = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_data = file.read()
            user_file = File(
                filename=filename,
                file_data=file_data,
            )
            uploaded_files.append(user_file)
    return uploaded_files
