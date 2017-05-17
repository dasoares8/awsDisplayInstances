import boto3
import argparse
from tabulate import tabulate

class InstanceInfo():

    def __init__(self, region='us-east-1', tag_key='Owner'):
        self.region = region
        self.tag_key = tag_key
        self.user_added_fields = []
        self.instance_table = []
        

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

    
    def populate_instance_info_table_data(self, ec2):
        # Just get all the instances there; no filtering involved
        instances = ec2.instances.filter(Filters=[])
        first_instance_iteration = True
        for inst in instances:
            tag_val=InstanceInfo.find_tag_and_return_value(self.tag_key, inst.tags)
            # value_list starts as default table config (based on requested tag name),
            # then appends user requested fields
            value_list = [inst.id, tag_val, inst.instance_type, inst.launch_time]
            for user_added_field in self.user_added_fields:
                if hasattr(inst, user_added_field):
                    user_added_val = getattr(inst, user_added_field)
                    value_list.append(user_added_val)
                else:
                    if first_instance_iteration:
                        print("\n{} is not an EC2 attribute; ignoring\n".format(user_added_field))
            first_instance_iteration = False
            self.instance_table.append(value_list)
        # Sort based on the tag's value
        self.instance_table.sort(key=lambda x: x[1])
        return


    def printInstanceTable(self):
        # initialize the default table headers, then tack on the user requested ones
        table_headers = ['Instance Id', self.tag_key, 'Instance Type', 'Launch Time']
        for i in self.user_added_fields:
            table_headers.append(i)
        print(tabulate(self.instance_table, headers=table_headers))


def main():
    instance_info = InstanceInfo()
    instance_info.init_with_arg_parser()
    ec2 = instance_info.init_ec2_resource()
    instance_info.populate_instance_info_table_data(ec2)
    
    # Data's fully prepared at this point; just print
    print("\nRegion: {}\n".format(instance_info.region))
    instance_info.printInstanceTable()

                    
if  __name__ =='__main__':
    main()
