# -*- coding: utf8 -*-

from example_config import *
from ots2 import *
import time

table_name = 'python_sdk_4'

def create_table(ots_client):
    schema_of_primary_key = [('gid', 'INTEGER'), ('uid', 'STRING')]
    table_meta = TableMeta(table_name, schema_of_primary_key)
    reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
    ots_client.create_table(table_meta, reserved_throughput)
    print 'Table has been created.'

def delete_table(ots_client):
    ots_client.delete_table(table_name)
    print 'Table \'%s\' has been deleted.' % table_name

def put_row(ots_client):
    primary_key = {'gid':1, 'uid':"101"}
    attribute_columns = {'name':'John', 'mobile':15100000000, 'address':'China', 'age':20}
    condition = Condition(RowExistenceExpectation.EXPECT_NOT_EXIST) # Expect not exist: put it into table only when this row is not exist.
    consumed, primary_key, attribute = ots_client.put_row(table_name, None, primary_key, attribute_columns)
    print u'Write succeed, consume %s write cu.' % consumed.write

def update_row(ots_client):
    primary_key = {'gid':1, 'uid':"101"}
    update_of_attribute_columns = {
        'PUT' : {'name':'David', 'address':'Hangkong'},
        'DELETE' : {'address':(None, 1488436949003)},
        'DELETE_ALL' : {'mobile':(None, None), 'age':(None, None)},
    }
    condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("age", 20, ComparatorType.EQUAL)) # update row only when this row is exist
    consumed, pk, attribute = ots_client.update_row(table_name, None, primary_key, update_of_attribute_columns) 
    print u'Update succeed, consume %s write cu.' % consumed.write

def get_row(ots_client):
    primary_key = {'gid':1, 'uid':"101"}
    columns_to_get = ['name', 'address', 'age'] # given a list of columns to get, or empty list if you want to get entire row.
    consumed, primary_key, attribute = ots_client.get_row(table_name, primary_key, columns_to_get, None, 1)
    print u'Read succeed, consume %s read cu.' % consumed.read

    print u'Value of attribute: %s' % attribute


if __name__ == '__main__':
    ots_client = OTSClient(OTS_ENDPOINT, OTS_ID, OTS_SECRET, OTS_INSTANCE)
    # create_table(ots_client)

    # time.sleep(3) # wait for table ready
    put_row(ots_client)
    print '#### row before update ####'
    get_row(ots_client)
    update_row(ots_client)
    print '#### row after update ####'
    get_row(ots_client)
    # delete_table(ots_client)

