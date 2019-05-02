from openerp import api, fields, models

class mrp_production(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    _description = 'bom_production_addons'

    description = fields.Char(string='Nom du travail', required=False, track_visibility='onchange',
                              help='Nom du document produit.')
    client = fields.Many2one(comodel_name='res.partner',
                             string='Client',
                             help='Personne demandant le travail')

    move_lines = fields.One2many('stock.move', 'raw_material_production_id', 'Machin to Consume', readonly=False)

    livrer = fields.Boolean(string='Doit ête livre ?', required=False, default=False)
    prevenir = fields.Boolean(string='Le client vient chercher ?', required=False, default=False,
                              help="Le client se charge de venir chercher le travail. Il faut le prévenir qu'il peut venir le chercher.")

    mo_cost = fields.Float(compute="_mo_cost", string="Coût de production", required=False)
    finition_ids = fields.Many2many(comodel_name='finition_mrp',
                                    string='Finitions')
    invoice_id = fields.Many2one('account.invoice', 'Facture', readonly=True, required=False)

    @api.multi
    def _mo_cost(self):
        for rec in self:
            rec.mo_cost = sum(stock_move.stock_move_cost for stock_move in rec.move_lines2)

    @api.multi
    def _create_invoice(self):
        for rec in self:
            invoice = self.env['account.invoice'].create({
                'name': name,
                'partner_id': rec.commanditaire.id,
                'amount_total': rec.mo_cost,
            })
            rec.invoice_id = invoice


class stock_move(models.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'
    _description = 'stock_move_addons'

    stock_move_cost = fields.Float(compute="_stock_move_cost", string="Total cost by product")

    # champ_bidon = fields.Char(string="Champs bidon", required=False)

    @api.multi  # Déprécié et déconseillé au profit de @api.multi... Mais je dis ça juste pcq je l'ai lu hein ;-)
    def _stock_move_cost(self):
        for rec in self:
            rec.stock_move_cost = rec.price_unit * rec.product_uom_qty
