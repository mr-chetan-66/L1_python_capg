### main.py
### Entry point — presents a 3-choice menu and delegates to StockPortfolioSystem

import db_config as db
from stock_portfolio_system import StockPortfolioSystem
from exceptions import (InvestorNotFoundException,
                        StockNotFoundException,
                        InsufficientSharesException,
                        InvalidSectorException,
                        DuplicateHoldingException)


def main():
    conn = db.get_connection()
    sps  = StockPortfolioSystem(conn)

    print("=" * 45)
    print("      STOCK PORTFOLIO MANAGEMENT SYSTEM")
    print("=" * 45)
    print("\n1. View Portfolio")
    print("2. Add Holding")
    print("3. Sell Holding")

    choice = input("\nEnter Choice (1 / 2 / 3) : ").strip()

    # ----------------------------------------------------------------
    # CHOICE 1 — View full portfolio summary + sector breakdown + export
    # ----------------------------------------------------------------
    if choice == '1':
        investor_name = input("Enter Investor Name : ")

        summary = sps.get_portfolio_summary(investor_name)

        print(f"\nPortfolio Summary — {summary['investor_name']}")
        print("=" * 65)

        for h in summary['holdings']:
            pl_sign = "+" if h['profit_loss'] >= 0 else ""
            print(f"  {h['symbol']:<8} | Qty: {h['quantity']:<5} | "
                  f"Buy: {h['buy_price']:<8} | Now: {h['current_price']:<8} | "
                  f"P/L: {pl_sign}{h['profit_loss']} ({pl_sign}{h['profit_loss_pct']}%) | "
                  f"Days: {h['holding_days']}")

        print(f"\n  Total Invested  : Rs. {summary['total_invested']}")
        print(f"  Current Value   : Rs. {summary['total_current']}")
        print(f"  Total P/L       : Rs. {summary['total_pl']}")
        print(f"  Overall P/L %   : {summary['overall_pl_pct']}%")
        print(f"  Best Performer  : {summary['best_performer']}")
        print(f"  Worst Performer : {summary['worst_performer']}")

        holdings_list = sps.retrieve_portfolio_by_investor(investor_name)
        sector_groups = sps.group_portfolio_by_sector(holdings_list)

        print("\n  Sector Breakdown:")
        for sector, items in sector_groups.items():
            print(f"    {sector}: {len(items)} holding(s)")

        filename = input("\nEnter Filename to Export Report : ")
        sps.export_portfolio_report(summary, sector_groups, filename)
        print(f"Report exported to {filename}")

    # ----------------------------------------------------------------
    # CHOICE 2 — Add a new holding to an investor's portfolio
    # ----------------------------------------------------------------
    elif choice == '2':
        investor_name = input("Enter Investor Name         : ")
        symbol        = input("Enter Stock Symbol          : ")
        quantity      = int(input("Enter Quantity              : "))
        buy_price     = float(input("Enter Buy Price             : "))
        buy_date_str  = input("Enter Buy Date (DD-MM-YYYY) : ")

        new_holding = sps.add_holding(
            investor_name, symbol, quantity, buy_price, buy_date_str
        )

        print(f"\nHolding added! Portfolio ID: {new_holding.get_portfolio_id()}")
        print(f"  {new_holding.get_quantity()} share(s) of "
              f"{new_holding.get_symbol()} at Rs. {new_holding.get_buy_price()}")

    # ----------------------------------------------------------------
    # CHOICE 3 — Sell shares (partial or full exit)
    # ----------------------------------------------------------------
    elif choice == '3':
        investor_name = input("Enter Investor Name         : ")
        symbol        = input("Enter Stock Symbol to Sell  : ")
        sell_qty      = int(input("Enter Quantity to Sell      : "))

        result = sps.sell_holding(investor_name, symbol, sell_qty, conn)
        print(result)

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == '__main__':
    try:
        main()
    except InvestorNotFoundException as e:
        print(e)
    except StockNotFoundException as e:
        print(e)
    except InsufficientSharesException as e:
        print(e)
    except InvalidSectorException as e:
        print(e)
    except DuplicateHoldingException as e:
        print(e)
    except ValueError:
        print("Invalid input. Please enter valid values.")
