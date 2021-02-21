from output_utils.progress.progress_bar import ProgressBar

def generate_worksheet(cards, worksheet, headers, freeze_col, hidden_columns, sheet_name):
    progress_bar = ProgressBar(len(headers) + len(cards) + len(hidden_columns), "Writing " + sheet_name + " sheet")

    # Write headers
    for i in range(len(headers)):
        worksheet.write(0, i, headers[i])
        
        progress_bar.increment("Writing " + sheet_name + " headers")
    # Headers are first row
    i = 1
    for card in cards:
        # Read parameters off player array
        player_arr = []
        for header in headers:
            player_arr.append(card[header])

        # Write to worksheet
        for j in range(len(player_arr)):
            worksheet.write(i, j, player_arr[j])
        i += 1

        progress_bar.increment("Writing " + sheet_name + " cards")
    # Freeze correct panes
    worksheet.freeze_panes(1, headers.index(freeze_col))

    # Hide some columns
    for hidden_cols in hidden_columns:
        start_column = headers.index(hidden_cols[0])
        end_column = headers.index(hidden_cols[1])
        worksheet.set_column(start_column, end_column, None, None, { "hidden": 1 })

        progress_bar.increment("Hiding " + sheet_name + " columns")

    progress_bar.finish()
