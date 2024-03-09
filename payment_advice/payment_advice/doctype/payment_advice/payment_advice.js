// Copyright (c) 2024, quantbit technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Advice', {
	// refresh: function(frm) {

	// }
});

//============================================================================* Filters on Fields *=================================================================================

frappe.ui.form.on('Payment Advice', {
    setup: function(frm) {
        frm.set_query("party_type", function(doc) {
            return {
                filters: [
                    ['DocType', 'name', 'in', ['Customer', 'Supplier']]
                ]
            };
        });
    }
});

frappe.ui.form.on('Payment Advice', {
    setup: function(frm) {
		frm.set_query("from_account", function() {
			var account_types = in_list(["Pay", "Internal Transfer"], frm.doc.payment_type) ?
			["Bank", "Cash"] : [frappe.boot.party_account_types[frm.doc.party_type]];
            return {
                filters:{
					"account_type": ["in", account_types],
					"is_group": 0,
					"company": frm.doc.company
				}
            };
        });
    }
});

frappe.ui.form.on('Payment Advice', {
    setup: function(frm) {
		frm.set_query("to_account", function() {
			var account_types = in_list(["Pay", "Internal Transfer"], frm.doc.payment_type) ?
			["Payable"] : [frappe.boot.party_account_types[frm.doc.party_type]];
            return {
                filters:{
					"account_type": ["in", account_types],
					"is_group": 0,
					"company": frm.doc.company
				}
            };
        });
    }
});

// ======================================================================= * Method Call * ==========================================================================

frappe.ui.form.on('Payment Advice', {
	party: function(frm) {
		frm.clear_table("payment_advice_details");
		frm.refresh_field('payment_advice_details');
		frm.call({
			method:'get_entries',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on('Payment Advice', {
	party_type: function(frm) {
		frm.call({
			method:'set_reference_doctype',
			doc:frm.doc
		})
	}
});

// ======================================================================== *Child Table* ====================================================================================
// Addition of Allocated Quantity based from Child Entries

frappe.ui.form.on("Payment Advice Details", {
	allocated_amount:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total1 = 0;
	frm.doc.payment_advice_details.forEach(function(d) { total1 += d.allocated_amount; });
	frm.set_value("total_allocated_amount", total1);
	refresh_field("total_allocated_amount");
	frm.set_value("paid_amount", total1);
	refresh_field("paid_amount");
	frm.set_value("received_amount", total1);
	refresh_field("received_amount");
	
  },
   items_remove:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total1 = 0;
	frm.doc.payment_advice_details.forEach(function(d) { total1 += d.allocated_amount; });
	frm.set_value("total_allocated_amount", total1);
	refresh_field("total_allocated_amount");
	frm.set_value("paid_amount", total1);
	refresh_field("paid_amount");
	frm.set_value("received_amount", total1);
	refresh_field("received_amount");
   }
 });