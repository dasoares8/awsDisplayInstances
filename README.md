# awsDisplayInstances
Python script to display a table of your EC2 instances in a specific region.

This script was written and tested with Python 3.4.3

Required Python modules (see requirements.txt):
- boto3
- argparse
- tabulate

usage: awsDisplayInstances.py [-h] [--region REGION] [--tagkey TAGKEY]
                                [--addfields [ADDFIELDS [ADDFIELDS ...]]]

list all EC2 instances in any single region, sorted by the value of a tag

optional arguments:
  -h, --help            show this help message and exit
  --region REGION       region to list instances from; default is us-east-1
  --tagkey TAGKEY       tag key to list and sort output; default is Owner
  --addfields [ADDFIELDS [ADDFIELDS ...]]
                        additional EC2 instance fields to be added to the
                        table; separate each with a space
                        
example output:
(venv) C:\>python awsDisplayInstances.py --addfields image_id subnet_id private_ip_address

Region: us-east-1

Instance Id          Owner        Instance Type    Launch Time                image_id      subnet_id        private_ip_address
-------------------  -----------  ---------------  -------------------------  ------------  ---------------  --------------------
i-0aea098495f9d1106  UbuntuChief  t2.micro         2017-05-12 21:54:56+00:00  ami-80861296  subnet-5e82f017  172.31.2.222
i-0ef30479a547a5d52  unknown      t2.micro         2017-03-27 14:48:47+00:00  ami-0b33d91d  subnet-9a0084c1  172.31.27.86
i-04a4dddb39a892dc1  unknown      t2.micro         2017-01-03 16:20:05+00:00  ami-9be6f38c  subnet-9a0084c1  172.31.16.194
