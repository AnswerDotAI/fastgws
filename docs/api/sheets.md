# Google Sheets API

Reads and writes Google Sheets.

Docs: https://developers.google.com/workspace/sheets/

## Methods

### `sheets.spreadsheets.batch_update`

`sheets.spreadsheets.batch_update(spreadsheet_id, body=None)`

Applies one or more updates to the spreadsheet. Each request is validated before being applied. If any request is not valid then the entire request will fail and nothing will be applied. Some requests have replies to give you some information about how they are applied. The replies will mirror the requests. For example, if you applied 4 updates and the 3rd one had a reply, then the response will have 2 empty replies, the actual reply, and another empty reply, in that order. Due to the collaborative nature of spreadsheets, it is not guaranteed that the spreadsheet will reflect exactly your changes after this completes, however it is guaranteed that the updates in the request will be applied together atomically. Your changes may be altered with respect to collaborator changes. If there are no collaborators, the spreadsheet should reflect your changes.

### `sheets.spreadsheets.create`

`sheets.spreadsheets.create(body=None)`

Creates a spreadsheet, returning the newly created spreadsheet.

### `sheets.spreadsheets.developer_metadata.get`

`sheets.spreadsheets.developer_metadata.get(metadata_id, spreadsheet_id)`

Returns the developer metadata with the specified ID. The caller must specify the spreadsheet ID and the developer metadata's unique metadataId. For more information, see [Read, write, and search metadata](https://developers.google.com/workspace/sheets/api/guides/metadata).

### `sheets.spreadsheets.developer_metadata.search`

`sheets.spreadsheets.developer_metadata.search(spreadsheet_id, body=None)`

Returns all developer metadata matching the specified DataFilter. For more information, see [Read, write, and search metadata](https://developers.google.com/workspace/sheets/api/guides/metadata). If the provided DataFilter represents a DeveloperMetadataLookup object, this will return all DeveloperMetadata entries selected by it. If the DataFilter represents a location in a spreadsheet, this will return all developer metadata associated with locations intersecting that region.

### `sheets.spreadsheets.get`

`sheets.spreadsheets.get(spreadsheet_id, exclude_tables_in_banded_ranges=None, include_grid_data=None, ranges=None)`

Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID. By default, data within grids is not returned. You can include grid data in one of 2 ways: * Specify a [field mask](https://developers.google.com/workspace/sheets/api/guides/field-masks) listing your desired fields using the `fields` URL parameter in HTTP * Set the includeGridData URL parameter to true. If a field mask is set, the `includeGridData` parameter is ignored For large spreadsheets, as a best practice, retrieve only the specific spreadsheet fields that you want. To retrieve only subsets of spreadsheet data, use the ranges URL parameter. Ranges are specified using [A1 notation](https://developers.google.com/workspace/sheets/api/guides/concepts#cell). You can define a single cell (for example, `A1`) or multiple cells (for example, `A1:D5`). You can also get cells from other sheets within the same spreadsheet (for example, `Sheet2!A1:C4`) or retrieve multiple ranges at once (for example, `?ranges=A1:D5&ranges=Sheet2!A1:C4`). Limiting the range returns only the portions of the spreadsheet that intersect the requested ranges.

### `sheets.spreadsheets.get_by_data_filter`

`sheets.spreadsheets.get_by_data_filter(spreadsheet_id, body=None)`

Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID. For more information, see [Read, write, and search metadata](https://developers.google.com/workspace/sheets/api/guides/metadata). This method differs from GetSpreadsheet in that it allows selecting which subsets of spreadsheet data to return by specifying a dataFilters parameter. Multiple DataFilters can be specified. Specifying one or more data filters returns the portions of the spreadsheet that intersect ranges matched by any of the filters. By default, data within grids is not returned. You can include grid data in one of two ways: * Specify a [field mask](https://developers.google.com/workspace/sheets/api/guides/field-masks) listing your desired fields using the `fields` URL parameter in HTTP. * Set the includeGridData parameter to `true`. If a field mask is set, the `includeGridData` parameter is ignored. For large spreadsheets, as a best practice, retrieve only the specific spreadsheet fields that you want.

### `sheets.spreadsheets.sheets.copy_to`

`sheets.spreadsheets.sheets.copy_to(sheet_id, spreadsheet_id, body=None)`

Copies a single sheet from a spreadsheet to another spreadsheet. Returns the properties of the newly created sheet.

### `sheets.spreadsheets.values.append`

`sheets.spreadsheets.values.append(range, spreadsheet_id, include_values_in_response=None, insert_data_option=None, response_date_time_render_option=None, response_value_render_option=None, value_input_option=None, body=None)`

Appends values to a spreadsheet. The input range is used to search for existing data and find a "table" within that range. Values will be appended to the next row of the table, starting with the first column of the table. See the [guide](https://developers.google.com/workspace/sheets/api/guides/values#appending_values) and [sample code](https://developers.google.com/workspace/sheets/api/samples/writing#append_values) for specific details of how tables are detected and data is appended. The caller must specify the spreadsheet ID, range, and a valueInputOption. The `valueInputOption` only controls how the input data will be added to the sheet (column-wise or row-wise), it does not influence what cell the data starts being written to.

### `sheets.spreadsheets.values.batch_clear`

`sheets.spreadsheets.values.batch_clear(spreadsheet_id, body=None)`

Clears one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more ranges. Only values are cleared -- all other properties of the cell (such as formatting and data validation) are kept.

### `sheets.spreadsheets.values.batch_clear_by_data_filter`

`sheets.spreadsheets.values.batch_clear_by_data_filter(spreadsheet_id, body=None)`

Clears one or more ranges of values from a spreadsheet. For more information, see [Read, write, and search metadata](https://developers.google.com/workspace/sheets/api/guides/metadata). The caller must specify the spreadsheet ID and one or more DataFilters. Ranges matching any of the specified data filters will be cleared. Only values are cleared -- all other properties of the cell (such as formatting, data validation, etc.) are kept.

### `sheets.spreadsheets.values.batch_get`

`sheets.spreadsheets.values.batch_get(spreadsheet_id, date_time_render_option=None, major_dimension=None, ranges=None, value_render_option=None)`

Returns one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more ranges.

### `sheets.spreadsheets.values.batch_get_by_data_filter`

`sheets.spreadsheets.values.batch_get_by_data_filter(spreadsheet_id, body=None)`

Returns one or more ranges of values that match the specified data filters. For more information, see [Read, write, and search metadata](https://developers.google.com/workspace/sheets/api/guides/metadata). The caller must specify the spreadsheet ID and one or more DataFilters. Ranges that match any of the data filters in the request will be returned.

### `sheets.spreadsheets.values.batch_update`

`sheets.spreadsheets.values.batch_update(spreadsheet_id, body=None)`

Sets values in one or more ranges of a spreadsheet. The caller must specify the spreadsheet ID, a valueInputOption, and one or more ValueRanges.

### `sheets.spreadsheets.values.batch_update_by_data_filter`

`sheets.spreadsheets.values.batch_update_by_data_filter(spreadsheet_id, body=None)`

Sets values in one or more ranges of a spreadsheet. For more information, see [Read, write, and search metadata](https://developers.google.com/workspace/sheets/api/guides/metadata). The caller must specify the spreadsheet ID, a valueInputOption, and one or more DataFilterValueRanges.

### `sheets.spreadsheets.values.clear`

`sheets.spreadsheets.values.clear(range, spreadsheet_id, body=None)`

Clears values from a spreadsheet. The caller must specify the spreadsheet ID and range. Only values are cleared -- all other properties of the cell (such as formatting, data validation, etc..) are kept.

### `sheets.spreadsheets.values.get`

`sheets.spreadsheets.values.get(range, spreadsheet_id, date_time_render_option=None, major_dimension=None, value_render_option=None)`

Returns a range of values from a spreadsheet. The caller must specify the spreadsheet ID and a range.

### `sheets.spreadsheets.values.update`

`sheets.spreadsheets.values.update(range, spreadsheet_id, include_values_in_response=None, response_date_time_render_option=None, response_value_render_option=None, value_input_option=None, body=None)`

Sets values in a range of a spreadsheet. The caller must specify the spreadsheet ID, range, and a valueInputOption.
