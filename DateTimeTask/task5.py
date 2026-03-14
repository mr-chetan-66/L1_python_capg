from datetime import date

def to_date(s: str) -> date:
    return date.fromisoformat(s)

def main():
    dates = ["2026-03-01", "2026-03-09", "2026-03-10", "2026-02-28"]
    start = "2026-03-01"
    end = "2026-03-10"

    s = to_date(start)
    e = to_date(end)

    in_range = [to_date(d) for d in dates if s <= to_date(d) <= e]

    if not in_range:
        print("No dates in the specified range")
        return

    min_date = min(in_range)
    max_date = max(in_range)

    print(f"{min_date:%Y-%m-%d}, {max_date:%Y-%m-%d}")

if __name__ == "__main__":
    main()