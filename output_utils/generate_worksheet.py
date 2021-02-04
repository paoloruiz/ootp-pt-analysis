def generate_worksheet(cards, worksheet, headers, freeze_col, hidden_columns):
    # Write headers
    for i in range(len(headers)):
        worksheet.write(0, i, headers[i])
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
    # Freeze correct panes
    worksheet.freeze_panes(1, headers.index(freeze_col))

    # Hide some columns
    for hidden_cols in hidden_columns:
        start_column = headers.index(hidden_cols[0])
        end_column = headers.index(hidden_cols[1])
        worksheet.set_column(start_column, end_column, None, None, { "hidden": 1 })
