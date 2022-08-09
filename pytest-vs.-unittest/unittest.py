"""Unit Test용 모듈 (unittest 패키지 사용)."""
import unittest

import os
import sys
import re
import csv
import pyodbc
from datetime import datetime, timedelta

import yaml


def get_date_dict(targetdate):
    date_dict = {
        'year': datetime.strftime(targetdate, '%Y'),
        'month': datetime.strftime(targetdate, '%m'),
        'day': datetime.strftime(targetdate, '%d'),
        'date': datetime.strftime(targetdate, '%Y-%m-%d')
    }
    return date_dict

class Something():

    def __init__(self):
        self.name = 5

    def get_some(self):
        return self.name

    def set_some(self, num):
        self.name = num

    def print_some(self):
        print(self.name)



class CustomTests(unittest.TestCase):

    config = None

    def setUp(self):
        """전처리(각 테스트 공통)."""
        self.config = get_config('test_config')
        # print('\n============== UnitTest Begins ================')

    def tearDown(self):
        """후처리(각 테스트 공통)."""
        # print('============== UnitTest Ends ==================')




    """
    def test_run_config(self):
        get_config('config_mua2tw_alpha.yml')
    def test_get_config(self):
        self.assertEqual(get_config('test_config.yml')['test'], 'pytest')

    def test_string(self):
        driver, server, db, userid, passwd = '1', '2', '3', '4', '5'
        gizon = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+db+';UID='+userid+';PWD='+passwd
        conn_info = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.\
                format(driver, server, db, userid, passwd)

        self.assertEqual(gizon, conn_info)

    def test_get_config_alpha(self):

        t_tables = config['tables']
        print(t_tables[0])
        self.assertEqual(type(t_tables), type(tables))
        self.assertEqual(type(t_tables[0]), type(tables[0]))

        self.assertEqual(t_tables, tables)
        self.assertEqual(t_tables[0], tables[0])

    def test_get_date_dict(self):
        targetdate = datetime.now()

    """



#if __name__ == '__main__':



