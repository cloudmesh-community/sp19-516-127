###############################################################
# pytest -v --capture=no test_benchmark.py
# pytest -v  test_benchmark.py
# pytest -v --capture=no test_benchmark.py:Test_benchmark.<METHODNAME>
###############################################################
import os
import sys
import platform

import pytest
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import HEADING
#from cloudmesh.common.systeminfo import systeminfo
from pprint import pprint


@pytest.mark.incremental
class TestConfig:

    def test_help(self):
        HEADING()

        StopWatch.start("cms help")
        result = Shell.execute("cms help", shell=True)
        StopWatch.stop("cms help")

        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_vm_status1(self):
        HEADING()

        StopWatch.start("cms vm status1")
        result = Shell.execute("cms newawsvm status", shell=True)
        StopWatch.stop("cms vm status1")

        VERBOSE(result)

        assert "Currently" in result
 

    def test_vm_status2(self):
        HEADING()

        StopWatch.start("cms vm status2")
        result = Shell.execute("cms newawsvm status test_name", shell=True)
        StopWatch.stop("cms vm status2")

        VERBOSE(result)

        assert "Currently" in result
 
        
    def test_vm_status3(self):
        HEADING()

        StopWatch.start("cms vm status3")
        result = Shell.execute("cms newawsvm status all", shell=True)
        StopWatch.stop("cms vm status3")

        VERBOSE(result)

        assert "Currently" in result

        
    def test_vm_boot1(self):
        HEADING()

        StopWatch.start("cms vm boot1")
        result = Shell.execute("cms newawsvm boot --dryrun", shell=True)
        StopWatch.stop("cms vm boot1")

        VERBOSE(result)

        assert "Started 1 node" in result

        
    def test_vm_boot2(self):
        HEADING()

        StopWatch.start("cms vm boot2")
        result = Shell.execute("cms newawsvm boot --n=10 --dryrun", shell=True)
        StopWatch.stop("cms vm boot2")

        VERBOSE(result)

        assert "Started 10 node" in result
 
        
    def test_vm_boot3(self):
        HEADING()

        StopWatch.start("cms vm boot3")
        result = Shell.execute("cms newawsvm boot --name=TEST_VM --dryrun", shell=True)
        StopWatch.stop("cms vm boot3")

        VERBOSE(result)

        assert "Started 1 node" in result


    def test_vm_stop1(self):
        HEADING()

        StopWatch.start("cms vm stop1")
        result = Shell.execute("cms newawsvm stop test1 --dryrun", shell=True)
        StopWatch.stop("cms vm stop1")

        VERBOSE(result)

        assert "stopped" in result


    def test_vm_stop2(self):
        HEADING()

        StopWatch.start("cms vm stop2")
        result = Shell.execute("cms newawsvm stop test1,test2 --dryrun", shell=True)
        StopWatch.stop("cms vm stop2")

        VERBOSE(result)

        assert "stopped" in result
  

    def test_vm_start1(self):
        HEADING()

        StopWatch.start("cms vm start1")
        result = Shell.execute("cms newawsvm start test1 --dryrun", shell=True)
        StopWatch.stop("cms vm start1")

        VERBOSE(result)

        assert "restarted" in result


    def test_vm_start2(self):
        HEADING()

        StopWatch.start("cms vm start2")
        result = Shell.execute("cms newawsvm start test1,test2 --dryrun", shell=True)
        StopWatch.stop("cms vm start2")

        VERBOSE(result)

        assert "started" in result

        
    def test_vm_terminate(self):
        HEADING()

        StopWatch.start("cms vm terminate")
        result = Shell.execute("cms newawsvm terminate test1 --dryrun", shell=True)
        StopWatch.stop("cms vm terminate")

        VERBOSE(result)

        assert "terminated" in result


    def test_vm_default(self):
        HEADING()

        StopWatch.start("cms vm default")
        result = Shell.execute("cms newawsvm default", shell=True)
        StopWatch.stop("cms vm default")

        VERBOSE(result)

        assert "yaml" in result

