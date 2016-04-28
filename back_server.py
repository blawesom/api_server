# coding: utf-8

from bottle import Bottle
from bottle import run
from boto.ec2.regioninfo import EC2RegionInfo
from boto.vpc import VPCConnection
from ConfigParser import ConfigParser
import os

app = Bottle()


@app.route('/usage')
def get_usage():
    cpu = 0.0
    memory = 0.0
    conf_path = '{0}/config.ini'.format(os.path.dirname(os.path.realpath(__file__)))
    ows = init_connection(conf_path)
    if ows:
        itype_list = ows.get_all_instance_types()
        instance_list = [inst for inst in ows.get_only_instances() if inst.update() == 'running']
        for instance in instance_list:
            for itype in itype_list:
                if itype.name == instance.instance_type:
                    cpu += float(itype.vcpu)
                    memory += float(itype.memory)
        return {'cpu': cpu, 'memory': memory/1000000, 'nb_instance': len(instance_list)}
    else:
        return 'default in configuration file'


def init_connection(conf):
    # Load general configuration file
    cnf = ConfigParser()
    try:
        cnf.read(conf)
        region_os = EC2RegionInfo(endpoint=cnf.get('outscale', 'endpoint'))
        ows = VPCConnection(cnf.get('outscale', 'access_key'), cnf.get('outscale', 'secret_key'), region=region_os)
        return ows
    except Exception as e:
        print 'error in the configuration file: ', e
        return None


run(app, host='0.0.0.0', port=8000)
