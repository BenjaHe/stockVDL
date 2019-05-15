# -*- coding: utf-8 -*-
{
    'name': "Stock VDL",

    'summary': """
        Extention du module Stock Picking et Res.Partner pour les besoins de l'Economat.""",

    'description': """
        Le module modifie les modules res.partner et stock pour ajouter un commentaire pour la livraison (Inventaire) 
        et les informations liées au budget du client (Contacts).

    """,

    'author': "Roland Neyrinck",
    'website': "",

    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_stock', 'sale', 'purchase', 'stock', 'account','website', 'website_sale','payment','payment_transfer', 'mrp','website','website_portal_sale'],

    'data': ['security/bdc_custom_security.xml',
             'security/ir.model.access.csv',
             'views/magasin_views.xml',
             'reports/report_economat.xml',
             'views/account_total.xml',
             'views/payment_acquirer_addons.xml',
             'views/view_order_form_acquirer_inherited.xml',
             'views/bom_line_custom.xml',
             'views/sale_order_view_inherit.xml',
             'views/web_customer_informations.xml',
             'views/partner_addons.xml',
             'views/bdc_addons.xml',
             'views/purchase_order_view_inherited.xml',
             'views/mrp_production_form_inherit.xml',
             'views/finition_mrp_views.xml',
             'reports/report_purchase_order_custom_vdl.xml',
             'views/product_template_inherit.xml'
             ],

}

# 'views/purchase_order_view_inherited.xml'