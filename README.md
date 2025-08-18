# tunnel-projection-app# Project Overview
This repository provides a Streamlit-based tool for projecting borehole locations onto a tunnel alignment. The main workflow is interactive: users upload CSV files for tunnel alignment and borehole locations, and the app computes and visualizes the projection results.

## Key Files & Structure
- `tunnel_projection_app.py`: Main Streamlit application. Handles file upload, data parsing, geometric projection, visualization, and CSV export.
- No test suite, build scripts, or CI/CD present; all workflows are interactive and data-driven.

## Data Flow & Patterns
- **File Upload**: User uploads two CSV files:
  - Tunnel alignment: columns must be `Easting (m)` and `Northing (m)`.
  - Borehole locations: columns must be `id`, `Easting`, and `Northing`.
- **Parsing**: Data is read into pandas DataFrames. Column names are strictly validated for downstream processing.
- **Projection**: Borehole points are projected onto the tunnel alignment using Shapely's `LineString` and `Point` geometry. For each borehole, the nearest point on the tunnel is found, and chainage/offset are calculated.
- **Visualization**: Results are shown in a table and plotted using matplotlib. The plot includes the tunnel alignment, original borehole locations, projected points, and offset lines.
- **Export**: Results can be downloaded as a CSV file via Streamlit's download button.

## Conventions & Patterns
- All data is processed in-memory; no persistent storage or database.
- DataFrames are used for all tabular data manipulation and display.
- UI is minimal: file upload, results table, download button, and plot.
- Error handling is user-facing (Streamlit error/info messages).
- All logic is contained in `tunnel_projection_app.py`.

## Integration Points & Dependencies
- **Streamlit**: For UI and app logic.
- **pandas**: For data manipulation.
- **matplotlib**: For plotting.
- **shapely**: For geometric calculations (projection, distance, chainage).
- **io**: For in-memory CSV export.

## Example Patterns
- Projecting a borehole onto the tunnel alignment:
  ```python
  drill_pt = Point(row.Easting, row.Northing)
  projected_pt = tunnel_line.interpolate(tunnel_line.project(drill_pt))
  offset = drill_pt.distance(projected_pt)
  chainage = tunnel_line.project(drill_pt)
  ```
- Plotting results:
  ```python
  ax.plot(tunnel_df['Easting (m)'], tunnel_df['Northing (m)'], label='Tunnel Alignment')
  ax.scatter(drill_df['Easting'], drill_df['Northing'], label='Drillholes')
  ax.scatter(projection_df['projected_easting'], projection_df['projected_northing'], label='Projected Points')
  ```

## How to Extend
- To support new input formats, update column validation and parsing logic.
- For new visualizations, add plotting functions and UI elements in `tunnel_projection_app.py`.

---

