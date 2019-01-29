# -*- coding: utf-8 -*-

from openerp import api, fields, models

class mrp_bom_line(models.Model):
    _name = 'mrp.bom.line'
    _inherit = 'mrp.bom.line'
    _description = 'bom_line_cost'

    bom_product_cost = fields.Float(string="Unit Cost", related="product_id.standard_price")

    bom_total_cost = fields.Float(compute="total_cost", string="Total cost by product")

    @api.one
    def total_cost(self):
        for rec in self:
            rec.bom_total_cost = self.bom_product_cost * self.product_qty
