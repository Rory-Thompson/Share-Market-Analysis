from dash import Dash, Input, Output, html, State
import dash_daq as daq
import Dashboard_testing.ids as ids

def render(app):

    app.clientside_callback(
        #client side callback written in js. 
        """
        function(toggle_value, buy_data, all_data) {
            let selectedData = toggle_value ? buy_data : all_data;

            if (!selectedData || selectedData.length === 0) {
                return [[], []];
            }

             const columnOrder = [
                "code", "title", "company_sector", "last",
                "high", "low", "change_percent", "market_cap",
                "updated_at", "week_percent_change",
                "ytd_percent_change", "RSI_window_14_periods_13"
            ];

            // Reorder the data based on columnOrder
            const reorderedData = selectedData.map(row => {
                let newRow = {};
                columnOrder.forEach(col => {
                    newRow[col] = row[col] !== undefined ? row[col] : null;
                });
                return newRow;
            });

            const columns = columnOrder.map(col => ({
                id: col,
                name: col
            }));

            return [reorderedData, columns];
        }
        """,
        Output(ids.DATATABLE, "data"),
        Output(ids.DATATABLE,"columns"),
        Input(ids.TOGGLEALLSWITCH,"value"),
        Input(ids.SHAREDATASTORE_LATEST_BUY,"data"),
        State(ids.SHAREDATASTORE_LATEST, "data"),
        
    )


    return daq.ToggleSwitch(
        id = ids.TOGGLEALLSWITCH,
        label = "Toggle between ALL share data and shares recomended to buy",
        value = False

    )


