# -*- coding: utf-8 -*-

from openerp import api, fields, models

class mrp_bom(models.Model):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'
    _description = 'bom_line_unit_cost'

    # champs non utilisé et perdu :
    bom_product_unit_cost = fields.Float(compute='_compute_bom_product_unit_cost', string="Prix unitaite")

    # champs calculant la sommes des lignes de bom (prix total par produit)
    bom_full_total_cost = fields.Float(compute='_bom_full_total_cost', string="Total Nomenclature")

    # champs calculant le coût de revient à l'unité
    bom_unit_cost = fields.Float(compute='_compute_bom_unit_cost', string="Coût de production à l'unité")

    @api.multi
    @api.depends('bom_line_ids.bom_total_cost')
    def _bom_full_total_cost(self):
        for rec in self:
            rec.bom_full_total_cost = sum(mrp_bom_line.bom_total_cost for mrp_bom_line in rec.bom_line_ids)

    @api.depends('bom_full_total_cost', 'product_qty')
    def _compute_bom_unit_cost(self):
        for rec in self:
            rec.bom_unit_cost = rec.bom_full_total_cost / rec.product_qty



