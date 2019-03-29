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
from libcloud.compute.base import NodeImage

from cloudmesh.abstractclass.ComputeNodeABC import ComputeNodeABC 

class AwsActions(object):

    ProviderMapper = {
        "aws": LibcloudProvider.EC2
    }

    Provider = ProviderMapper["aws"]

    def __init__(self, **kwargs):
        self._provider = LibcloudProvider.EC2



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

        # Needs to be initialized somewhere else 
        conf=Config("~/.cloudmesh/cloudmesh4.yaml")["cloudmesh"]
        auth=conf["cloud"]['aws']

        aws_access_key_id=auth['credentials']['EC2_ACCESS_ID']
        aws_secret_access_key=auth['credentials']['EC2_SECRET_KEY']
        region_name=auth['default']['region']

        EC2Driver = get_driver(LibcloudProvider.EC2)
                      
        # drivers contains list of drivers, could work with multiple drivers
        drivers = [EC2Driver(aws_access_key_id, aws_secret_access_key, region='us-east-2')]
        
        current_status={}
        
        if arguments.status:
            names = []
            nodes = [] 
            if arguments["--cloud"]:
                clouds = get_clouds(arguments, variables)
                print(clouds)
#                for cloud in clouds:
#                    Console.msg(
#                        "find names in cloud {cloud}".format(cloud=cloud))
#                    # names = find all names in these clouds
            else:
                names = get_names(arguments, variables)
            
                        
            if arguments["NAMES"]:
                names += arguments["NAMES"]
            else:
                names = ["test", "test2", "test3"] 

            nodes = []

            for driver in drivers:
                nodes += driver.list_nodes()
            print("Current nodes:",nodes)
            print(nodes[0])
            # nodes contains all current nodes associated with aws_access_key_iD

            for name in names:
                found = 0
                for node in nodes:
                    if node.name == name:
                        print("found",node.name) 
                        print(node.name,"status:",node.state)
                        found=1
                if found == 0:
                    print(name,"status:","not found")
            return
        
        elif arguments.boot:
            try:
                numb_of_nodes=int(n)
            except:
                numb_of_nodes=1
                
            print("start")
            
            driver_ec2 = EC2Driver(aws_access_key_id, aws_secret_access_key, region='us-east-2')
            numb_of_nodes=1
            for number in range(numb_of_nodes):
                name      = 'test_cloudmesh' + str(number)
                image     = 'ami-0653e888ec96eab9b'     
                flavor    = 't2.micro'
                key       = 'test_awskeys'        
                public_ip = '3.17.128.170'
            
                current_status[name] = "starting"
                
                #images = driver_ec2.list_images()
                #image1 = [i for i in images if i.id == image][0]

                sizes = driver_ec2.list_sizes()
                size = [s for s in sizes if s.id == 't2.micro'][0]   

                #node = self._provider.allocate_node(name=name, key=key, image=image, flavor=flavor)
                #node = driver_ec2.create_node(name=name, key=key, image=image1, size=size)
                
                node_image = NodeImage(id=image, name=None, driver=driver_ec2)
                node = driver_ec2.create_node(name='test', image=node_image, size=size) 
                
                print(name,node.id,"status=starting")
                #optional wait here?
                #print('Waiting...')
                #node.wait_until_running()
                #current_status[name] = "running"
            return

                   
        elif arguments.ssh:
            # need to get name.pem from aws 
            # ssh -i "name.pem" ubuntu@ec2-3-17-128-170.us-east-2.compute.amazonaws.com
            print("ssh")
            return
        
        elif arguments.stop:
            print("stop")
            # use these as a demo, node_id can be retrieved from the same code in vm status implemented above
            # implemented above as list_nodes() and node.name
            node_id = 'i-08f3ed1058f95f8bd' 
            driver_ec2.ex_stop_node(node_id) 
            return
        
        elif arguments.delete:
            print("delete")
            node_id = 'i-08f3ed1058f95f8bd'
            driver_ec2._get_terminate_boolean(node_id)
            return
        
        else:
            print("not implemented")

