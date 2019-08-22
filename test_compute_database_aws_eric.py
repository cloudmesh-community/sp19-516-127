###############################################################
# pytest -v --capture=no tests/test_compute_database.py
# pytest -v  tests/test_compute_database.py
# pytest -v --capture=no -v --nocapture tests/test_compute_database.py:Test_compute_database.<METHIDNAME>
###############################################################
from cloudmesh.management.configuration.name import Name
import subprocess
import time
import platform
import os
import sys
from pprint import pprint

from cloudmesh.common.Printer import Printer
from cloudmesh.common.util import HEADING
from cloudmesh.compute.vm.Provider import Provider
from cloudmesh.management.configuration.SSHkey import SSHkey
from cloudmesh.management.configuration.config import Config
from cloudmesh.variables import Variables
from cloudmesh.common.util import banner
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.console import Console
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.systeminfo import systeminfo

import pytest

@pytest.mark.incremental
class Test_Compute_Database:

    def setup(self):
        print()
        self.user = Config()["cloudmesh"]["profile"]["user"]
        self.clouduser = 'cc'
        self.name_generator = Name(
            experiment="exp",
            group="grp",
            user=self.user,
            kind="vm",
            counter=1)

        self.name = str(self.name_generator)
        self.name_generator.incr()

        self.new_name = str(self.name_generator)

        variables = Variables()
        clouds = Parameter.expand(variables['cloud'])
        cloud = clouds[0]

        self.p = Provider(name=cloud)

        self.secgroupname = "CM4TestSecGroup"
        self.secgrouprule = {"ip_protocol": "tcp",
                             "from_port": 8080,
                             "to_port": 8088,
                             "ip_range": "129.79.0.0/16"}
        self.testnode = None
        print("\n")

    def test_00_banner(self):
        StopWatch.start("banner")
        banner("START", color="RED")
        StopWatch.stop("banner")

    def test_01_list_flavors(self):
        HEADING()
        StopWatch.start("list flavors")
        flavors = self.p.flavors()
        StopWatch.stop("list flavors")

    def test_02_list_images(self):
        HEADING()
        StopWatch.start("list images")
        images = self.p.images()
        StopWatch.stop("list images")

    def test_03_list_nodes(self):
        HEADING()
        StopWatch.start("list nodes")
        nodes = self.p.list()
        StopWatch.stop("list nodes")

    def test_04_list_keys(self):
        HEADING()
        StopWatch.start("list keys")
        self.keys = self.p.keys()

    # pprint(self.keys)

    # print(Printer.flatwrite(self.keys,
    #                    sort_keys=["name"],
    #                    order=["name", "fingerprint"],
    #                    header=["Name", "Fingerprint"])
    #      )

        StopWatch.stop("list keys")

    def test_05_key_upload(self):
        HEADING()
        StopWatch.start("key upload")
        key = SSHkey()
        print(key.__dict__)

        self.p.key_upload(key)

        self.test_04_list_keys()
        StopWatch.stop("key upload")

    def test_06_list_images(self):
        HEADING()
        StopWatch.start("list images2")
        images = self.p.images()
        # pprint(images)
        sort_keys = self.p.p.output['image']['sort_keys']  # not pretty
        order = self.p.p.output['image']['order']  # not pretty
        header = self.p.p.output['image']['header']  # not pretty

        print(Printer.flatwrite(images,
                                sort_keys=sort_keys,
                                order=order,
                                header=header))
        StopWatch.stop("list images2")

    def test_07_list_vm(self):
        HEADING()
        StopWatch.start("list vm")
        vms = self.p.list()
        # pprint (vms)

        sort_keys = self.p.p.output['vm']['sort_keys']  # not pretty
        order = self.p.p.output['vm']['order']  # not pretty
        header = self.p.p.output['vm']['header']  # not pretty

        print(Printer.flatwrite(vms,
                                sort_keys=sort_keys,
                                order=order,
                                header=header)
              )

        StopWatch.stop("list vm")

    def test_print(self):
        HEADING()
        StopWatch.benchmark()


class a:

    def test_8_list_secgroups(self):
        HEADING()
        secgroups = self.p.list_secgroups()
        for secgroup in secgroups:
            print(secgroup["name"])
            rules = self.p.list_secgroup_rules(secgroup["name"])
            print(Printer.write(rules,
                                sort_keys=["ip_protocol", "from_port", "to_port", "ip_range"],
                                order=["ip_protocol", "from_port", "to_port", "ip_range"],
                                header=["ip_protocol", "from_port", "to_port", "ip_range"])
                  )

    def test_09_secgroups_add(self):
        HEADING()
        self.p.add_secgroup(self.secgroupname)
        self.test_05_list_secgroups()

    def test_10_secgroup_rules_add(self):
        HEADING()
        rules = [self.secgrouprule]
        self.p.add_rules_to_secgroup(self.secgroupname, rules)
        self.test_05_list_secgroups()

    def test_11_secgroup_rules_remove(self):
        HEADING()
        rules = [self.secgrouprule]
        self.p.remove_rules_from_secgroup(self.secgroupname, rules)
        self.test_05_list_secgroups()

    def test_12_secgroups_remove(self):
        HEADING()
        self.p.remove_secgroup(self.secgroupname)
        self.test_05_list_secgroups()

    def test_13_create(self):
        HEADING()
        image = "CC-Ubuntu16.04"
        size = "m1.medium"
        self.p.create(name=self.name,
                      image=image,
                      size=size,
                      # username as the keypair name based on
                      # the key implementation logic
                      ex_keyname=self.user,
                      ex_security_groups=['default'])
        time.sleep(5)
        nodes = self.p.list()
        node = self.p.find(nodes, name=self.name)
        pprint(node)

        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break

        assert node is not None

    def test_14_publicIP_attach(self):
        HEADING()
        pubip = self.p.get_public_ip()
        pprint(pubip)
        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break
        if self.testnode:
            print("attaching public IP...")
            self.p.attach_public_ip(self.testnode, pubip)
            time.sleep(5)
        self.test_04_list_vm()

    def test_15_publicIP_detach(self):
        print("detaching and removing public IP...")
        time.sleep(5)
        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break
        ipaddr = self.testnode.public_ips[0]
        pubip = self.p.cloudman.ex_get_floating_ip(ipaddr)
        self.p.detach_publicIP(self.testnode, pubip)
        time.sleep(5)
        self.test_04_list_vm()

    # def test_11_printer(self):
    #    HEADING()
    #    nodes = self.p.list()

    #    print(Printer.write(nodes, order=["name", "image", "size"]))

    # def test_01_start(self):
    #    HEADING()
    #    self.p.start(name=self.name)

    # def test_12_list_vm(self):
    #    self.test_04_list_vm()

    def test_16_info(self):
        HEADING()
        self.p.info(name=self.name)

    def test_17_destroy(self):
        HEADING()
        self.p.destroy(names=self.name)
        nodes = self.p.list()
        node = self.p.find(nodes, name=self.name)

        pprint(node)

        assert node["extra"]["task_state"] == "deleting"

    def test_18_list_vm(self):
        self.test_04_list_vm()

    def test_19_vm_login(self):
        self.test_04_list_vm()
        self.test_10_create()
        # use the self.testnode for this test
        time.sleep(30)
        self.test_11_publicIP_attach()
        time.sleep(5)
        nodes = self.p.list(raw=True)
        for node in nodes:
            if node.name == self.name:
                self.testnode = node
                break
        # pprint (self.testnode)
        # pprint (self.testnode.public_ips)
        pubip = self.testnode.public_ips[0]

        COMMAND = "cat /etc/*release*"

        ssh = subprocess.Popen(["ssh", "%s@%s" % (self.clouduser, pubip), COMMAND],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print("ERROR: %s" % error)
        else:
            print("RESULT:")
            for line in result:
                line = line.decode("utf-8")
                print(line.strip("\n"))

        self.test_14_destroy()
        self.test_04_list_vm()

    def print_benchmark(self):
        HEADING()
        StopWatch.benchmark() 

#class other:

    #def test_30_rename(self):
    #    HEADING()
#        self.p.rename(source=self.name, destination=self.new_name)

    # def test_01_stop(self):
    #    HEADING()
    #    self.stop(name=self.name)

    # def test_01_suspend(self):
    #    HEADING()
    #    self.p.suspend(name=self.name)

    # def test_01_resume(self):
    #    HEADING()
    #    self.p.resume(name=self.name)
