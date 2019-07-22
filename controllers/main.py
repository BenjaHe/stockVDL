# -*- coding: utf-8 -*-
import datetime

from openerp import http
from openerp.exceptions import AccessError
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.website_portal.controllers.main import website_account


class website_account(website_account):

    @http.route(['/my/home'], type='http', auth="user", website=True)
    def company_details(self, **kw):
        companies = http.request.env['res.company'].sudo().search([])
        return http.request.render("website_portal_sale.orders_followup", {
            'companies': companies})


class CheckoutComment(website_sale):

    def checkout_values(self, data=None):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        sale_order_obj = registry.get('sale.order')
        if data:
            current_order = request.website.sale_get_order(context=context)
            sale_order_obj.write(cr, SUPERUSER_ID, [current_order.id],{'customer_comment_num_engagement': data.get('customer_comment_num_engagement', None),
                                                                       'customer_comment_num_article': data.get('customer_comment_num_article', None),
                                                                       'date_livraison_souhaite': data.get('date_livraison_souhaite', None)},
                                                                        context=context)
        return super(CheckoutComment, self).checkout_values(data)