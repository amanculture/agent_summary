from django.urls import path
from . import views


urlpatterns = [
    path('', views.first, name='first'),
    path('plotly/first', views.Parent.first, name='first'), #
    path('plotly/summary', views.CRMGraphCopy.summary, name='summary'), # 
    path('plotly/details', views.CRMGraphCopy.login_details, name='details'), #
    path('plotly/report', views.CRMGraphCopy.sales_report, name='sales_report'),  #.
    path('plotly/msg-report', views.test.query_report, name='query_report'), #
    path('trav-info', views.TravInfo.Trav_details, name='Trav_Info'),
    path('guess-gender', views.TravInfo.gender_guess_view, name='guess_gender'),
    path('agentdata', views.agent_data, name='agent_data'),  # For downloading Agent Data
    path('code-terminal', views.code_terminal, name='code_terminal'),
   
    
    path('login', views.dashboard.login_page, name='login'),  # Login Page API for Insights Dashboard
    path('download', views.dashboard.excel_download_api, name='download'),

    path('api/inactive-agents', views.dashboard.get_inactive_agents, name='inactive_agents'),
    path('api/agent-login', views.dashboard.agent_login, name='agent_login'),
    path('api/quarterly-tour', views.dashboard.get_quarterly_tour, name='quarterly_tour'),
    path('api/popular-date', views.dashboard.most_popular_tourdate, name='popular_date'), # ignore right now
    path('api/txn-tour-date', views.dashboard.txn_tourdate_relation, name='txn_tour_date'),
    path('api/active-agent-booking', views.dashboard.notactive_agent, name='active_agent_booking'),
    path('api/quarterly-booking', views.dashboard.get_quarterly_booking, name='quarterly_booking'),
    path('api/frequently-login', views.dashboard.frequently_login, name='frequently_login'),
    path('api/login-details', views.dashboard.login_details, name='login_details'),
    path('api/HolidaysSearch', views.dashboard.most_searched_tour, name='Holidays_Search'),


    path('api/yearly-searched-tour', views.dashboard.yearly_searched_tour, name='yearly_searched_tour'), #not using
    path('api/monthly-searched-tour', views.dashboard.monthly_searched_tour, name='monthly_searched_tour'), #not using
    path('api/daily-searched-tour', views.dashboard.daily_searched_tour, name='daily_searched_tour'), #not using

    path('api/most-search-country', views.dashboard.overall_country_search, name='most_search_country'),
    path('api/flyer-download', views.dashboard.flyer_overview, name='flyer_download') ,
    path('api/booking-details', views.dashboard.booking_overviews, name='booking_details'), #ignore
    path('api/booking-kpi', views.dashboard.booking_kpi, name='booking_kpi'), #ignore 
    path('api/agent-booking-report', views.dashboard.agent_booking_report, name='agent_booking_report'),

    path('api/most-search-package', views.dashboard.most_search_package, name='most_search_package'),
    path('api/agent-query', views.dashboard.agent_query, name='agent_query'),
    
    path('api/agent-login-trend', views.dashboard.agent_login_trend, name='agent_login_trend'),
    path('api/agent-query-with-booking', views.dashboard.agent_query_with_booking, name='agent_query_with_booking'),
    path('api/average-booking', views.dashboard.average_booking_report, name='average_booking'), # Ignore
    path('api/get-country-list', views.dashboard.api_get_country_list, name='get_country_list'),
    path('api/get-pkg-title', views.dashboard.api_get_pkg_title, name='series_pkg_title'),
    path('api/active-cancel-guest', views.dashboard.guest_details_by_package, name='guest_details_by_package'),
    path('api/customize-report', views.dashboard.customize_report, name='customize_report'),
    path('api/series-booking', views.dashboard.series_booking_overview, name='series-booking'),
    path('api/customize-booking', views.dashboard.customize_booking_overview, name='customize-booking'),

    path('api/get-emp-id', views.dashboard.api_get_emp_id, name='Employee_ID'), 
    path('api/emp-sales', views.dashboard.tour_sale_by_staff, name='Employee_Sales'), 
    path('api/emp-sales-year', views.dashboard.tour_sale_by_staff_by_year, name='Employee_Sales_by_Year'),

    path('api/country-customize-booking', views.dashboard.country_of_customize_booking_month, name='Country_of_Customize_Booking'),


    path('api/query-data', views.dashboard.query, name='Query'), 

    path('api/top-10-searches', views.dashboard.top_10_searches, name='top_10_searches'),
    path('api/payment-gateway-report', views.dashboard.payment_gateway_report, name='payment_gateway_report'),
    path('api/new-added-guest', views.dashboard.new_added_guest, name='new_added_guest'),

    path('inactive-agent', views.dashboard.inactive_agent, name='Inactive Agents'),  # API for Download Inactive Agents


    path('api/mail-report', views.dashboard.mail_report, name='mail_report'), # API for Mail Send Report
    path('api/mail-not-read', views.dashboard.mail_not_read, name='mail_not_read'),  # API for unread emails
    path('api/mail-for-booking', views.dashboard.mail_For_booking, name='Mail For Booking'),


    path('api/new-added-guest-details', views.dashboard.new_guest_added_details, name="New Added Guest List"),

    path('api/get-distributor-agentid', views.dashboard.list_of_distributor_agents, name="List of Distributor"), # API for getting only Distributor Agent IDs
    path('api/total-sub-agents', views.dashboard.total_sub_agents, name="Total Sub Agents Name"), # API for getting Agent ID of Sub Agent of a Distributor
    path('api/sub-agents-booking', views.dashboard.sub_agent_with_booking, name="Sub Agents With Booking"), # API for Details of Sub Agents of a Distributor
    

    path('api/get-agentid-list', views.dashboard.get_agentid_list, name="List of all Agent ID"), # API for getting list of All Agent IDs with their Name
    path('api/get-agentid-list-2', views.dashboard.get_agentid_list_2, name="List of all Agent ID for Wallet"),
    path('api/wallet-summary', views.dashboard.agent_wallet_summary, name="Wallet Transaction Summary"), # API for Wallet Transaction of Agents
    path('api/guest-payment-by-wallet', views.dashboard.guest_payment_by_wallet, name="Guest Booking Payment by Wallet"), # API for Guest Details whose Payment Done by Agent Wallet

    path('api/flyer-search', views.dashboard.flyer_region, name="Flyer Search by Region/State"), 

    path('api/daily-mailsend-report', views.dashboard.daily_mailsend_report, name="Report for Daily Sended Mail"),

    path('api/wallet-transaction-details', views.dashboard.wallet_transaction_details, name="Wallet Transaction Details"), # API for Wallet Transaction Summary

    path('api/customize-sales-report', views.dashboard.customize_sales_report, name='Customize Sales Report'), # API fro customize Sales Report given by Rahul Sir


    path('api/tour-full-report', views.dashboard.tour_full_report, name='tour_full_report'),  # API for Tour Full Details

    path('api/tour-hotel-details', views.dashboard.tour_hotel_details, name='tour_hotel_details'),  # API for Tour Hotel Details
    
]