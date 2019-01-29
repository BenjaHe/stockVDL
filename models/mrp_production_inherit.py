from openerp import api, fields, models

class mrp_production(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    _description = 'bom_production_addons'


    description = fields.Char(string='Nom du travail', required=False, track_visibility='onchange', help='Nom du document produit.')
<<<<<<< HEAD
    move_lines = fields.One2many('stock.move', 'raw_material_production_id', 'Machin to Consume', readonly=False)
=======
    move_lines = fields.One2many('stock.move', 'raw_material_production_id', 'Machin to Consume', readonly=False)
>>>>>>> Mise à niveau de la Prod' avec le Dev du 29 janvier 2019.
