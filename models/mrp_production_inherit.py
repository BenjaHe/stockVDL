from openerp import api, fields, models

class mrp_production(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    _description = 'bom_production_addons'


    description = fields.Char(string='Nom du travail', required=False, track_visibility='onchange', help='Nom du document produit.')
    move_lines = fields.One2many('stock.move', 'raw_material_production_id', 'Machin to Consume', readonly=False)

