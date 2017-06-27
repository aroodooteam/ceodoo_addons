# -*- coding: utf-8 -*-
# !/usr/bin/python


from openerp import models, api, fields, exceptions, _
from datetime import datetime
import os
import csv
import timeit
# codeAg = cn.code_sa + code_gra
# import shutil
import logging
_logger = logging.getLogger(__name__)


# import sys  # , getopt
# import psycopg2
# import xmlrpclib

def splitList(arr, size):
    """
    Split long list in sublist
    """
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def addElementInTuple(arr, elt):
    """
    :param list arr: The list to manipulate
    arr format -> [(x,x,{}), (x,x,{}), (x,x,{})]
    :param dict elt: The element to insert
    """
    arrs = []
    for tpl in arr:
        tpl[2].update(elt)
        arrs.append(tpl)
    return arrs


class CsvLoader(models.Model):
    _name = 'csv.loader'
    _description = 'Load csv file'

    name = fields.Char(string='Name', required=True)
    csv_path = fields.Char(string='Full path to csv file', required=True)
    with_header = fields.Boolean(string='Header', help='Contain header')
    delimiter = fields.Char(string='Separator', default=',',
                            help='Specify the separator', required=True)
    map_data = fields.Char(string='Map',
                           help='Map is a dict that will be use to fit \
                           column in database')

    @api.multi
    def CheckProductCateg(self, name):
        if not name:
            raise exceptions.Warning(_('Error'), _('No Name Categ'))
        if name == 'BOISS':
            name = 'BOISSON'

        categ_obj = self.env['product.category']
        categ_id =  categ_obj.search([('name', '=', name)])
        if len(categ_id) > 1:
            raise exceptions.Warning(_('Error'), _('More than one product category with same name: %s' % name))
        return categ_id

    @api.multi
    def CheckProduct(self, ref):
        if not ref:
            raise exceptions.Warning(_('Error'), _('No reference'))

        product_obj = self.env['product.product']
        product_id =  product_obj.search([('default_code', '=', ref)])
        if len(product_id) > 1:
            raise exceptions.Warning(_('Error'), _('More than one product with same reference: %s' % ref))
        return product_id

    @api.multi
    def main_import_product(self):
        with open(self.csv_path, 'rb') as csv_count:
            total = csv.DictReader(csv_count, delimiter=str(self.delimiter))
            total = len(list(total))
        with open(self.csv_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=str(self.delimiter))
            for i, line in enumerate(reader):
                st = timeit.default_timer()
                _logger.info('=== line = %s ===' % line)
                product_id = self.CheckProduct(line.get('Ref'))
                categ_id = self.CheckProductCateg(line.get('categ'))
                vals = {
                    'list_price': line.get('pv', 0.0).replace(',', '.'),
                    'standard_price': line.get('pa', 0.0).replace(',', '.'),
                    'categ_id': categ_id.id,
                }
                product_id.write(vals)
                # _logger.info('=== read %d / %s ===' % (i+1, total))
        return True

    @api.multi
    def main_import_partner(self):
        with open(self.csv_path, 'rb') as csv_count:
            total = csv.DictReader(csv_count, delimiter=str(self.delimiter))
            total = len(list(total))
        with open(self.csv_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=str(self.delimiter))
            for i, line in enumerate(reader):
                st = timeit.default_timer()
                _logger.info('=== line = %s ===' % line)
        return True
