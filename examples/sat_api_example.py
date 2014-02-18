#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# The purpose of this script is to provide a simple tutorial about how to
# use Red Hat Satellite v. 5.6 API with Python and a satellite_api module.
#
# In this tutorial we play with SatelliteConnector and it's call_api -method.
# The script is not trying to do anything fancy, just showing you different
# ways to use the API.
#
# Written by: Pekka Wallendahl (pwallend@redhat.com)
# License: GPLv3+, for more info see: http://www.gnu.org/licenses/gpl-3.0.html
#
# Import the helper class from satellite_api.py:
from satellite_api import SatelliteConnector

# Import pretty print module in order to have nicer output for dumps:
import pprint
dump = pprint.PrettyPrinter(indent=2)

# SatelliteConnector reads username and password from config-file and
# gets the satellite hostname as an arguent. 
# Define location of config-file and the hostname

CONFIG_FILE = '/path/to/sat_api_example.cfg'
SATELLITE_HOSTNAME = 'satellite.example.com'

# Define object to use as your API
try:
    sat = SatelliteConnector(config_file=CONFIG_FILE, 
                             satellite_server=SATELLITE_HOSTNAME)
except:
    raise

# Your object should now be initialized with a session cookie for 
# satellite API, which you can try to use with 'call_api' method.

# EXAMPLE: Get all your systems with their IDs

try:
    # Retrive list of system names from API. With no arguments, 
    # the used API method is given as a single string for call_api() method.
    list_of_systems = sat.call_api('system.listSystems')
except:
    raise

# From Satellite API documentation we can see that following data
# structure is returned:
# * array:
#   * struct - system (essentially this means dictionary hash)
#       * int 'id'
#       * string 'name'
#       * date Time.iso8601 'last_checkin'
# So this is an array of dictionary hashes, where each hash contains
# information of one system

# Define dictionary hash for key-value pairs, we are using system names
# as keys and set their ids as values.
system_id_dict = {}

# Define array-list for system ids
system_id_list = []

# Loop over the list_of_systems and assing system ids to system_id_dict and
# to system_id_list
for sys_dict in list_of_systems:
    sys_id = sys_dict['id']
    sys_name = sys_dict['name']
    system_id_dict[sys_name] = sys_id
    system_id_list.append(sys_id)

# To print out particular system id you can try:
print(system_id_dict['replaceme.example.com'])

# Now lets try to print a dump of large python object that contains details
# from satellite systems. In this time as we have to pass the system_id_list
# as an argumet for API method listActiveSystemsDetails, we have to define for
# call_api() which of the two is the API method and which one is the list
# that is passed to API as an argument.
try:
    system_info = sat.call_api( method='system.listActiveSystemsDetails',
                                args=system_id_list)
except:
    raise

# Dump the retrived data structure with pretty print
dump.pprint(system_info)

# If we need to give multiple arguments to use with any API method, we have to
# construct a tuple from those arguments and give that tuple to call_api().
# call_api() reads the tuple from beginning and passes each item as a separate
# argument for the actual Satellite API method.
#
# EXAMPLE: Check if a system has package bash-4.1.2-15.el6_4 installed on it. 
# To get this we have to pass four arguments, namely: system id, package name,
# package version and package release, to API method system.isNvreInstalled 
# (nvre stands for: name-version-release)
try:
    sys_id = system_id_dict['test.example.com']
    args = (sys_id, 'bash', '4.1.2', '15.el6_4')  # args = (..) is a tuple
    pkg_info = sat.call_api(method='system.isNvreInstalled', args=args)
except:
    raise

# prints 1 if pkg is installed and 0 if not.
print("bash-4.1.2-15.el6_4 installed: %s" % (pkg_info)) 

# EOF
