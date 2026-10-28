from app.data.loader import (
    load_online_retail,
    clean_online_retail
)

from app.data.analytics import (
    calculate_business_metrics,
    monthly_revenue,
    top_products,
    country_performance,
    customer_performance
)


def main():

    print("=" * 60)
    print("NEXUS BUSINESS DATA ENGINE")
    print("=" * 60)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_online_retail(
        "data/Online Retail.xlsx"
    )

    print("\nOriginal dataset:")
    print(df.head())

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    df = clean_online_retail(df)

    print("\nCleaned dataset:")
    print(df.head())

    print(
        f"\nRows after cleaning: {len(df):,}"
    )

    # --------------------------------------------------------
    # Business metrics
    # --------------------------------------------------------

    metrics = calculate_business_metrics(
        df
    )

    print("\n" + "=" * 60)
    print("BUSINESS KPIs")
    print("=" * 60)

    for key, value in metrics.items():

        print(
            f"{key}: {value}"
        )

    # --------------------------------------------------------
    # Monthly revenue
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("MONTHLY REVENUE")
    print("=" * 60)

    monthly = monthly_revenue(df)

    print(
        monthly.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Top products
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP PRODUCTS")
    print("=" * 60)

    products = top_products(
        df,
        limit=10
    )

    print(
        products.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Countries
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP COUNTRIES")
    print("=" * 60)

    countries = country_performance(
        df,
        limit=10
    )

    print(
        countries.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Customers
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP CUSTOMERS")
    print("=" * 60)

    customers = customer_performance(
        df,
        limit=10
    )

    print(
        customers.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()