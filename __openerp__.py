# -*- coding: utf-8 -*-
{
    'name': "Stock VDL",

    'summary': """
        Extention du module Stock Picking pour pouvoir laisser un commentaire sur la picking list des magasiniers.""",

    'description': """
        Le module modifie juste le module stock picking. Il surcharge le modèle stock.picking pour ajouter un seul champ : "commentaire" qui est un commentaire utile pour
        la  livraison. L'information s'encode directement dans la vue Inventaire->Livraison-> vue form de la livraison "Commentaire pour la livraison".
        Ce champ est reporté dans le document imprimable (report) "Bon de préparation avec code barre". Le rapport existant est surchargé pour faire apparaître le champs 
        en haut du formulaire à côté de l'adresse de livraison du client.

    """,

    'author': "Roland Neyrinck",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_stock', 'sale', 'purchase', 'stock'],

    'data': ['views/magasin_views.xml',
             'report_economat.xml'
             ],

}