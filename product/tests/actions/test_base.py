from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path


def make_simple_file() -> SimpleUploadedFile:
    path = Path(__file__).parent.parent.parent.parent
    file_path = ''.join(
        (str(path), '/product/tests/base_tests/file_test.pdf')
    )
    simple_file = SimpleUploadedFile(
        name='file_test.pdf',
        content=open(file_path, 'rb').read(),
        content_type='file/pdf'
    )
    return simple_file
