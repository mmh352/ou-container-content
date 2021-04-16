"""Tests for the distribution functionality."""
import os
import shutil

from ou_container_content.distributor import distribute

basepath = os.path.join(os.getcwd(), os.path.dirname(__file__))


def prepare_structures(name):
    """Prepare the temporary structures for the test."""
    if os.path.exists(os.path.join(basepath, 'tmp')):
        shutil.rmtree(os.path.join(basepath, 'tmp'))
    shutil.copytree(os.path.join(basepath, f'{name}_target'), os.path.join(basepath, 'tmp'))


def cleanup_structures():
    """Cleanup the temporary structures."""
    if os.path.exists(os.path.join(basepath, 'tmp')):
        shutil.rmtree(os.path.join(basepath, 'tmp'))


def get_file_content(path):
    """Get the file content for the specified path."""
    with open(os.path.join(basepath, 'tmp', path)) as in_f:
        return in_f.read()


def test_always_overwrite():
    """Test that the always overwriting works as designed."""
    prepare_structures('overwrite_always')
    config = {
        'paths': [
            {
                'source': os.path.join(basepath, 'overwrite_always_source'),
                'target': os.path.join(basepath, 'tmp'),
                'overwrite': 'always'
            }
        ]
    }
    distribute(config)
    assert get_file_content('file1.txt') == 'File 1\n'
    assert get_file_content('dir1/file2.txt') == 'File 2\n'
    assert get_file_content('dir2/file3.txt') == 'File 3\n'
    assert get_file_content('dir2/file4.txt') == 'File 4\n'
    cleanup_structures()


def test_never_overwrite():
    """Test that the never overwriting works as designed."""
    prepare_structures('overwrite_never')
    config = {
        'paths': [
            {
                'source': os.path.join(basepath, 'overwrite_never_source'),
                'target': os.path.join(basepath, 'tmp'),
                'overwrite': 'never'
            }
        ]
    }
    distribute(config)
    assert get_file_content('file1.txt') == 'Old Content\n'
    assert get_file_content('dir1/file2.txt') == 'File 2\n'
    assert get_file_content('dir2/file3.txt') == 'Old Content\n'
    assert get_file_content('dir2/file4.txt') == 'File 4\n'
    cleanup_structures()
