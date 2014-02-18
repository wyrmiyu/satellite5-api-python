#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# satellite_api is a helper module. This module contains a class called
# SatelliteConnector, which aims to make interaction with Red Hat Satellite 
# XML-RPC API more convenient.
#
# Written by: Pekka Wallendahl (pwallend@redhat.com)
# License: GPLv3+, for more info see: http://www.gnu.org/licenses/gpl-3.0.html
# 
#    Copyright (C) 2013-2014  Pekka Wallendahl
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
import xmlrpclib
import ConfigParser
aamen
class SatelliteConnector:

    def __init__(   self, 
                    config_file='config.cfg', 
                    satellite_server='satellite.example.com'
    ):
        self.__api_client = None
        self.__session_key = None
        
        try:
            config = ConfigParser.ConfigParser()
            config.read(config_file)

            self.__api_url = 'http://%s/rpc/api' % satellite_server
            self.__login = config.get(satellite_server, 'login')
            self.__password = config.get(satellite_server, 'password')
aamen
            self.__api_client, self.__session_key = self.__open_connection()
        except:
            raise
    
    def __del__(self):
        try:
            self.__close_connection()
        except:
            raise           
       
    def __str__(self):
        return("%s.__api_client = %s\n" \
               "%s.__session_key = %s\n" % (
                                            self.__class__.__name__,
                                            self.__api_client,
                                            self.__class__.__name__,
                                            self.__session_key
                                         )
        )
        
    # Opens connection to satellite
    #
    def __open_connection(self):
        api_client = None
        session_key = None
        try:
            api_client = xmlrpclib.Server(self.__api_url, verbose=0)
            session_key = api_client.auth.login(self.__login,
                                              self.__password)
            if not session_key:
                raise Exception("Can't login to satellite.")
        except:
            raise
        return api_client, session_key

    # Closes connection to satellite (if any)
    #
    def __close_connection(self):
        try:
            if (self.__session_key):
                self.__api_client.auth.logout(self.__session_key)
        except xmlrpclib.Fault:
            # session already closed
            pass

    def call_api(self, method=None, args=None):
        if method is None:
            raise Exception('No method provided for api call')
        try:
            api_call = getattr(self.__api_client, method)
            if args is None:
                return api_call(self.__session_key)
            elif type(args) is tuple:
                return api_call(self.__session_key, *args)
            elif type(args) is str or int or list:
                return api_call(self.__session_key, args)
            else:
                e = "Bad object type '%s' for arg: %s\n" % (type(args), args)
                e = e + "Supported object types are 'str' and 'tuple'"
                raise TypeError(e)
        except:
            raise

# EOF
