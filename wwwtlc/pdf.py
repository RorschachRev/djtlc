tier1html = """
<h2>{{ app.property.address }}, {{ app.user }} : {{ app.get_status_display }}</h2>
	<h3> ({{ app.submission_date }})</h3>
	<br>
	<br>
	<h2>Property Information</h2>
	<p><strong>Address:</strong> {{ app.property.address }}</p>
	<p><strong>Number of Units:</strong> {{ app.property.no_units }}</p>
	<p><strong>Legal Description:</strong> {{ app.property.legal_description }}</p>
	<p><strong>Year Built:</strong> {{ app.property.year_built }}</p>
	<p><strong>Construction Loan:</strong> {{ app.property.construction_loan }}</p>
	<p><strong>Refinance Loan:</strong> {{ app.property.refinance_loan }}</p>
	<p><strong>Title Names:</strong> {{ app.property.title_names }}</p>
	
	<br>
	<br>
	<h2>Construction Loan Information</h2>
	<p><strong>Year Acquired:</strong> {{ app.property.construction_loan.year_acquired }}</p>
	<p><strong>Original Cost:</strong> {{ app.property.construction_loan.original_cost }}</p>
	<p><strong>Existing Liens Amount:</strong> {{ app.property.construction_loan.amt_existing_liens }}</p>
	<p><strong>Present Value:</strong> {{ app.property.construction_loan.present_value }}</p>
	<p><strong>Improvement Costs:</strong> {{ app.property.construction_loan.improve_cost }}</p>
	<p><strong>Total:</strong> {{ app.property.construction_loan.total }}</p>
	
	<br>
	<br>
	<h2>Refinance Information</h2>
	<p><strong>Year Acquired:</strong>{{ app.property.refinance_loan.year_acquired }}</p>
	<p><strong>Original Cost:</strong>{{ app.property.refinance_loan.original_cost }}</p>
	<p><strong>Existing Liens Amount:</strong>{{ app.property.refinance_loan.amt_existing_liens }}</p>
	<p><strong>Present Value:</strong>{{ app.property.refinance_loan.present_value }}</p>
	<p><strong>Improvement Costs:</strong>{{ app.property.refinance_loan.improve_cost }}</p>
	<p><strong>Total:</strong>{{ app.property.refinance_loan.total }}</p>
	
	<br>
	<br>
	<h2>Business Information</h2>
	<p><strong>Business Name:</strong> {{ app.borrower.business.bus_name }}</p>
	<p><strong>Business Description:</strong> {{ app.borrower.business.bus_description }}</p>
	<p><strong>Base Employee Income:</strong> ${{ app.borrower.business.base_emp_income }}</p>
	<p><strong>Rent:</strong> ${{ app.borrower.business.rent }}</p>
	<p><strong>First Mortgage:</strong> ${{ app.borrower.business.first_mortgage }}</p>
	<p><strong>Other Financing:</strong> ${{ app.borrower.business.other_financing }}</p>
	<p><strong>Other Financing Description:</strong> {{ app.borrower.business.other_financing_description }}</p>
	<p><strong>Hazard Insurance:</strong> ${{ app.borrower.business.hazard_insur }}</p>
	<p><strong>Real Estate Taxes:</strong> ${{ app.borrower.business.real_estate_taxes }}</p>
	<p><strong>Mortgage Insurance:</strong> ${{ app.borrower.business.mortgage_insur }}</p>
	<p><strong>Overtime:</strong> ${{ app.borrower.business.overtime }}</p>
	<p><strong>Bonuses:</strong> ${{ app.borrower.business.bonuses }}</p>
	<p><strong>Commissions:</strong> ${{ app.borrower.business.commissions }}</p>
	<p><strong>Dividends:</strong> ${{ app.borrower.business.dividends }}</p>
	<p><strong>Interest:</strong> ${{ app.borrower.business.interest }}</p>
	<p><strong>Net Rental Income:</strong> ${{ app.borrower.business.net_rental }}</p>
	<p><strong>Income Other Total:</strong> ${{ app.borrower.business.income_other }}</p>
	<p><strong>Income Other Description:</strong> {{ app.borrower.business.income_other_description }}</p>
	<p><strong>Income Total:</strong> ${{ app.borrower.business.income_total }}</p>
	<p><strong>Expense Other Total:</strong> ${{ app.borrower.business.expense_other_total }}</p>
	<p><strong>Expense Other Description:</strong> {{ app.borrower.business.expense_other_description }}</p>
	<p><strong>Expense Total</strong> ${{ app.borrower.business.expense_total }}</p>
	<p><strong>Net Revenue</strong> ${{ app.borrower.business.net_revenue }}</p>
	
	<br>
	<br>
	<h2>Borrower Information</h2>
	<p><strong>User:</strong>{{ app.borrower.user }}</p>
	<p><strong>Application Type:</strong> {{ app.borrower.get_application_type_display }}</p>
	<p><strong>First Name:</strong> {{ app.borrower.borrower_fname }}</p>
	<p><strong>Last Name:</strong> {{ app.borrower.borrower_lname }}</p>
	<p><strong>Applicant Type:</strong> {{ app.borrower.get_applicant_type_display }}</p>
	<p><strong>Filing Type:</strong> {{ app.borrower.get_filing_type_display }}</p>
	<p><strong>Assumed Business Name(s):</strong> {{ app.borrower.assumed_business_names }}</p>
	<p><strong>DBA Name:</strong> {{ app.borrower.dba_name }}</p>
	<p><strong>Borrower Type:</strong> {{ app.borrower.get_borrower_type_display }}</p>
	<p><strong>Title:</strong> {{ app.borrower.title }}</p>
	<p><strong>Authorization:</strong> {{ app.borrower.authorized }}</p>
	<p><strong>Social Security Number:</strong> {{ app.borrower.ssn }}</p>
	<p><strong>TIN Number:</strong> {{ app.borrower.tin_no }}</p>
	<p><strong>Phone Number:</strong> {{ app.borrower.home_phone }}</p>
	<p><strong>Date of Birth:</strong> {{ app.borrower.dob }}</p>
	<p><strong>Years of Schooling Completed:</strong> {{ app.borrower.yrs_school }}</p>
	<p><strong>Marital Status:</strong> {{ app.borrower.get_marital_status_display }}</p>
	<p><strong>Number of Dependents:</strong> {{ app.borrower.dependents }}</p>
	<p><strong>Present Address:</strong> {{ app.borrower.present_addr }}</p>
	<p><strong>Rent/Own:</strong> {{ app.borrower.get_own_rent_display }}</p>
	<p><strong>Years at Address:</strong> {{ app.borrower.living_yrs }}</p>
	<p><strong>Mailing Address:</strong> {{ app.borrower.mail_addr }}</p>
	<p><strong>Pricipal Office Address:</strong> {{ app.borrower.principal_office_addr }}</p>
	<p><strong>Organization's State:</strong> {{ app.borrower.get_organizations_state_display }}</p>
	<p><strong>Former Address:</strong> {{ app.borrower.former_addr }}</p>
	<p><strong>Rent/Own:</strong> {{ app.borrower.get_former_own_rent_display }}</p>
	<p><strong>Years at Address:</strong> {{ app.borrower.former_yrs_lived }}</p>
	<p><strong>Assets & Liabilities Summary:</strong> {{ app.borrower.assets_liabilities }}</p>
	<p><strong>Declarations:</strong> {{ app.borrower.declarations }}</p>
	<p><strong>Filing Date:</strong>{{ app.borrower.filing_dates }}</p>
	<p><strong>Filing Location:</strong>{{ app.borrower.filing_locations }}</p>
	
	
	<br>
	<br>
	<h2>Credit Request</h2>
	<p><strong>Borrower:</strong> {{ credit.borrower }}</p>
	<p><strong>Amount Requested:</strong> {{ credit.amt_requested }}</p>
	<p><strong>Term Requested:</strong> {{ credit.term_requested }}</p>
	<p><strong>Loan Type:</strong> {{ credit.loan_type }}</p>
	<p><strong>Market Survey:</strong> {{ credit.market_survey }}</p>
	<p><strong>Request Purpose:</strong> {{ credit.request_purpose }}</p>
	<p><strong>Credit Request</strong> {{ credit.get_credit_request_display }}</p>
	<p><strong>Submission Date:</strong> {{ credit.submission_date }}</p>
	
	
	<br>
	<br>
	<h2>Declarations</h2>
	<p><strong>Outstanding Judgements:</strong> {{ app.borrower.declarations.outstanding_judgements }}</p>
	<p><strong>Bankrupt:</strong> {{ app.borrower.declarations.bankrupt }}</p>
	<p><strong>Foreclosed:</strong> {{ app.borrower.declarations.forclosed }}</p>
	<p><strong>Lawsuit:</strong> {{ app.borrower.declarations.lawsuit }}</p>
	<p><strong>Obligated Forclosure:</strong> {{ app.borrower.declarations.obligated_forclosure }}</p>
	<p><strong>In Delinquent / Default:</strong> {{ app.borrower.declarations.delinquent_indefault }}</p>
	<p><strong>Alimony:</strong> {{ app.borrower.declarations.alimony }}</p>
	<p><strong>Child Support:</strong> {{ app.borrower.declarations.child_support }}</p>
	<p><strong>Seperate Maintenance:</strong> {{ app.borrower.declarations.seperate_maintenance }}</p>
	<p><strong>Borrowed Down Payment:</strong> {{ app.borrower.declarations.borrowed_down_payment }}</p>
	<p><strong>Co-Maker / Endorser:</strong> {{ app.borrower.declarations.co_maker_endorser }}</p>
	<p><strong>US Citizen:</strong> {{ app.borrower.declarations.us_citizen }}</p>
	<p><strong>Permanent Resident Alien:</strong> {{ app.borrower.declarations.permanent_res_alien }}</p>
	<p><strong>Primary Residence:</strong> {{ app.borrower.declarations.primary_residence }}</p>
	<p><strong>Ownership Interest:</strong> {{ app.borrower.declarations.ownership_interest }}</p>
	<p><strong>Property Type:</strong> {{ app.borrower.declarations.get_m_property_type_display }}</p>
	<p><strong>Title Method:</strong> {{ app.borrower.declarations.get_m_title_method_display }}</p>
	<p><strong>Continuation:</strong> {{ app.borrower.declarations.continuation }}</p>
	
	
	<br>
	<br>
	<h2>Transaction Details:</h2>
	<p><strong>Purchase Price:</strong>{{ app.transaction_details.purchase_price }}</p>
	<p><strong>Alterations:</strong>{{ app.transaction_details.alterations }}</p>
	<p><strong>Improvements:</strong>{{ app.transaction_details.improvements }}</p>
	<p><strong>Repairs:</strong>{{ app.transaction_details.repairs }}</p>
	<p><strong>Land:</strong>{{ app.transaction_details.land }}</p>
	<p><strong>Refinance:</strong>{{ app.transaction_details.refinance }}</p>
	<p><strong>Estimated Prepaid Items:</strong>{{ app.transaction_details.estimated_prepaid_items }}</p>
	<p><strong>Estimated Closing Costs:</strong>{{ app.transaction_details.estimated_closing_costs }}</p>
	<p><strong>PMI:</strong>{{ app.transaction_details.pmi }}</p>
	<p><strong>MIP:</strong>{{ app.transaction_details.mip }}</p>
	<p><strong>Funding Fee:</strong>{{ app.transaction_details.funding_fee }}</p>
	<p><strong>Discount:</strong>{{ app.transaction_details.discount }}</p>
	<p><strong>Total Costs:</strong>{{ app.transaction_details.total_costs }}</p>
	<p><strong>Subordinate Financing:</strong>{{ app.transaction_details.subordinate_financing }}</p>
	<p><strong>Closing Costs Paid:</strong>{{ app.transaction_details.closing_cost_paid }}</p>
	<p><strong>Other Credits Description:</strong>{{ app.transaction_details.other_credits_description }}</p>
	<p><strong>Other Credits Total:</strong>{{ app.transaction_details.other_credits_total }}</p>
	<p><strong>Loan Amount Exclude:</strong>{{ app.transaction_details.loan_amount_exclude }}</p>
	<p><strong>Financed PMI:</strong>{{ app.transaction_details.financed_pmi }}</p>
	<p><strong>Financed MIP:</strong>{{ app.transaction_details.financed_mip }}</p>
	<p><strong>Financed Funding Fee:</strong>{{ app.transaction_details.financed_funding_fee }}</p>
	<p><strong>Loan Amount:</strong>{{ app.transaction_details.loan_amount }}</p>
	<p><strong>Borrower Cash:</strong>{{ app.transaction_details.borrower_cash }}</p>
	
	
	<br>
	<br>
	<h2>Acknowledge / Agree</h2>
	<p><strong>Borrower:</strong>{{ app.acknowledge.borrower }}</p>
	<p><strong>Borrower Agreement:</strong>{{ app.acknowledge.borrower_agree }}</p>
	<p><strong>Coborrower:</strong>{{ app.acknowledge.coborrower }}</p>
	<p><strong>Coborrower Agreement:</strong>{{ app.acknowledge.coborrower_agree }}</p>
	<p><strong>Date:</strong>{{ app.acknowledge.date }}</p>
"""
 
from pyfpdf import FPDF, HTMLMixin
 
class MyFPDF(FPDF, HTMLMixin):
    pass
 
pdf=MyFPDF()
#First page
pdf.add_page()
pdf.write_html(tier1html)
pdf.output('tier1form.pdf','F')