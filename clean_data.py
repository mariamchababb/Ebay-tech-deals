import pandas as pd

INPUT_FILE = "ebay_tech_deals.csv"
OUTPUT_FILE = "cleaned_ebay_deals.csv"


def clean_price(value: str):
    if pd.isna(value):
        return None

    value = value.replace("US $", "").replace(",", "").strip()

    return value


def main():

    # Load all columns as strings
    df = pd.read_csv(INPUT_FILE, dtype=str)

    # Clean price text
    df["price"] = (
        df["price"]
        .str.replace("US $", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["original_price"] = (
        df["original_price"]
        .str.replace("US $", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    # Convert missing values
    df["original_price"] = df["original_price"].replace(["N/A", ""], pd.NA)

    # Fill missing original prices
    df["original_price"] = df["original_price"].fillna(df["price"])

    # Clean shipping
    df["shipping"] = df["shipping"].fillna("").str.strip()
    df.loc[df["shipping"] == "", "shipping"] = "Shipping info unavailable"
    df.loc[df["shipping"] == "N/A", "shipping"] = "Shipping info unavailable"

    # Convert to float
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

    # Compute discount
    df["discount_percentage"] = (
        (df["original_price"] - df["price"]) / df["original_price"] * 100
    ).round(2)

    # Save cleaned data 
    df.to_csv(OUTPUT_FILE, index=False)

    print("Cleaned data saved to", OUTPUT_FILE)


if __name__ == "__main__":
    main()
