# -*- coding: utf-8 -*-

from openerp import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class mail_mail(models.Model):
    _name = 'mail.mail'
    _inherit = 'mail.mail'

    @api.multi
    def _postprocess_sent_message(self, mail, mail_sent=True):
        for rec in self:
            if mail.model == 'purchase.order':
                obj = self.env['purchase.order'].browse( mail.res_id)
                if obj.state == 'validation_1':
                    _logger.info('On passe dans le méthode spécifique de mail_mail dans StockVDL')
                    obj.button_approve()
                    _logger.info('On est passé par le bouton_approve')
            return super(mail_mail, rec)._postprocess_sent_message(mail=mail, mail_sent=mail_sent)