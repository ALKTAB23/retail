odoo.define("sh_pos_secondary.SelectionPopup", function (require) {
    "use strict";

    const SelectionPopup = require("point_of_sale.SelectionPopup");
    const Registries = require('point_of_sale.Registries');

    const ShSelectionPopup = (SelectionPopup) =>
        class extends SelectionPopup {
            setup(){
                super.setup()
            }
            add_class(event){
                let clicked_row =  event.target.parentElement
                if($(clicked_row).hasClass("highlight")){
                    $(clicked_row).removeClass()
                }else{
                    $(clicked_row).addClass("highlight")
                } 
            }
        }

    Registries.Component.extend(SelectionPopup, ShSelectionPopup)

});
