import sys
sys.path.append('./gen-py')

from core.db import *

from datahub import DataHub
from datahub.constants import *
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Server
'''

def construct_query_result(res):
  query_result = DHQueryResult(
      status = res['status'],
      row_count = res['row_count'],
      column_types = res['column_types'],
      column_names = res['column_names'],
      tuples = res['tuples'])

  return query_result


class DataHubHandler:
  def __init__(self):
    pass

  def get_version(self):
    return VERSION

  def connect(self, dh_con_params):  
    try:
      dh_database = DHDatabase()

      if dh_con_params.database:
        dh_database.name = dh_con_params.database.name

      con = Connection(db_name=dh_database.name)
      dh_con = DHConnection(database=dh_database)
      return dh_con
    except Exception, e:
      raise DHException(message=str(e))
    
  def open_database(self, dh_con, dh_db):  
    try:
      con = Connection(db_name=dh_db.name)
      dh_con.database = dh_db
      return dh_con
    except Exception, e:
      raise DHException(message=str(e))

  def list_databases(self, dh_con):
    try:
      con = Connection(db_name=dh_con.database.name)
      res = con.list_databases()
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def list_tables(self, dh_con):
    try:
      con = Connection(db_name=dh_con.database.name)
      res = con.list_tables()
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def execute_sql(self, dh_con, query, query_params=None):
    try:
      con = Connection(db_name=dh_con.database.name)
      res = con.execute_sql(query, query_params)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

handler = DataHubHandler()
  
processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting DataHub Server'
server.serve()