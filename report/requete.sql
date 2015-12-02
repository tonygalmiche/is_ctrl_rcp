select  ROW_NUMBER() over (order by pol.id) as id,
        pol.id,
        pol.name, 
        --rp.name,
        po.name, 
        --sw.name,
        --po.minimum_planned_date,
        sp.state,
        pas.attconf_type_id,
        psc.ref,                    -- Code du controle liberatoir
        --spl.origin_lot,             -- Lot d'originie du fournisseur
        spl.name "Lot",             -- N°lot interne EG
        spl.id,
        pas.state,                  -- Etat du contrôle libéraoire
        spl.lot_state               -- Etat du lot 
        --pol.purchase_state,
        --pol.product_id,
        --sm.id,
        --sp.name "Réception",      -- N°Réception
        --sm.state,
        --st.name "Colis",          -- Colis
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
      --and (spl.lot_state<>'conforme' or spl.lot_state is null)
      and (pas.state<>'ok' or pas.state is null)
order by po.name desc limit 10;



