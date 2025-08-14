import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import io

st.set_page_config(page_title="Tunnel Projection Tool", layout="wide")
st.title("Tunnel Projection Tool")

st.markdown("Upload your tunnel alignment and drillhole CSV files to project drillholes onto the tunnel alignment.")

# File upload
tunnel_file = st.file_uploader("Upload Tunnel Alignment CSV data, make sure to rename the columns to exactly this format Easting (m) and Northing (m) ", type=["csv"])
drill_file = st.file_uploader("Upload Borehole Locations CSV data, make sure the column names are id , Easting , Northing ", type=["csv"])

if tunnel_file and drill_file:
    try:
        # Read uploaded files
        tunnel_df = pd.read_csv(tunnel_file)
        drill_df = pd.read_csv(drill_file)

        # Create tunnel line
        tunnel_points = list(zip(tunnel_df['Easting (m)'], tunnel_df['Northing (m)']))
        tunnel_line = LineString(tunnel_points)

        # Project drillholes
        results = []
        for row in drill_df.itertuples(index=False):
            drill_pt = Point(row.Easting, row.Northing)
            projected_pt = tunnel_line.interpolate(tunnel_line.project(drill_pt))
            offset = drill_pt.distance(projected_pt)
            chainage = tunnel_line.project(drill_pt) 
            
            results.append({
                'drillhole_id': row.id,
                'easting': row.Easting,
                'northing': row.Northing,
                'projected_easting': projected_pt.x,
                'projected_northing': projected_pt.y,
                'chainage': chainage,
                'offset': offset
            })

        projection_df = pd.DataFrame(results)

        st.subheader("Projection Results")
        st.dataframe(projection_df)

        # Download button
        csv_buffer = io.StringIO()
        projection_df.to_csv(csv_buffer, index=False)
        st.download_button("Download Results as CSV", csv_buffer.getvalue(), file_name="drillhole_projection_results.csv", mime="text/csv")

        # Plotting
        st.subheader("Projection Plot")
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(tunnel_df['Easting (m)'], tunnel_df['Northing (m)'], label='Tunnel Alignment', color='blue')
        ax.scatter(drill_df['Easting'], drill_df['Northing'], label='Drillholes', color='red', s=30)
        ax.scatter(projection_df['projected_easting'], projection_df['projected_northing'], label='Projected Points', color='green', s=30)

        for i in range(len(projection_df)):
            ax.plot(
                [projection_df.loc[i, 'easting'], projection_df.loc[i, 'projected_easting']],
                [projection_df.loc[i, 'northing'], projection_df.loc[i, 'projected_northing']],
                color='gray', linestyle='--', linewidth=0.8
            )

        ax.set_xlabel('Easting (m)')
        ax.set_ylabel('Northing (m)')
        ax.set_title('Drillhole Projections onto Tunnel Alignment')
        ax.legend()
        ax.grid(True)
        ax.set_aspect('equal')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
