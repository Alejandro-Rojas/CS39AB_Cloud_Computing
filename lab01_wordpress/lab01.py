# CS39AB - Cloud Computing - Summer 2021 
# Instructor: Thyago Mota
# Description: lab01
# Members: Alejandro Rojas 

import boto3
import time

# us-west-1(N.California)


if __name__ == "__main__":
    # Step 1: obtain the id of the default VPC
    client = boto3.client('ec2')
    vpcs = client.describe_vpcs()['Vpcs']
    default_vpc_id = None
    for vpc in vpcs:
        if vpc['IsDefault']:
            default_vpc_id = vpc['VpcId']
            break
    if not default_vpc_id:
        print('There is not default VPC!')
        exit(1)
    print('Default VPC id is ' + default_vpc_id)


    # Step 2: obtain the id of the subnet that has the 
        # property MapPublicIpOnLaunch(Public Subnet) set to true
    filter = {
        'Name': 'vpc-id',
        'Values': [ default_vpc_id ]
    }
    subnets = client.describe_subnets( Filters = [filter])['Subnets']
    public_subnet_id = None
    for subnet in subnets:
        if subnet['MapPublicIpOnLaunch']:
            public_subnet_id = subnet['SubnetId']
            break 
    if not public_subnet_id:
        print('There is no public subnet!')
        exit(1)
    print('Public subnet id is ' + public_subnet_id)


    # Step 3: Create a security group named lab01
    sg_id = client.create_security_group(
        GroupName = 'lab01',
        Description = 'lab01',
        VpcId = default_vpc_id)['GroupId']
    print('Security group was created with id ' + sg_id)


    # Step 4: add an ingress rule to security group
        # add with inbound ssh (port 22), http (port 80), 
        # and mysql/mariadb (port 3306) traffic enabled from anywhere.
    # port 22
    ip_permission_ssh = {
        'FromPort': 22,
        'ToPort':   22,
        'IpProtocol': 'tcp',
        'IpRanges': [ 
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'ssh access to ec2 instance from anywhere!'
            }
        ]
    }

    # port 80
    ip_permission_http = {
        'FromPort': 80,
        'ToPort':   80,
        'IpProtocol': 'tcp',
        'IpRanges': [ 
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'http access to ec2 instance from anywhere!'
            }
        ]
    } 

    # port 3306
    ip_permission_mysql = {
        'FromPort': 3306,
        'ToPort':   3306,
        'IpProtocol': 'tcp',
        'IpRanges': [ 
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'mysql access to ec2 instance from anywhere!'
            }
        ]
    } 

    client.authorize_security_group_ingress(
        GroupId = sg_id, 
        IpPermissions = [ ip_permission_ssh, ip_permission_http, ip_permission_mysql ]
    )   

    # Step 5: Launch ec2 instance 
    user_data = '''#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y httpd mariadb-server
sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl start mariadb
sudo systemctl enable mariadb
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cp wordpress/wp-config-sample.php wordpress/wp-config.php'''
    instance_id = client.run_instances(
        ImageId = 'ami-0b2ca94b5b49e0132',
        MinCount = 1, 
        MaxCount = 1,
        InstanceType = 't2.micro',
        SecurityGroupIds = [ sg_id ],
        SubnetId = public_subnet_id, 
        KeyName = 'cs39ab',
        UserData = user_data
    )['Instances'][0]['InstanceId']
    print('Instance id is ' + instance_id)

    # Display the public IP of the EC2 instance before it finishes. (no wait time)
    print('Waiting for instance to be launched...')
    time.sleep(30)
    ip_address = client.describe_instances(
        InstanceIds = [ instance_id ]
    )['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(ip_address)