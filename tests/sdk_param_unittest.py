#!/bin/python
# -*- coding: utf8 -*-

import logging
import unittest
import exceptions

from ots2.client import *
from ots2.metadata import *
from ots2.error import *
from lib.mock_connection import MockConnection
from lib.test_config import *

class SDKParamTest(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger('test')
        handler=logging.FileHandler("test.log")
        formatter = logging.Formatter("[%(asctime)s]    [%(process)d]   [%(levelname)s] " \
                    "[%(filename)s:%(lineno)s]   %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        OTSClient.connection_pool_class = MockConnection
        self.ots_client = OTSClient(OTS_ENDPOINT, OTS_ID, OTS_SECRET, OTS_INSTANCE)

    def tearDown(self):
        pass

    def test_list_table(self):
        try:
            self.ots_client.list_table('one');
            self.assertTrue(False)
        except TypeError:
            pass

    def test_create_table(self):
        try:
            self.ots_client.create_table('one', 'two', 'three')
            self.assertTrue(False)
        except OTSClientError:
            pass

        try:
            table_meta = TableMeta('test_table', ['PK1', 'STRING'])
            capacity_unit = CapacityUnit(10, 10)
            self.ots_client.create_table(table_meta, TableOptions(), capacity_unit)
            self.assertTrue(False)
        except OTSClientError:
            pass

        try:
            table_meta = TableMeta('test_table', [('PK1', 'STRING'), ('PK2', 'INTEGER')])
            capacity_unit = CapacityUnit(10, None)
            self.ots_client.create_table(table_meta, TableOptions(), capacity_unit)
            self.assertTrue(False)
        except OTSClientError:
            pass

        try:
            capacity_unit = CapacityUnit(10, 10)
            self.ots_client.create_table('test_table', TableOptions(), capacity_unit)
            self.assertTrue(False)
        except OTSClientError:
            pass

        try:
            table_meta = TableMeta('test_table', [('PK1', 'STRING'), ('PK2', 'INTEGER')])
            self.ots_client.create_table(table_meta, TableOptions(), [1, 2])
            self.assertTrue(False)
        except OTSClientError:
            pass

    def test_delete_table(self):
        try:
            self.ots_client.delete_table('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            capacity_unit = CapacityUnit(10, 10)
            self.ots_client.delete_table(capacity_unit)
            self.assertTrue(False)
        except OTSClientError:
            pass

    def test_update_table(self):
        try:
            self.ots_client.update_table('one', 'two', 'three')
            self.assertTrue(False)
        except:
            pass

        try:
            self.ots_client.update_table('test_table', TableOptions(), (10, 10))
            self.assertTrue(False)
        except OTSClientError:
            pass

        try:
            capacity_unit = CapacityUnit(None, None)
            self.ots_client.update_table('test_table', TableOptions(),capacity_unit)
            self.assertTrue(False)
        except OTSClientError:
            pass

    def test_describe_table(self):
        try:
            self.ots_client.describe_table('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            response = self.ots_client.describe_table(['test_table'])
            self.assertTrue(False)
        except OTSClientError:
            pass

    def test_put_row(self):
        try:
            self.ots_client.put_row('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            primary_key = [('PK1','hello'), ('PK2',100)]
            attribute_columns = [('COL1','world'), ('COL2',1000)]
            condition = Condition('InvalidCondition')
            consumed = self.ots_client.put_row('test_table', condition, primary_key, attribute_columns)
            self.assertTrue(False)
        except OTSClientError:
            pass
    
        try:
            primary_key = [('PK1','hello'), ('PK2',100)]
            attribute_columns = [('COL1','world'), ('COL2',1000)]
            consumed = self.ots_client.put_row('test_table', [RowExistenceExpectation.IGNORE], primary_key, attribute_columns)
            self.assertTrue(False)
        except:
            pass
    
        try:
            condition = Condition(RowExistenceExpectation.IGNORE)
            consumed = self.ots_client.put_row('test_table', condition, 'primary_key', 'attribute_columns')
            self.assertTrue(False)
        except:
            pass
    
    def test_get_row(self):
        try:
            self.ots_client.get_row('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            consumed, resp_pks, resp_attribute_columns = self.ots_client.get_row('test_table', 'primary_key', 'columns_to_get')
            self.assertTrue(False)
        except:
            pass

    def test_update_row(self):
        try:
            self.ots_client.update_row('one', 'two', 'three')
            self.assertTrue(False)
        except:
            pass

        try:
            condition = Condition(RowExistenceExpectation.IGNORE)
            consumed = self.ots_client.update_row('test_table', condition, [('PK1', 'STRING'), ('PK2', 'INTEGER')], 'update_of_attribute_columns')
            self.assertTrue(False)
        except OTSClientError as e:
            pass

        try:
            condition = Condition(RowExistenceExpectation.IGNORE)
            consumed = self.ots_client.update_row('test_table', condition, [('PK1', 'STRING'), ('PK2', 'INTEGER')], [('ncv', 1)])
            self.assertTrue(False)
        except OTSClientError as e:
            pass
            
        try:
            condition = Condition(RowExistenceExpectation.IGNORE)
            consumed = self.ots_client.update_row('test_table', condition, [('PK1', 'STRING'), ('PK2', 'INTEGER')], {'put' : []})
            self.assertTrue(False)
        except OTSClientError as e:
            pass
            
        try:
            condition = Condition(RowExistenceExpectation.IGNORE)
            consumed = self.ots_client.update_row('test_table', condition, [('PK1', 'STRING'), ('PK2', 'INTEGER')], {'delete' : []})
            self.assertTrue(False)
        except OTSClientError as e:
            pass
 
    def test_delete_row(self):
        try:
            self.ots_client.delete_row('one', 'two', 'three', 'four')
            self.assertTrue(False)
        except:
            pass

        try:
            condition = Condition(RowExistenceExpectation.IGNORE)
            consumed = self.ots_client.delete_row('test_table', condition, 'primary_key')
            self.assertTrue(False)
        except:
            pass

    def test_batch_get_row(self):
        try:
            self.ots_client.batch_get_row('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            response = self.ots_client.batch_get_row('batches')
            self.assertTrue(False)
        except OTSClientError:
            pass

    def test_batch_write_row(self):
        try:
            self.ots_client.batch_write_row('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            response = self.ots_client.batch_write_row('batches')
            self.assertTrue(False)
        except OTSClientError:
            pass

        batch_list = [('test_table')]
        try:
            response = self.ots_client.batch_write_row(batch_list)
            self.assertTrue(False)
        except OTSClientError:
            pass

        batch_list = [{'table_name':None}]
        try:
            response = self.ots_client.batch_write_row(batch_list)
            self.assertTrue(False)
        except OTSClientError:
            pass

        batch_list = [{'table_name':'abc', 'put':None}]
        try:
            response = self.ots_client.batch_write_row(batch_list)
            self.assertTrue(False)
        except OTSClientError:
            pass

        batch_list = [{'table_name':'abc', 'put':['xxx']}]
        try:
            response = self.ots_client.batch_write_row(batch_list)
            self.assertTrue(False)
        except OTSClientError:
            pass

        batch_list = [{'table_name':'abc', 'Put':[]}]
        try:
            response = self.ots_client.batch_write_row(batch_list)
            self.assertTrue(False)
        except OTSClientError:
            pass

        batch_list = [{'table_name':'abc', 'Any':[]}]
        try:
            response = self.ots_client.batch_write_row(batch_list)
            self.assertTrue(False)
        except OTSClientError:
            pass

    def test_get_range(self):
        try:
            self.ots_client.get_range('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            start_primary_key = [('PK1','hello'),('PK2',100)]
            end_primary_key = [('PK1',INF_MAX),('PK2',INF_MIN)]
            columns_to_get = ['COL1','COL2']
            response = self.ots_client.get_range('table_name', 'InvalidDirection', 
                        start_primary_key, end_primary_key, 
                        columns_to_get, limit=100, max_version=1
            )
            self.assertTrue(False)
        except OTSClientError:
            pass

        try:
            start_primary_key = ['PK1','hello','PK2',100]
            end_primary_key = [('PK1',INF_MAX), ('PK2',INF_MIN)]
            columns_to_get = ['COL1', 'COL2']
            response = self.ots_client.get_range('table_name', 'FORWARD', 
                        start_primary_key, end_primary_key, 
                        columns_to_get, limit=100, max_version=1
            )
            self.assertTrue(False)
        except:
            pass

        try:
            start_primary_key = [('PK1','hello'),('PK2',100)]
            end_primary_key = [('PK1',INF_MAX), ('PK2',INF_MIN)]
            columns_to_get = ['COL1', 'COL2']
            response = self.ots_client.get_range('table_name', 'FORWARD', 
                        start_primary_key, end_primary_key, 
                        columns_to_get, limit=100, max_version=-1
            )
            self.assertTrue(False)
        except:
            pass


        try:
            response = self.ots_client.get_range('table_name', 'FORWARD', 
                        'primary_key', 'primary_key', 'columns_to_get', 100)
            self.assertTrue(False)
        except:
            pass

    def test_xget_range(self):
        try:
            self.ots_client.xget_range('one', 'two')
            self.assertTrue(False)
        except:
            pass

        try:
            iter = self.ots_client.xget_range('one', 'two', 'three', 'four', 'five', 'six', 'seven')
            iter.next()
            self.assertTrue(False)
        except OTSClientError:
            pass

    def assert_client_error(self, error, message):
        self.assertEqual(str(error), message)

    def test_condition(self):
        Condition(RowExistenceExpectation.IGNORE)
        Condition(RowExistenceExpectation.EXPECT_EXIST)
        Condition(RowExistenceExpectation.EXPECT_NOT_EXIST)

        try:
            cond = Condition('errr')
            self.assertTrue(False)
        except OTSClientError, e:
            self.assertEqual("Expect input row_existence_expectation should be one of ['RowExistenceExpectation.IGNORE', 'RowExistenceExpectation.EXPECT_EXIST', 'RowExistenceExpectation.EXPECT_NOT_EXIST'], but 'errr'", str(e))

        try:
            cond = Condition(RowExistenceExpectation.IGNORE, "")
            self.assertTrue(False)
        except OTSClientError, e:
            self.assertEqual("The input column_condition should be an instance of ColumnCondition, not str", str(e))

        try:
            cond = Condition(RowExistenceExpectation.IGNORE, RelationCondition("", "", ""))
            self.assertTrue(False)
        except OTSClientError, e:
            self.assertEqual("Expect input comparator should be one of ['ComparatorType.EQUAL', 'ComparatorType.NOT_EQUAL', 'ComparatorType.GREATER_THAN', 'ComparatorType.GREATER_EQUAL', 'ComparatorType.LESS_THAN', 'ComparatorType.LESS_EQUAL'], but ''", str(e))


    def test_column_condition(self):
        cond = RelationCondition("uid", 100, ComparatorType.EQUAL)
        self.assertEqual(ColumnConditionType.SINGLE_COLUMN_CONDITION, cond.get_type())
        
        cond = CompositeCondition(LogicalOperator.AND)
        self.assertEqual(ColumnConditionType.COMPOSITE_COLUMN_CONDITION, cond.get_type())
       

    def test_relation_condition(self):
        RelationCondition("uid", 100, ComparatorType.EQUAL)
        RelationCondition("uid", 100, ComparatorType.NOT_EQUAL)
        RelationCondition("uid", 100, ComparatorType.GREATER_THAN)
        RelationCondition("uid", 100, ComparatorType.GREATER_EQUAL)
        RelationCondition("uid", 100, ComparatorType.LESS_THAN)
        RelationCondition("uid", 100, ComparatorType.LESS_EQUAL)

        try:
            cond = RelationCondition("uid", 100, "")
            self.assertTrue(False)
        except OTSClientError, e:
            self.assertEqual("Expect input comparator should be one of ['ComparatorType.EQUAL', 'ComparatorType.NOT_EQUAL', 'ComparatorType.GREATER_THAN', 'ComparatorType.GREATER_EQUAL', 'ComparatorType.LESS_THAN', 'ComparatorType.LESS_EQUAL'], but ''", str(e))
       
        try:
            cond = RelationCondition("uid", 100, ComparatorType.LESS_EQUAL, "True")
            self.assertTrue(False)
        except OTSClientError, e:
            self.assertEqual("The input pass_if_missing should be an instance of Bool, not str", str(e))
       

    def test_composite_condition(self):
        CompositeCondition(LogicalOperator.NOT)
        CompositeCondition(LogicalOperator.AND)
        CompositeCondition(LogicalOperator.OR)

        try:
            cond = CompositeCondition("")
            self.assertTrue(False)
        except OTSClientError, e:
            self.assertEqual("Expect input combinator should be one of ['LogicalOperator.NOT', 'LogicalOperator.AND', 'LogicalOperator.OR'], but ''", str(e))
 

if __name__ == '__main__':
    unittest.main()
