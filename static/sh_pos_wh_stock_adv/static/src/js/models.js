odoo.define('sh_pos_wh_stock.Models', function (require) {
    'use strict';

    var { Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");


    const ShPoswhStockOrderline = (Orderline) => class ShPoswhStockOrderline extends Orderline {
        // set_quantity(quantity, keep_price) {
        //     var sh_old_stock = 0
        //     var self = this;
        //     if (this.pos.config.sh_update_real_time_qty && this.pos.config.sh_show_qty_location && this.pos.config.sh_update_quantity_cart_change) {
        //         if (this.quantity){
        //             if (this && this.pos.db && this.pos.db.quant_by_product_id && this.product && this.product.id && this.pos.db.quant_by_product_id[this.product.id] && this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]]) {
        //                 if (this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] <= this.quantity){
        //                     this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] = parseInt(this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]]) + this.quantity;
        //                 }
        //             }
        //         }
        //         console.log('total',this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]])
        //         if (quantity && quantity < 1 && quantity != 'remove' && this.pos.db.quant_by_product_id[this.product.id] && this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]]) {
        //             var actual_quantity = this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] + this.quantity
        //         }
        //         console.log('actual_quantity -> ',actual_quantity)
        //         super.set_quantity(...arguments);
        //         if (quantity != 'remove' && this.pos.db.quant_by_product_id[this.product.id] && this.pos.config.sh_pos_location[0] && this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]]) {
        //             var actual_quantity = this.pos.db.quant_by_product_id[this.product.id][this.pos.config.sh_pos_location[0]] - this.quantity
        //         }
        //         if (actual_quantity) {
        //             var dic = {
        //                 'product_id': this.product.id,
        //                 'location_id': this.pos.config.sh_pos_location[0],
        //                 'quantity': actual_quantity,
        //                 'other_session_qty': this.quantity,
        //                 'manual_update': false
        //             }
    
        //             rpc.query({
        //                 model: 'sh.stock.update',
        //                 method: 'sh_update_manual_qty',
        //                 args: [self.pos.pos_session.id, dic]
        //             })
        //         }
        //     }else{
        //         super.set_quantity(...arguments);
        //     }

        //     return true
        // }
    }

    Registries.Model.extend(Orderline, ShPoswhStockOrderline);

    return ShPoswhStockOrderline


});