import dash_ag_grid as dag
import pandas as pd
from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash
from django.db import connection

app = DjangoDash('DataTableApp', external_stylesheets=["/static/css/dash_styles.css"])

columnDefs = [
    {"field": "TourDate", "headerClass": "custom-header"},
    {"field": "PackgID", "headerClass": "custom-header", "cellStyle": {"textAlign": "center"}},
    {"field": "Agentid", "headerClass": "custom-header"},
    {"field": "Destination", "headerClass": "custom-header"},
    {"field": "QueryID", "headerClass": "custom-header"},
    {"field": "Guest", "headerClass": "custom-header", "type": "numericColumn","cellStyle": {"textAlign": "center"}},
    {"field": "RemovedGuest", "headerClass": "custom-header", "type": "numericColumn", "cellStyle": {"textAlign": "center"}},
    {"field": "Amount", "headerClass": "custom-header", "type": "numericColumn", "valueFormatter": {"function": "params.value ? '$' + params.value.toLocaleString() : ''"}, "cellStyle": {"textAlign": "center"}},
    {"field": "Paid", "headerClass": "custom-header", "type": "numericColumn", "valueFormatter": {"function": "params.value ? '$' + params.value.toLocaleString() : ''"}, "cellStyle": {"textAlign": "center"}},
    {"field": "Due", "headerClass": "custom-header", "type": "numericColumn", "valueFormatter": {"function": "params.value ? '$' + params.value.toLocaleString() : ''"}, "cellStyle": {"textAlign": "center"}},
]



def fetch_data():
    with connection.cursor() as cursor:
        cursor.execute(f"""
            WITH BookingData AS (
                SELECT 
                    b.tourdate,
                    b.PackgID,
                    b.agentId,
					b.QueryID,
                    t.PKG_QUERY_ID,
                    ISNULL(t.PKGORIGINALCOST, 0) + ISNULL(t.Makrup, 0) + ISNULL(t.Commision, 0) AS TotalCost,
                    ISNULL(t.PaxDepositAmount, 0) AS PaxDepositAmount
                FROM TBL_BOOKING b
                JOIN TBL_TRAVELLER_NAME t 
                    ON t.PKG_QUERY_ID = b.QueryID
                WHERE b.txn_msg = 'success'
            )
            SELECT 
                b.tourdate,
                b.PackgID,
                b.agentId,
                p.PKG_DESTINATION AS PackageDestination,
				b.QueryID,
                (SELECT COUNT(*) 
                 FROM TBL_TRAVELLER_NAME t 
                 WHERE t.PaxDepositAmount > 0 
                 AND t.Status1 = 'Active' 
                 AND t.CREATED_BY = b.agentId 
                 AND t.pkgid = b.PackgID) AS Total_Guests,
                (SELECT COUNT(*) 
                 FROM TBL_TRAVELLER_NAME t 
                 WHERE t.PaxDepositAmount > 0 
                 AND t.Status1 = 'cancelled'
                 AND t.CREATED_BY = b.agentId 
                 AND t.pkgid = b.PackgID) AS Cancelled_Guest,
                SUM(b.TotalCost) AS TotalCost,
                SUM(b.PaxDepositAmount) AS PaxDepositAmount,
                SUM(b.TotalCost) - SUM(b.PaxDepositAmount) AS DueAmount
            FROM BookingData b
            JOIN TBL_PKG_DETAILS p 
                ON p.pkg_id = b.PackgID
            WHERE CONVERT(DATE, b.tourdate, 103) 
                BETWEEN GETDATE() AND DATEADD(DAY, 30, GETDATE())
            GROUP BY 
                b.tourdate, b.PackgID, b.agentId, p.PKG_DESTINATION, b.QueryID
            ORDER BY b.tourdate,
            CAST(b.PackgID AS INT) ASC;
        """)

        data_to_show = cursor.fetchall()

    df = pd.DataFrame(data_to_show, columns=['TourDate', 'PackgID', 'Agentid', 'Destination', 'QueryID', 'Guest', 'RemovedGuest', 'Amount', 'Paid', 'Due'])

    # # Grouping by 'TourDate' and 'PackgID'
    # df = df_new.groupby(['TourDate', 'PackgID']).agg({
    #     'Agentid': lambda x: list(x),  # Store Agent IDs as a list
    #     'Destination': 'first',        # Keep first destination
    #     'Guest': 'sum',
    #     'RemovedGuest': 'sum',
    #     'Amount': 'sum',
    #     'Paid': 'sum',
    #     'Due': 'sum',
    # }).reset_index()

    return df


app.layout = html.Div(
    [
        dcc.Markdown("""###  Upcoming Tours in Next 30 Days""", style={"textAlign": "center", "fontSize": "20px", "color": "#2C3E50"}),
        
        dag.AgGrid(
            id="enable-pagination",
            columnDefs=columnDefs,
            rowData=[],  # Empty initially, will be filled by callback
            columnSize="sizeToFit",
            #defaultColDef={"filter": True},
            defaultColDef={"filter": True, "sortable": True, "resizable": True},
            #dashGridOptions={"pagination": True, "animateRows": False},
            dashGridOptions={"pagination": True, "animateRows": True},
            style={"height": "400px", "width": "100%", "border": "1px solid #ccc", "borderRadius": "20px"},
            
        ),
    ],
    style={"margin": "10px","padding" : "1px", "backgroundColor": "#ECF0F1", "borderRadius": "15px"},
)

# ✅ Callback to load data dynamically
@app.callback(
    Output("enable-pagination", "rowData"),
    Input("enable-pagination", "id")  # Trigger when component loads
)
def load_data(_):
    df = fetch_data()
    return df.to_dict("records")
