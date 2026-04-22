import ydata_profiling_utils as ydputi


def main() -> None:
    """
    Run YData-profiling on the Baltimore housing dataset.

    :return: None.
    """
    df = ydputi.load_baltimore_data()
    ydputi.print_basic_info(df)
    profile = ydputi.create_profile_report(df)
    output_path = ydputi.save_profile_report(profile)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()