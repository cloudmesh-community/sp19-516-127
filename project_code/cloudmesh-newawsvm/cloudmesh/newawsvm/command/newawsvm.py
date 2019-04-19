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


#
#	run demo/run_vm.sh script for a demo of starting, displaying status, and stopping nodes in aws vm
#       pytest in progress
#

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

class NewawsvmCommand(PluginCommand):

    @command
    def do_newawsvm(self, args, arguments):
        """
        ::
            Usage:
                newawsvm status [NAMES] [--cloud=CLOUDS]
                newawsvm stop [NAMES] [--cloud=CLOUD] [--dryrun]
                newawsvm list [NAMES]
                        [--cloud=CLOUDS]
                        [--format=FORMAT]
                        [--refresh]
                newawsvm boot [--name=NAME]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--public]
                        [--secgroup=SECGROUPs]
                        [--key=KEY]
                        [--dryrun]
                newawsvm boot [--n=COUNT]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--public]
                        [--secgroup=SECGROUPS]
                        [--key=KEY]
                        [--dryrun]
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
                vm stop [options...]
                    Stops a vm instance .
                vm status [options...]
                    Retrieves status of VM booted on cloud and displays it.
            Tip:
                give the VM name, but in a hostlist style, which is very
                convenient when you need a range of VMs e.g. sample[1-3]
                => ['sample1', 'sample2', 'sample3']
                sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']
            Quoting commands:
                cm vm login gvonlasz-004 --command=\"uname -a\"
        """
        #print(args, arguments)
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

            #if clouds is None:
            #    Console.error("")
            #    return None

            return clouds

        def get_names(arguments, variables):
            names = arguments["NAME"] or arguments["NAMES"] or arguments[
                "--name"] or variables["vm"]
            if names is None:
                return None
            else:
                return Parameter.expand(names)

        def name_loop(names, label, f):
            names = get_names(arguments, variables)
            for name in names:
                Console.msg("{label} {name}".format(label=label, name=name))
                # r = f(name)
		
        def increment_string(strng):
            ls = list(strng)
            numb_where = [0]*len(ls)
            numb = ""
            count_zeros = 0
            i = 0
            insert = len(ls) - 1
            while i < len(ls):
                try:
                    int(ls[i])
                    numb_where[i] = 1
                    if int(ls[i]) == 0 and numb_where[i-1] == 0:
                        numb_where[i] = 1
                        count_zeros += 1
                    elif numb_where[i-1] == 0:
		    # found a second number (disconnected)
                        if numb_where[i] == 1:
                            j = 0
                            while j < i:
                                numb_where[j] == 0
                                j += 1
                        numb = ""
                        numb = numb + ls[i]
                        insert = i
                    else:
                        numb = numb + ls[i]
                    i += 1
                except:
                    i += 1
                    continue

            if sum(numb_where) == 0:
                if count_zeros == 0:
                    return strng + str(1)
                else: 
                    new_strng = ""
                    i = 0
                    rm_zero = 1
                    while i < len(ls):
                        if ls[i] == str(0) and rm_zero == 1:
                            rm_zero = 0
                        else:
                            new_strng = new_strng + ls[i]
                        i += 1  
                    return new_strng + str(1)    
            b4 = len(numb)
            numb = int(numb) + 1
            after = len(str(numb))
            if b4 != after:
                rm_zero = 1
            else:
                rm_zero = 0
            new_strng = ""
            new_numb_added = 0
            i = 0
            while i < len(numb_where):
                if numb_where[i] == 0:
                    if numb_where[i+1] == 1 and rm_zero == 1 and ls[i] == str(0):
                        rm_zero = 0
                    else:
                        new_strng = new_strng + ls[i]
                elif new_numb_added == 0:
                    if i == insert:
                        new_strng = new_strng + str(numb)
                        new_numb_added = 1
                    else: 
                        new_strng = new_strng + ls[i]

                i += 1
            return new_strng

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

        #pprint(arguments)

        variables = Variables()

        # INITIALIZE 
        conf=Config("~/.cloudmesh/cloudmesh4.yaml")["cloudmesh"]
        auth=conf["cloud"]['aws']

        aws_access_key_id=auth['credentials']['EC2_ACCESS_ID']
        aws_secret_access_key=auth['credentials']['EC2_SECRET_KEY']
        region_name=auth['default']['region']

        EC2Driver = get_driver(LibcloudProvider.EC2)
        driver_ec2 = EC2Driver(aws_access_key_id, aws_secret_access_key, region='us-east-2')
        # drivers contains list of drivers, could work with multiple drivers
        drivers = [EC2Driver(aws_access_key_id, aws_secret_access_key, region='us-east-2')]
        
        current_status={}
        nodes = []
        for driver in drivers:
            nodes += driver.list_nodes()
        for node in nodes:
            current_status[node.name]=node.state
        #pprint(current_status)
	
        # initialized


 
        if arguments.status:
            #if names == None:
            #    names = []
 
            if arguments["--cloud"]:
                clouds = get_clouds(arguments, variables)
                #print(clouds)
            else:
                names = get_names(arguments, variables)
            #pprint(names) 
            if names == None:
                names = []                        

            #print("Current nodes:",nodes)
            # nodes contains all current nodes associated with aws_access_key_id

            numb_of_nodes=len(nodes)

            if "all" in names or len(names) == 0:
                print("--Status on all nodes:")
                print("--Currently, there are",numb_of_nodes,"nodes.")
                for driver in drivers:
                    for node in nodes:
                        print("Name:",node.name,"\n  Status:",node.state,"\n  InstanceId:",node.id,"\n")
                return
            elif len(names) == 1:
                name=names[0]
                print("--Finding the status on:", name,"...")
                found = 0
                for node in nodes:
                    if node.name == name:
                        print(node.name,": found") 
                        print("  Status:",node.state)
                        found=1
                if found == 0:
                    print(name,": not found")
            elif "all" not in names and len(names) > 1:
                for name in names:
                    print("--Finding the status on:", name,"...")
                    found = 0
                    for node in nodes:
                        if node.name == name:
                            print(node.name,": found") 
                            print("  Status:",node.state)
                            found=1
                    if found == 0:
                        print(name,": not found")
            if found==0:
                print("--Status on all nodes:")
                print("--Currently, there are",numb_of_nodes,"nodes.")
                for driver in drivers:
                    for node in nodes:
                        print("Name:",node.name,"\n  Status:",node.state,"\n  InstanceId:",node.id,"\n")

            return
        
        elif arguments.boot:
            try:
                numb_of_nodes=int(n)
            except:
                numb_of_nodes=1
                
            print("--Starting nodes")
            numb_of_nodes=1
            for number in range(numb_of_nodes):
                if number < 10:
              	    name = 'test00_cloudmesh' + '0' + str(number)
                else:
                    name = 'test00_cloudmesh' + str(number)
                image     = 'ami-0653e888ec96eab9b'     
                flavor    = 't2.micro'
                key       = 'test_awskeys'        
                            
                current_status[name] = "starting"
                sizes = driver_ec2.list_sizes()
                size = [s for s in sizes if s.id == 't2.micro'][0]   

                node_image = NodeImage(id=image, name=None, driver=driver_ec2)
                found = 1
                while found == 1:
                    if name in current_status:
                        print(name,"already taken")
                        name = increment_string(name)
                        print("using",name,"instead")
                    else:
                        found = 0
                node = driver_ec2.create_node(name=name, image=node_image, size=size) 
                print(name,node.id,"status=starting; DRY RUN\n")
                #optional wait here?
                print('Waiting...')
                #node.wait_until_running()
                #current_status[name] = "running"
            print("--Started",n,"node(s)")
            return

                   
        elif arguments.ssh:
            # need to get name.pem from aws 
            # ssh -i "name.pem" ubuntu@ec2-3-17-128-170.us-east-2.compute.amazonaws.com
            print("ssh")
            return
        
        elif arguments.stop:
            print("--Stopping nodes")
            names = get_names(arguments, variables)
            #pprint(names) 
            if names == None:
                names = []
                print("--Error: you need to specify a node to stop")
            #names = ["test_cloudmesh0","test_cloudmesh01"]
            elif len(names) > 2:
                for name in names:
                    found = 0
                    for node in nodes:
                        if node.name == name:
                            print(node.name,": found") 
                            print("stopping",node.name)
                            driver_ec2.ex_stop_node(node)
                            print(node.name,"was stopped")
                            found=1
                    if found == 0:
                        print(name,": not found")
                        print(name,"was not stopped")
                
            else:
                found = 0
                name = names[0]
                for node in nodes:
                    if node.name == name:
                        print(node.name,": found") 
                        print("stopping",node.name)
                        driver_ec2.ex_stop_node(node)
                        print(node.name,"was stopped")
                        found=1
                if found == 0:
                    print(name,": not found")
                    print(name,"was not stopped")
            return
        else:
            print("not implemented")

