/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

patch(Order.prototype, {
    export_for_printing() {
        const result = super.export_for_printing();
        const partner = this.get_partner ? this.get_partner() : this.partner;
        if (partner) {
            result.client = Object.assign(result.client || {}, {
                name: partner.name || '',
                vat: partner.vat || '',
            });
        }
        return result;
    }
});

patch(OrderReceipt.prototype, {
    get dibonCustomerName() {
        const services = this.env && this.env.services;
        const pos = services && services.pos;
        const order = pos && pos.selectedOrder;
        const partner = order && (order.get_partner ? order.get_partner() : order.partner);
        if (partner && partner.name) {
            return partner.name;
        }

        const receiptData = this._getDibonReceiptData();
        return receiptData && receiptData.client && receiptData.client.name || "";
    },

    get dibonCustomerVat() {
        const services = this.env && this.env.services;
        const pos = services && services.pos;
        const order = pos && pos.selectedOrder;
        const partner = order && (order.get_partner ? order.get_partner() : order.partner);
        if (partner && partner.vat) {
            return partner.vat;
        }

        const receiptData = this._getDibonReceiptData();
        return receiptData && receiptData.client && receiptData.client.vat || "";
    },

    _getDibonReceiptData() {
        const p = this.props || {};
        let receiptData = p.data || p.order || p.receiptInfo || p.receipt || null;
        if (receiptData && typeof receiptData.export_for_printing === 'function') {
            receiptData = receiptData.export_for_printing();
        }
        return receiptData;
    },
});
