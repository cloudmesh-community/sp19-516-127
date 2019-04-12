###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_newawsvm.py:Test_newawsvm.test_001
# pytest -v --capture=no tests/test_newawsvm.py
# pytest -v  tests/test_newawsvm.py
###############################################################

from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
import pytest

@pytest.mark.incremental
class Test_newawsvm:

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_create(self):
        a = 1
        assert a==1
