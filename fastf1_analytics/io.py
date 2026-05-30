def get_drivers_from_input():
    drivers_abbrs = []
    while True:
        abbr = input("Enter the abbreviations of F1 drivers' surnames [-1 to exit]: ").strip()
        if abbr == "-1":
            break
        drivers_abbrs.append(abbr.upper())
    return drivers_abbrs