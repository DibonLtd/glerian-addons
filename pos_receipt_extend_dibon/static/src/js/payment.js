/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.pos = usePos();
    },
    async validateOrder(isForceValidate) {
        const receipt_order = await super.validateOrder(isForceValidate);
        const data = this.pos.session_orders;
        if (data && data.length > 0) {
            const order = data[data.length - 1];
            this.pos.customer_details = order.customer_details;
            this.pos.customer_name = order.customer_name;
            this.pos.customer_address = order.customer_address;
            this.pos.customer_mobile = order.customer_mobile;
            this.pos.customer_phone = order.customer_phone;
            this.pos.customer_email = order.customer_email;
            this.pos.customer_vat = order.customer_vat;
        }
        return receipt_order;
    },
});
