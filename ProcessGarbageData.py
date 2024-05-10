import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('Data.csv')

# Convert time columns to datetime objects with explicit format
df['Time1'] = pd.to_datetime(df['Time1'], format='%H:%M:%S')
df['Time2'] = pd.to_datetime(df['Time2'], format='%H:%M:%S')

# Drop duplicate timestamps in Time1 column
df = df.drop_duplicates(subset=['Time1'])

# Ensure data is sorted by Time1
df = df.sort_values(by='Time1')

# Fill NaN values in Time1 column with a forward-fill method
df['Time1'] = df['Time1'].ffill()

# Reset index
df.reset_index(drop=True, inplace=True)

# Define a function to interpolate missing temperature values
def interpolate_temperature(df):
    for i in range(1, len(df)-1):
        if pd.isnull(df.at[i, 'Ambient']):
            if pd.notnull(df.at[i-1, 'Ambient']) and pd.notnull(df.at[i+1, 'Ambient']):
                df.at[i, 'Ambient'] = (df.at[i-1, 'Ambient'] + df.at[i+1, 'Ambient']) / 2
        if pd.isnull(df.at[i, 'Motor']):
            if pd.notnull(df.at[i-1, 'Motor']) and pd.notnull(df.at[i+1, 'Motor']):
                df.at[i, 'Motor'] = (df.at[i-1, 'Motor'] + df.at[i+1, 'Motor']) / 2
    return df

# Interpolate missing temperature values
df = interpolate_temperature(df)

df['Delta'] = df['Motor'] - df['Ambient']

timeOfBlank = "12:35:00"

# Find the index of the blanking point
blanking_point_index = df[df['Time1'] == pd.to_datetime(timeOfBlank, format='%H:%M:%S')].index
if not blanking_point_index.empty:
    blanking_point_index = blanking_point_index[0]
else:
    print("Blanking point not found.")

# Split DataFrame into two parts: before and after the blanking point
if blanking_point_index > 0:
    df_before = df.iloc[:blanking_point_index]
    df_after = df.iloc[blanking_point_index+1:]  # Exclude the blanking point itself

    # Calculate average delta before and after the blanking point
    average_delta_before = df_before['Delta'].mean()
    average_delta_after = df_after['Delta'].mean()

    print("Average Delta Before Blanking Point:", average_delta_before)
    print("Average Delta After Blanking Point:", average_delta_after)

    # Plot the data
    plt.plot(df['Time1'].values, df['Ambient'].values, label='Ambient Temperature')
    plt.plot(df['Time1'].values, df['Motor'].values, label='Motor Temperature')
    plt.plot(df['Time1'].values, df['Delta'].values, label='Delta')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature Variation Over Time')
    plt.legend()

    # Adding a horizontal line at '12:50'
    blanking_point = pd.to_datetime(timeOfBlank, format='%H:%M:%S')  # Assuming all timestamps are on the same day
    if blanking_point in df['Time1'].values:
        plt.axvline(x=blanking_point, color='r', linestyle='--', label='Blanking Point')
        plt.text(blanking_point + pd.Timedelta(hours=1),  # Position the text one hour after the blanking point
                df['Delta'].max(),  # Adjust y position to avoid overlapping with the plot
                f'Average delta after blanking: {average_delta_after:.3f}',  # Text to display
                color='green',  # Text color
                fontsize=12)  # Text font size
        plt.text(blanking_point - pd.Timedelta(hours=2),  # Position the text two hours before the blanking point
                df['Delta'].max(),  # Adjust y position to avoid overlapping with the plot
                f'Average delta before blanking: {average_delta_before:.3f}',  # Text to display
                color='blue',  # Text color
                fontsize=12)  # Text font size

    plt.show()

