from __future__ import print_function

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.shell.variables import Variables
from cloudmesh.common.console import Console
from pprint import pprint
from cloudmesh.common.parameter import Parameter
from cloudmesh.management.configuration.config import Active
from cloudmesh.management.configuration.config import Config

from libcloud.compute.types import Provider as LibcloudProvider 
from libcloud.compute.providers import get_driver

from cloudmesh.abstractclass.ComputeNodeABC import ComputeNodeABC 

# cms vm status --cloud='aws'
# cms vm status NAMES --cloud='aws'


class AwsActions(object):

    ProviderMapper = {
        "aws": LibcloudProvider.EC2
    }

    Provider = ProviderMapper["aws"]

    def __init__(self, **kwargs):
        self._provider = LibcloudProvider.EC2


    def list_flavors(self):
        flavors = self._provider.flavors()
        print(Printer.list(flavors))


    def allocate_node(self, image=None, flavor=None, key=None, public_ip=None):

        # default kwargs can't be used due to dself, ocopt

        name      = 'cloudmesh'
        image     = image      or 'ami-c58c1dd3'
        flavor    = flavor     or 't2.micro'
        key       = key        or gethostname()
        public_ip = public_ip  or False

        node = self._provider.allocate_node(name=name, key=key, image=image, flavor=flavor)
        print('Booted', node.id)

        if public_ip:
            addr = None
            for a in self._provider.addresses():
                if not a.instance_id:
                    print('Using old ip', a.public_ip)
                    addr = a
                    break

            if not addr:
                print('Allocating new ip')
                addr = self._provider.allocate_ip()

            print('Waiting for node')
            node.wait_until_running()
            print('Associating public ip', addr.public_ip)
            addr.associate(InstanceId=node.id)



    def deallocate_node(self, id):
        self._provider.deallocate_node(id)


    def list_nodes(self):
        nodes = []
        for n in self._provider.nodes():
            d = {}
            d['id'] = n.id
            d['key'] = n.key_name
            d['image_id'] = n.image_id
            d['private_ip'] = n.private_ip_address
            d['public_ip'] = n.public_ip_address
            d['state'] = n.state['Name']
            nodes.append(d)

        print(Printer.list(nodes))

class VmCommand(PluginCommand):

    # see also https://github.com/cloudmesh/client/edit/master/cloudmesh_client/shell/plugins/VmCommand.py

    # noinspection PyUnusedLocal
    @command
    def do_vm(self, args, arguments):
        """
        ::
            Usage:
                vm ping [NAMES] [--cloud=CLOUDS] [N]
                vm check [NAMES] [--cloud=CLOUDS]
                vm refresh [NAMES] [--cloud=CLOUDS]
                vm status [NAMES] [--cloud=CLOUDS]
                vm console [NAME] [--force]
                vm start [NAMES] [--cloud=CLOUD] [--dryrun]
                vm stop [NAMES] [--cloud=CLOUD] [--dryrun]
                vm terminate [NAMES] [--cloud=CLOUD] [--dryrun]
                vm delete [NAMES] [--cloud=CLOUD] [--dryrun]
                vm list [NAMES]
                        [--cloud=CLOUDS]
                        [--format=FORMAT]
                        [--refresh]
                vm boot [--name=NAME]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--public]
                        [--secgroup=SECGROUPs]
                        [--key=KEY]
                        [--dryrun]
                vm boot [--n=COUNT]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--public]
                        [--secgroup=SECGROUPS]
                        [--key=KEY]
                        [--dryrun]
                vm run [--name=NAMES] [--username=USERNAME] [--dryrun] COMMAND
                vm script [--name=NAMES] [--username=USERNAME] [--dryrun] SCRIPT
                vm ip assign [NAMES]
                          [--cloud=CLOUD]
                vm ip show [NAMES]
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--format=FORMAT]
                           [--refresh]
                vm ip inventory [NAMES]
                vm ssh [NAMES] [--username=USER]
                         [--quiet]
                         [--ip=IP]
                         [--key=KEY]
                         [--command=COMMAND]
                         [--modify-knownhosts]
                vm rename [OLDNAMES] [NEWNAMES] [--force] [--dryrun]
                vm wait [--cloud=CLOUD] [--interval=SECONDS]
                vm info [--cloud=CLOUD]
                        [--format=FORMAT]
                vm username USERNAME [NAMES] [--cloud=CLOUD]
                vm resize [NAMES] [--size=SIZE]
            Arguments:
                COMMAND        positional arguments, the commands you want to
                               execute on the server(e.g. ls -a) separated by ';',
                               you will get a return of executing result instead of login to
                               the server, note that type in -- is suggested before
                               you input the commands
                NAME           server name. By default it is set to the name of last vm from database.
                NAMES          server name. By default it is set to the name of last vm from database.
                KEYPAIR_NAME   Name of the vm keypair to be used to create VM. Note this is
                               not a path to key.
                NEWNAMES       New names of the VM while renaming.
                OLDNAMES       Old names of the VM while renaming.
            Options:
              -H --modify-knownhosts  Do not modify ~/.ssh/known_hosts file
                                      when ssh'ing into a machine
                --username=USERNAME   the username to login into the vm. If not
                                      specified it will be guessed
                                      from the image name and the cloud
                --ip=IP          give the public ip of the server
                --cloud=CLOUD    give a cloud to work on, if not given, selected
                                 or default cloud will be used
                --count=COUNT    give the number of servers to start
                --detail         for table print format, a brief version
                                 is used as default, use this flag to print
                                 detailed table
                --flavor=FLAVOR  give the name or id of the flavor
                --group=GROUP          give the group name of server
                --secgroup=SECGROUP    security group name for the server
                --image=IMAGE    give the name or id of the image
                --key=KEY        specify a key to use, input a string which
                                 is the full path to the private key file
                --keypair_name=KEYPAIR_NAME   Name of the vm keypair to
                                              be used to create VM.
                                              Note this is not a path to key.
                --user=USER      give the user name of the server that you want
                                 to use to login
                --name=NAME      give the name of the virtual machine
                --force          rename/ delete vms without user's confirmation
                --command=COMMAND
                                 specify the commands to be executed
            Description:
                commands used to boot, start or delete servers of a cloud
                vm default [options...]
                    Displays default parameters that are set for vm boot either
                    on the default cloud or the specified cloud.
                vm boot [options...]
                    Boots servers on a cloud, user may specify flavor, image
                    .etc, otherwise default values will be used, see how to set
                    default values of a cloud: cloud help
                vm start [options...]
                    Starts a suspended or stopped vm instance.
                vm stop [options...]
                    Stops a vm instance .
                vm delete [options...]
                    Delete servers of a cloud, user may delete a server by its
                    name or id, delete servers of a group or servers of a cloud,
                    give prefix and/or range to find servers by their names.
                    Or user may specify more options to narrow the search
                vm floating_ip_assign [options...]
                    assign a public ip to a VM of a cloud
                vm ip show [options...]
                    show the ips of VMs
                vm ssh [options...]
                    login to a server or execute commands on it
                vm list [options...]
                    same as command "list vm", please refer to it
                vm status [options...]
                    Retrieves status of last VM booted on cloud and displays it.
            Tip:
                give the VM name, but in a hostlist style, which is very
                convenient when you need a range of VMs e.g. sample[1-3]
                => ['sample1', 'sample2', 'sample3']
                sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']
            Quoting commands:
                cm vm login gvonlasz-004 --command=\"uname -a\"
        """

        def map_parameters(arguments, *args):
            for arg in args:
                flag = "--" + arg
                if flag in arguments:
                    arguments[arg] = arguments[flag]
                else:
                    arguments[arg] = None

        def get_clouds(arguments, variables):

            clouds = arguments["cloud"] or arguments["--cloud"] or variables[
                "cloud"]
            if "active" == clouds:
                active = Active()
                clouds = active.clouds()
            elif "aws" == clouds:
                conf=Config("~/.cloudmesh/cloudmesh4.yaml")["cloudmesh"]
                auth=conf["cloud"]['aws']
                aws = AwsActions(
                    aws_access_key_id=auth['credentials']['EC2_ACCESS_ID'],
                    aws_secret_access_key=auth['credentials']['EC2_SECRET_KEY'],
                    region_name=auth['default']['region']
                )
                pprint("loaded aws")
            else:
                clouds = Parameter.expand(clouds)

            if clouds is None:
                Console.error("you need to specify a cloud")
                return None

            return clouds

        def get_names(arguments, variables):
            names = arguments["NAME"] or arguments["NAMES"] or arguments[
                "--name"] or variables["vm"]
            if names is None:
                Console.error("you need to specify a vm")
                return None
            else:
                return Parameter.expand(names)

        def name_loop(names, label, f):
            names = get_names(arguments, variables)
            for name in names:
                Console.msg("{label} {name}".format(label=label, name=name))
                # r = f(name)

        map_parameters(arguments,
                       'active',
                       'cloud',
                       'command',
                       'dryrun',
                       'flavor',
                       'force',
                       'format',
                       'group',
                       'image',
                       'interval',
                       'ip',
                       'key',
                       'modify-knownhosts',
                       'n',
                       'name',
                       'public',
                       'quiet',
                       'refresh',
                       'secgroup',
                       'size',
                       'username')

        pprint(arguments)

        variables = Variables()

        if arguments.status:
            names = []
            nodes = [] 
            if arguments["--cloud"]:
                clouds = get_clouds(arguments, variables)
                print(clouds)
                # for cloud in clouds:
                #    Console.msg(
                #        "find names in cloud {cloud}".format(cloud=cloud))
                #    # names = find all names in these clouds
                #    # implemented as nodes for aws below
            else:
                names = get_names(arguments, variables)
            
                        
            if arguments["NAMES"]:
                names += arguments["NAMES"]
            else:
                names = ["test1", "test2", "test3"] 

            # ---------------------------------------
            # Needs to be initialized somewhere else?
            #
            
            conf=Config("~/.cloudmesh/cloudmesh4.yaml")["cloudmesh"]
            auth=conf["cloud"]['aws']

            aws_access_key_id=auth['credentials']['EC2_ACCESS_ID']
            aws_secret_access_key=auth['credentials']['EC2_SECRET_KEY']
            region_name=auth['default']['region']

            #
            #
            # ---------------------------------------
            
            EC2Driver = get_driver(LibcloudProvider.EC2)
                        
            # drivers contains list of drivers, could work with multiple drivers
            drivers = [EC2Driver(aws_access_key_id, aws_secret_access_key)]

            for driver in drivers:
                nodes += driver.list_nodes()
            # print("Current nodes:",nodes) will ist all nodes found in drivers

            # nodes contains all current nodes associated with aws_access_key_iD

            for name in names:
                found = 0
                for node in nodes:
                    if node.name == name:
                        print("name",node.name,"status:",node.status)
                        found=1
                if found == 0:
                    print("name:",name,"status:","not found")

            return

        else:
            print("not implemented")

