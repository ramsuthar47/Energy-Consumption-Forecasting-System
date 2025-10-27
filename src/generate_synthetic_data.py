import pandas as pd
import numpy as np
import os

def generate_synthetic_data(base_file):
    
    df = pd.read_csv(base_file)
    print(f"📄 Loaded dataset from: {base_file}")
    print(f"Columns: {list(df.columns)}")
    print(f"Shape: {df.shape}\n")

    df.columns = df.columns.str.strip().str.lower()

    df = df[['country', 'time', 'balance', 'product', 'value', 'unit']]
    df = df[df['product'].str.lower().str.contains('electricity', na=False)]
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])

    print(f"✅ Filtered electricity data. Shape: {df.shape}\n")

    countries = df['country'].unique()
    print(f"🌍 Countries found: {countries}\n")

    all_data = []
    np.random.seed(42)

    for country in countries:
        base_val = df[df['country'] == country]['value'].mean()
        for month in range(1, 13):
            noise = np.random.uniform(-0.1, 0.1)
            value = base_val * (1 + noise)
            all_data.append({
                'country': country,
                'Date': pd.Timestamp(2024, month, 1),
                'Total_Electricity_Production_GWh': round(value, 2)
            })

    df_synthetic = pd.DataFrame(all_data)
    print("✅ Synthetic data created successfully.\n")

    os.makedirs("../Data", exist_ok=True)

    output_path = "../Data/synthetic_electricity_data.csv"
    df_synthetic.to_csv(output_path, index=False)

    print(f"Synthetic data saved to: {os.path.abspath(output_path)}")
    print(f"Final shape: {df_synthetic.shape}\n")
    print("Done! You can now use this file for forecasting or visualization.")

if __name__ == "__main__":
    base_file = "../Data/iea_monthly_electricity.csv"
    generate_synthetic_data(base_file)