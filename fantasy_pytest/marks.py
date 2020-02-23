"""
=============
marks
=============
"""
import os
import pytest

skip_in_ci = pytest.mark.skipif(
    os.environ.get('FLASK_ENV') == 'drone',
    reason="CI/CD Mode Actived..."
)
