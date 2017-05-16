import boto3
import argparse
from tabulate import tabulate

class InstanceInfo():

    def __init__(self, region='us-east-1', tag_key='Owner'):
        self.region = region
        self.tag_key = tag_key
        self.user_added_fields = []
        
    # Given a tag_name to find in a tag_list, return the value if there; if not then 'unknown' per requirements
    @staticmethod
    def find_tag_and_return_value(tag_key, tag_list):
        for tag in tag_list:
            if tag['Key'] == tag_key:
                return tag['Value']
            return 'unknown'

    # populate the instance with information passed from the user
    def init_with_arg_parser(self):
        parser = argparse.ArgumentParser(description="list all EC2 instances in any single region, sorted by the value of a tag")
        parser.add_argument("--region", help="region to list instances from; default is us-east-1")
        parser.add_argument("--tagkey", help="tag key to list and sort output; default is Owner")
        parser.add_argument("--addfields", nargs='*',
                            help="additional EC2 instance fields to be added to the table; separate each with a space")
        args = parser.parse_args()
        if args.region:
            self.region = args.region
        if args.tagkey:
            self.tag_key = args.tagkey
        if args.addfields:
            for field in args.addfields:
                self.user_added_fields.append(field)


    def init_ec2_resource(self):
        return boto3.resource(
            'ec2',
            region_name=self.region
#            aws_access_key_id='ABC123',
#            aws_secret_access_key='DEF456'
        )
 
        
    def get_instance_info_table_data(self, ec2):
        # Just get all the instances there; no filtering involved
        instances = ec2.instances.filter(Filters=[])
        instance_list = []
        for inst in instances:
            tag_val=InstanceInfo.find_tag_and_return_value(self.tag_key, inst.tags)
            # value_list starts as default table config (based on requested tag name),
            # then appends user requested fields
            value_list = [inst.id, tag_val, inst.instance_type, inst.launch_time]
            for user_added_field in self.user_added_fields:
                user_added_val = getattr(inst, user_added_field)
                value_list.append(user_added_val)
            instance_list.append(value_list)
        # Sort based on the tag's value
        instance_list.sort(key=lambda x: x[1])
        return instance_list

    def printInstanceTable(self, instance_list):
        # initialize the default table headers, then tack on the user requested ones
        table_headers = ['Instance Id', self.tag_key, 'Instance Type', 'Launch Time']
        for i in self.user_added_fields:
            table_headers.append(i)
        print(tabulate(instance_list, headers=table_headers))


def main():
    instance_info = InstanceInfo()
    instance_info.init_with_arg_parser()
    ec2 = instance_info.init_ec2_resource()
    instance_table = instance_info.get_instance_info_table_data(ec2)
    
    # Data's fully prepared at this point; just print
    print("\nRegion: {}\n".format(instance_info.region))
    instance_info.printInstanceTable(instance_table)

                    
if  __name__ =='__main__':
    main()
