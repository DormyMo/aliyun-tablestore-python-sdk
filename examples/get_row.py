# -*- coding: utf8 -*-

from example_config import *
from ots2 import *
import time

table_name = 'OTSGetRowSimpleExample'

def create_table(ots_client):
    schema_of_primary_key = [('uid', 'INTEGER'), ('gid', 'INTEGER')]
    table_meta = TableMeta(table_name, schema_of_primary_key)
    table_options = TableOptions()
    reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
    ots_client.create_table(table_meta, table_options, reserved_throughput)
    print ('Table has been created.')

def delete_table(ots_client):
    ots_client.delete_table(table_name)
    print ('Table \'%s\' has been deleted.' % table_name)

def put_row(ots_client):
    primary_key = [('uid',1), ('gid',101)]
    attribute_columns = [('name','杭州'), ('growth',0.95), ('type','sub-provincial city'), ('postal code',310000), ('Alibaba', True), ('chengdu', False)]
    row = Row(primary_key, attribute_columns)
    condition = Condition(RowExistenceExpectation.EXPECT_NOT_EXIST) # Expect not exist: put it into table only when this row is not exist.
    consumed, return_row = ots_client.put_row(table_name, row, condition)
    print ('Write succeed, consume %s write cu.' % consumed.write)

def get_row(ots_client):
    primary_key = [('uid',1), ('gid',101)]
    columns_to_get = ['name', 'growth', 'type'] # given a list of columns to get, or empty list if you want to get entire row.

    cond = CompositeColumnCondition(LogicalOperator.AND)
    cond.add_sub_condition(SingleColumnCondition("growth", 0.9, ComparatorType.NOT_EQUAL))
    cond.add_sub_condition(SingleColumnCondition("name", '杭州', ComparatorType.EQUAL))

    consumed, return_row, next_token = ots_client.get_row(table_name, primary_key, columns_to_get, cond, 1)

    print ('Read succeed, consume %s read cu.' % consumed.read)

    print ('Value of primary key: %s' % return_row.primary_key)
    print ('Value of attribute: %s' % return_row.attribute_columns)
    for att in return_row.attribute_columns:
        print ('name:%s\tvalue:%s\ttimestamp:%d' % (att[0], att[1], att[2]))

def get_row2(ots_client):
    primary_key = [('uid',1), ('gid',101)]
    columns_to_get = []

    cond = CompositeColumnCondition(LogicalOperator.AND)
    cond.add_sub_condition(SingleColumnCondition("growth", 0.9, ComparatorType.NOT_EQUAL))
    cond.add_sub_condition(SingleColumnCondition("name", '杭州', ComparatorType.EQUAL))

    consumed, return_row, next_token = ots_client.get_row(table_name, primary_key, columns_to_get, cond, 1,
                                                          start_column = 'Alibaba', end_column = 'name')

    print ('Read succeed, consume %s read cu.' % consumed.read)

    print ('Value of primary key: %s' % return_row.primary_key)
    print ('Value of attribute: %s' % return_row.attribute_columns)


if __name__ == '__main__':
    ots_client = OTSClient(OTS_ENDPOINT, OTS_ID, OTS_SECRET, OTS_INSTANCE)
    try:
        delete_table(ots_client)
    except:
        pass
    create_table(ots_client)

    time.sleep(3) # wait for table ready
    put_row(ots_client)
    get_row(ots_client)
    get_row2(ots_client)
    delete_table(ots_client)
