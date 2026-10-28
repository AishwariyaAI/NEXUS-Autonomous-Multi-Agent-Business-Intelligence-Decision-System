from app.data.loader import get_business_analytics


def main():

    print("=" * 60)
    print("NEXUS BUSINESS ANALYTICS ENGINE")
    print("=" * 60)

    analytics = get_business_analytics()

    print("\nBUSINESS KPIs")
    print("-" * 60)

    for key, value in analytics["kpis"].items():
        print(f"{key}: {value:,}")

    print("\nMONTHLY SALES")
    print("-" * 60)

    print(
        analytics["monthly_sales"].to_string(
            index=False
        )
    )

    print("\nTOP PRODUCTS")
    print("-" * 60)

    print(
        analytics["top_products"].to_string(
            index=False
        )
    )

    print("\nTOP COUNTRIES")
    print("-" * 60)

    print(
        analytics["top_countries"].to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()