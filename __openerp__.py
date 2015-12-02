# -*- coding: utf-8 -*-
{
    'name': 'Eurogerm - Contrôle Réception',
    'version': '1.0',
    'description': """
Avoir un état des produits devant être réceptionnés, des contrôles à réaliser et des contrôles à lever (environnement, sanitaire...) """,
    'author': 'Tony GALMICHE',
    'website': 'http://www.infosaone.com',
    'images': [],
    'depends': ['eurogerm_profile'],
    'init_xml': [],
    'update_xml': [
        'report/report_ctrl_rcp.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
