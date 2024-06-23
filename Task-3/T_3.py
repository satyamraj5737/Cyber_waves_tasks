import pandas as pd

# Read data into DataFrame
df = pd.read_csv("C:\\Users\\user\\Downloads\\data.csv")

# Convert date to datetime format
df['date'] = pd.to_datetime(df['date'])

# Convert amount to numeric, coerce errors, and drop rows with NaN amounts
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df.dropna(subset=['amount'], inplace=True)

# Calculate basic statistics by category
stats = df.groupby('category')['amount'].agg(['mean', 'median', 'std', 'count'])
stats = stats.rename(columns={'std': 'std_dev'})
#print(stats)

def detect_anomalies(df, stats, z_threshold=3):
    anomalies = []
    
    for index, row in df.iterrows():
        category_stats = stats.loc[row['category']]
        mean = category_stats['mean']
        std_dev = category_stats['std_dev']
        
        # Calculate Z-score
        if std_dev > 0:  # To avoid division by zero
            z_score = (row['amount'] - mean) / std_dev
            #print(f'Z_Score : {z_score}')
            if abs(z_score) > z_threshold:
                anomalies.append({
                    'transaction_id': row['transaction_id'],
                    'date': row['date'],
                    'category': row['category'],
                    'amount': row['amount'],
                    'reason_for_anomaly': f'Z-score {z_score:.2f} > {z_threshold}'
                })
    
    return pd.DataFrame(anomalies)

anomalies_df = detect_anomalies(df, stats)
print(anomalies_df)

if not anomalies_df.empty:
    # Save anomalies to CSV
    anomalies_df.to_csv('anomalies_report.csv', index=False)
    
    # Print summary statistics
    summary = anomalies_df['category'].value_counts().reset_index()
    summary.columns = ['category', 'anomaly_count']
    print(summary)
else:
    print("No anomalies detected.")
