import pandas as pd
from geopy.distance import geodesic
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Sample data
data = {
    'id': [1, 2, 3, 4],
    'event': ['SOSP', 'EOSP', 'SOSP', 'EOSP'],
    'dateStamp': [43831, 43831, 43832, 43832],
    'timeStamp': [0.708333, 0.791667, 0.333333, 0.583333],
    'voyage_From': ['Port A', 'Port A', 'Port B', 'Port B'],
    'lat': [34.0522, 34.0522, 36.7783, 36.7783],
    'lon': [-118.2437, -118.2437, -119.4179, -119.4179],
    'imo_num': ['9434761', '9434761', '9434761', '9434761'],
    'voyage_Id': ['6', '6', '6', '6'],
    'allocatedVoyageId': [None, None, None, None]
}

df = pd.DataFrame(data)

# Function to convert Excel date and time to datetime
def excel_date_to_datetime(excel_date, excel_time):
    base_date = datetime(1899, 12, 30)
    date = base_date + timedelta(days=excel_date)
    time = timedelta(days=excel_time)
    return date + time

# Add datetime column
df['event_datetime'] = df.apply(lambda row: excel_date_to_datetime(row['dateStamp'], row['timeStamp']), axis=1)

# Sort by datetime
df = df.sort_values('event_datetime')

# Calculate previous event and previous event datetime
df['prev_event'] = df['event'].shift(1)
df['prev_event_datetime'] = df['event_datetime'].shift(1)
df['prev_voyage_From'] = df['voyage_From'].shift(1)
df['prev_lat'] = df['lat'].shift(1)
df['prev_lon'] = df['lon'].shift(1)

# Calculate duration in minutes
df['duration_minutes'] = (df['event_datetime'] - df['prev_event_datetime']).dt.total_seconds() / 60

# Define segment type
df['segment_type'] = df.apply(lambda row: 'Port Stay' if row['prev_event'] == 'EOSP' and row['event'] == 'SOSP' 
                                             else 'Sailing' if row['prev_event'] == 'SOSP' and row['event'] == 'EOSP'
                                             else 'Other', axis=1)

# Calculate distance travelled in nautical miles using geopy
def calculate_distance(lat1, lon1, lat2, lon2):
    if pd.notnull(lat1) and pd.notnull(lon1) and pd.notnull(lat2) and pd.notnull(lon2):
        return geodesic((lat1, lon1), (lat2, lon2)).nautical
    else:
        return 0

df['distance_travelled_nautical_miles'] = df.apply(lambda row: calculate_distance(row['prev_lat'], row['prev_lon'], row['lat'], row['lon']), axis=1)

# Print the DataFrame with calculated fields
print(df[['id', 'event', 'event_datetime', 'voyage_From', 'lat', 'lon', 'prev_event', 'prev_event_datetime', 'prev_voyage_From', 'prev_lat', 'prev_lon', 'duration_minutes', 'segment_type', 'distance_travelled_nautical_miles']])

# Plot timeline of events
plt.figure(figsize=(12, 6))
for i, row in df.iterrows():
    if row['segment_type'] == 'Port Stay':
        plt.plot([row['prev_event_datetime'], row['event_datetime']], [row['voyage_From'], row['voyage_From']], 'ro-')
    elif row['segment_type'] == 'Sailing':
        plt.plot([row['prev_event_datetime'], row['event_datetime']], [row['prev_voyage_From'], row['voyage_From']], 'bo-')

plt.xlabel('Time')
plt.ylabel('Port')
plt.title('Voyage Event Timeline')
plt.grid(True)
plt.show()

# Summarize duration by segment type
duration_summary = df.groupby('segment_type')['duration_minutes'].sum()

# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(duration_summary, labels=duration_summary.index, autopct='%1.1f%%', startangle=140)
plt.title('Time Distribution by Segment Type')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
