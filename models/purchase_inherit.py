# -*- coding: utf-8 -*-

from openerp import api, fields, models

class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _description = "Purchase Order Custom Workflow"

    # VALUES = [('validation_1', 'Imputation comptable'),
    #           ('validation_2', 'Validation deuxième niveau')]
    #
    # state = fields.Selection(selection_add=VALUES)

    state = fields.Selection([
        ('draft', 'Draft PO'),
        ('sent', 'RFQ Sent'),
        ('validation_1', 'BdC à envoyer'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    article_budgetaire = fields.Char('Article budgétaire', required=True, track_visibility='onchange')
    num_engagement = fields.Char('Numero engagement', required=True, track_visibility='onchange')

    @api.multi
    def action_po_send(self):
#        for rec in self:
#            rec.write({'state': 'purchase'})
        res = self.send_mail_template()
        return res

    @api.multi
    def action_to_validation_1(self):
        self.write({'state': 'validation_1'})
        return {}

    @api.multi
    def send_mail_template(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'purchase', 'email_template_edi_purchase')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'purchase.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment'
        })
        res = {
            'name': ('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        return res

