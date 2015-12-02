# -*- coding: utf-8 -*-

import tools
from osv import fields,osv

WAITING_STATES = [
    ('conforme', 'Conform'),
    ('att_conformite', 'Waiting Conformity'),
    ('non_conforme', 'Non-conform'),
    ('rebut', 'Scrapped'),
    ('recycl_conf', 'Conform Recycle'),
    ('recycl_non_conf', 'Non-conform Recycle'),
]


class report_ctrl_rcp(osv.osv):
    _name = "report.ctrl.rcp"
    _description = "Report Ctrl Rcp"
    _auto = False
    _order = 'purchase_order desc'
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
        'partner_id': fields.many2one('res.partner', 'Supplier'),
        'purchase_order': fields.char('Order Reference', size=64),
        'picking': fields.char('Picking', size=64),
        'tracking': fields.char('Tracking', size=64),
        'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse'),
        'minimum_planned_date': fields.date('Expected Date'),
        #'receipt_state': fields.char('State Receipt', size=64),
        'receipt_state': fields.selection([
            ('draft', 'Draft'),
            ('auto', 'Waiting'),
            ('confirmed', 'Confirmed'),
            ('assigned', 'Available'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
            ], 'State Receipt'),
        'ctrl_liberatoire': fields.char('Ctrl Liberatoire', size=64),
        'purchase_lot': fields.char('Purchase Lot', size=64),
        'purchase_eg': fields.char('EG Lot', size=64),
        'ctrl_state': fields.selection([('',''), ('undecided', ''), ('ok', 'Conform'), ('nak', 'Non-Conform')], 'State Ctrl'),
        #'ctrl_state': fields.char('State ctrl', size=64),
        'lot_state': fields.selection(WAITING_STATES, 'State Lot'),
        #'lot_state': fields.char('State Lot', size=64),
        'comment': fields.char('Comment', size=64),
    }


    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_ctrl_rcp')
        cr.execute("""
CREATE OR REPLACE view report_ctrl_rcp as (
select  
        ROW_NUMBER() over (order by pol.id) as id,
        --pol.id as id,
        pol.product_id as product_id, 
        rp.id as partner_id,
        po.name as purchase_order, 
        sp.name as picking,                         -- N°Réception
        sw.id as warehouse_id,
        po.minimum_planned_date as minimum_planned_date,
        sp.state as receipt_state,
        --pas.attconf_type_id as ctrl_liberatoire,              -- Code du controle liberatoir
        --psc.id as ctrl_liberatoire,              -- Code du controle liberatoir
        --psc.ref as ctrl_liberatoire,              -- Code du controle liberatoir
        psc.name as ctrl_liberatoire,               -- Intitulé du controle liberatoir
        spl.origin_lot as purchase_lot,             -- Lot d'originie du fournisseur
        spl.name as purchase_eg,                    -- N°lot interne EG
        st.name as tracking,                        -- Colis
        pas.state as ctrl_state,                    -- Etat du contrôle libéraoire
        spl.lot_state as lot_state,                 -- Etat du lot 
        '' as comment
        --pol.purchase_state,
        --pol.product_id,
        --sm.id,
        --sp.name,                  -- N°Réception
        --sm.state,
        --st.name,                  -- Colis
        --spl.id,                   -- Id du lot
        --pas.id,
        --psc.id,                   -- Id Controle liberatoir
        --psc.name                  -- Intitulé du controle liberatoir
from purchase_order_line pol inner join      purchase_order po                  ON pol.order_id =po.id              -- Lignes des commandes
                             inner join      res_partner rp                     ON po.partner_id=rp.id              -- Partenaires
                             inner join      stock_warehouse sw                 ON po.warehouse_id=sw.id            -- Entrepôt
                             left outer JOIN stock_move sm                      ON sm.purchase_line_id  = pol.id    -- Mouvement de stocks
                             left outer JOIN stock_picking sp                   ON sm.picking_id=sp.id              -- Réception
                             left outer JOIN stock_tracking st                  ON sm.tracking_id=st.id             -- Colis
                             -- inner join      product_waiting_status_type_rel pw ON pol.product_id=pw.type_id     -- Controles liberatoir indiqués dans fiche article
                             left outer join stock_production_lot spl           ON sm.prodlot_id=spl.id             -- Lots
                             left outer join prodlot_attconf_status pas         ON spl.id=pas.prodlot_id            -- Controles liberatoir sur les lots
                             left outer join prodlot_status_change_type psc     ON pas.attconf_type_id=psc.id       -- Etat du controle libéraoire des lots
where purchase_direct_delivery <> True 
      and purchase_state in ('approved', 'arrived','done')
      and (spl.lot_state<>'conforme' or spl.lot_state is null)
      --and (pas.state<>'ok' or pas.state is null)
order by po.name desc 
        )
        """)

report_ctrl_rcp()





