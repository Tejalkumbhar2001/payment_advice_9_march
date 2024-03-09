# Copyright (c) 2024, quantbit technology and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PaymentAdvice(Document):

	def on_submit(self):
		self.payment_entry()

	# FoR Fetch Child entries from customer or supplier
	@frappe.whitelist()
	def get_entries(self):
		if self.party_type == "Customer":
			doc = frappe.get_all("Sales Invoice", 
							filters={"customer": self.party},
							fields=["name","grand_total","outstanding_amount"],)
			if(doc):
				for d in doc:
					if d.outstanding_amount >0:
						self.append('payment_advice_details', {
															"document_number":d.name,
															"grand_total":d.grand_total,
															"outstanding_amount":d.outstanding_amount,
						
														})
		else:
			doc = frappe.get_all("Purchase Invoice", 
							filters={"supplier": self.party},
							fields=["name","grand_total","outstanding_amount"],)
			if(doc):
				for d in doc:
					if d.outstanding_amount >0:
						self.append('payment_advice_details', {
															"document_number":d.name,
															"grand_total":d.grand_total,
															"outstanding_amount":d.outstanding_amount,
		
														})
						
		self.set_rdoc_inchild()

	# Set Reference Doctype based on Paty Type
	@frappe.whitelist()
	def set_reference_doctype(self):
		if self.party_type == "Customer":
			self.reference_doctype = "Sales Invoice"
		else:
			self.reference_doctype = "Purchase Invoice"

	# Set Reference doctype in child table Payment  Advice Details
	@frappe.whitelist()
	def set_rdoc_inchild(self):
		for i in self.get("payment_advice_details"):
			i.reference_doctype = self.reference_doctype
  
	

	# For Payment Entry creation after Saving Payment Advice Document
	@frappe.whitelist()
	def payment_entry(self):
		doc = frappe.new_doc("Payment Entry")
		doc.payment_type = self.payment_type
		doc.company = self.company	
		doc.party_type = self.party_type
		doc.party = self.party
		doc.posting_date =self.posting_date

		doc.paid_from = self.from_account
		doc.paid_to = self.to_account
		doc.paid_from_account_currency = self.paid_from_account_currency
		doc.paid_to_account_currency = self.paid_to_account_currency
		doc.paid_amount = self.paid_amount
		doc.received_amount = self.received_amount
		doc.base_paid_amount = self.base_paid_amount
		doc.received_amount_company_currency = self.received_amount_company_currency
		doc.source_exchange_rate = self.source_exchange_rate
		doc.target_exchange_rate =self.target_exchange_rate

		if self.chequereference_no and self.chequereference_date:
			doc.reference_date = self.chequereference_date
			doc.reference_no = self.chequereference_no

		for i in self.get("payment_advice_details"):
			
			doc.append("references", {
				"reference_doctype":i.reference_doctype,
				"reference_name": i.document_number,
				"total_amount": i.grand_total,
				"outstanding_amount": i.outstanding_amount,
				"allocated_amount": i.allocated_amount,
			})

		doc.custom_payment_advice = self.name
		doc.insert()
		doc.save()
		doc.submit()




	