# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Finition_mrp (models.Model):
    _name = 'finition_mrp'
    _order = 'name'

    id = fields.Integer(string='id')
    name = fields.Char(string='Nom',
                       required=True)
    active = fields.Boolean('Actif ?', default=True)

    # price = fields.Float('Prix', (6, 2))
