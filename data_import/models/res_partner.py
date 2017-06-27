# -*- coding: utf-8 -*-

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    matricule = fields.Char(string='Matricule', size=8)
