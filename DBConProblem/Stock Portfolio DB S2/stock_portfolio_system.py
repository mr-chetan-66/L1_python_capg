### stock_portfolio_system.py
### StockPortfolioSystem class — all DB operations, calculations, grouping,
### and report export for the Stock Portfolio Management System

import stock as sk
import portfolio as pf
import cx_Oracle
from datetime import datetime, date
from exceptions import (InvestorNotFoundException,
                        StockNotFoundException,
                        InsufficientSharesException,
                        InvalidSectorException,
                        DuplicateHoldingException)

# Valid sectors — used in group_portfolio_by_sector validation
VALID_SECTORS = ['it', 'banking', 'pharma', 'energy', 'fmcg', 'auto']


class StockPortfolioSystem:

    def __init__(self, conn):
        self.conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all portfolio holdings for an investor
    # ----------------------------------------------------------------
    def retrieve_portfolio_by_investor(self, investor_name):
        cursor = self.conn.cursor()

        query = """
            SELECT portfolio_id, investor_name, stock_id, symbol,
                   quantity, buy_price, buy_date
            FROM portfolio
            WHERE LOWER(investor_name) = :1
            ORDER BY buy_date ASC
        """

        cursor.execute(query, (investor_name.lower(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise InvestorNotFoundException(
                f"No portfolio found for investor: {investor_name}")

        result = []
        for row in rows:
            # Safely handle Oracle datetime vs date
            b_date = row[6].date() if hasattr(row[6], 'date') else row[6]
            obj    = pf.Portfolio(row[0], row[1], row[2], row[3],
                                  row[4], float(row[5]), b_date)
            result.append(obj)

        return result

    # ----------------------------------------------------------------
    # SELECT — retrieve a single stock by ticker symbol
    # ----------------------------------------------------------------
    def retrieve_stock_by_symbol(self, symbol):
        cursor = self.conn.cursor()

        query = """
            SELECT stock_id, symbol, company_name, sector,
                   current_price, listed_date
            FROM stock
            WHERE LOWER(symbol) = :1
        """

        cursor.execute(query, (symbol.lower(),))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            raise StockNotFoundException(
                f"Stock not found for symbol: {symbol}")

        # Safely handle Oracle datetime vs date
        l_date = row[5].date() if hasattr(row[5], 'date') else row[5]

        return sk.Stock(row[0], row[1], row[2], row[3],
                        float(row[4]), l_date)

    # ----------------------------------------------------------------
    # CALCULATION — compute all holding metrics for one portfolio entry
    # ----------------------------------------------------------------
    def calculate_holding_metrics(self, portfolio_obj):
        stock_obj     = self.retrieve_stock_by_symbol(portfolio_obj.get_symbol())
        quantity      = portfolio_obj.get_quantity()
        buy_price     = portfolio_obj.get_buy_price()
        current_price = stock_obj.get_current_price()

        invested_value  = round(quantity * buy_price, 2)
        current_value   = round(quantity * current_price, 2)
        profit_loss     = round(current_value - invested_value, 2)
        pl_pct          = round((profit_loss / invested_value) * 100, 2) \
                          if invested_value != 0 else 0.0
        holding_days    = (date.today() - portfolio_obj.get_buy_date()).days

        return {
            'symbol'          : portfolio_obj.get_symbol(),
            'company_name'    : stock_obj.get_company_name(),
            'sector'          : stock_obj.get_sector(),
            'quantity'        : quantity,
            'buy_price'       : buy_price,
            'current_price'   : current_price,
            'invested_value'  : invested_value,
            'current_value'   : current_value,
            'profit_loss'     : profit_loss,
            'profit_loss_pct' : pl_pct,
            'holding_days'    : holding_days
        }

    # ----------------------------------------------------------------
    # GROUPING — group portfolio holdings by sector (title-cased keys)
    # ----------------------------------------------------------------
    def group_portfolio_by_sector(self, portfolio_list):
        grouped = {}
        for p in portfolio_list:
            stock_obj = self.retrieve_stock_by_symbol(p.get_symbol())
            sector    = stock_obj.get_sector()

            if sector.lower() not in VALID_SECTORS:
                raise InvalidSectorException(
                    f"Unknown sector encountered: {sector}")

            key = sector.title()
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(p)

        return grouped

    # ----------------------------------------------------------------
    # INSERT — add a new holding with 4-step ordered validation
    # ----------------------------------------------------------------
    def add_holding(self, investor_name, symbol, quantity, buy_price, buy_date_str):
        # Step 1: Check stock exists — raises StockNotFoundException if not
        stock_obj = self.retrieve_stock_by_symbol(symbol)

        # Step 2: Check investor does not already hold this symbol
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT COUNT(*) FROM portfolio
               WHERE LOWER(investor_name) = :1 AND LOWER(symbol) = :2""",
            (investor_name.lower(), symbol.lower())
        )
        count = cursor.fetchone()[0]
        cursor.close()

        if count > 0:
            raise DuplicateHoldingException(
                f"Investor already holds {symbol.upper()}. Use sell to modify.")

        # Step 3: Validate quantity
        if quantity < 1:
            raise InsufficientSharesException("Quantity must be at least 1.")

        # Step 4: Validate buy_price
        if buy_price <= 0:
            raise InsufficientSharesException("Buy price must be greater than 0.")

        # Parse buy date from DD-MM-YYYY string
        buy_date     = datetime.strptime(buy_date_str, "%d-%m-%Y").date()
        portfolio_id = stock_obj.get_stock_id() * 1000 + datetime.now().second

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """INSERT INTO portfolio
                   (portfolio_id, investor_name, stock_id, symbol,
                    quantity, buy_price, buy_date)
                   VALUES (:1, :2, :3, :4, :5, :6, :7)""",
                (portfolio_id, investor_name, stock_obj.get_stock_id(),
                 symbol.upper(), quantity, buy_price, buy_date)
            )
            self.conn.commit()
            cursor.close()

        except cx_Oracle.DatabaseError:
            self.conn.rollback()
            raise

        return pf.Portfolio(portfolio_id, investor_name,
                            stock_obj.get_stock_id(), symbol.upper(),
                            quantity, buy_price, buy_date)

    # ----------------------------------------------------------------
    # UPDATE / DELETE — sell shares with 3-step ordered validation
    # Full exit deletes the row; partial exit updates quantity
    # ----------------------------------------------------------------
    def sell_holding(self, investor_name, symbol, sell_quantity, conn):
        # Step 1: Check stock exists — raises StockNotFoundException if not
        self.retrieve_stock_by_symbol(symbol)

        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT portfolio_id, quantity FROM portfolio
                   WHERE LOWER(investor_name) = :1 AND LOWER(symbol) = :2""",
                (investor_name.lower(), symbol.lower())
            )
            row = cursor.fetchone()

            # Step 2: Check holding exists for this investor
            if row is None:
                cursor.close()
                raise InvestorNotFoundException(
                    f"No holding found for {investor_name} in {symbol.upper()}.")

            portfolio_id = row[0]
            current_qty  = row[1]

            # Step 3: Check sufficient shares to sell
            if sell_quantity > current_qty:
                cursor.close()
                raise InsufficientSharesException(
                    f"Cannot sell {sell_quantity} shares. Only {current_qty} held.")

            # Full exit — DELETE the portfolio row
            if sell_quantity == current_qty:
                cursor.execute(
                    "DELETE FROM portfolio WHERE portfolio_id = :1",
                    (portfolio_id,)
                )
                conn.commit()
                cursor.close()
                return (f"Sold {sell_quantity} share(s) of {symbol.upper()}. "
                        f"Holding removed.")

            # Partial exit — UPDATE quantity
            else:
                new_qty = current_qty - sell_quantity
                cursor.execute(
                    "UPDATE portfolio SET quantity = :1 WHERE portfolio_id = :2",
                    (new_qty, portfolio_id)
                )
                conn.commit()
                cursor.close()
                return (f"Sold {sell_quantity} share(s) of {symbol.upper()}. "
                        f"Remaining: {new_qty} share(s).")

        except (InvestorNotFoundException, InsufficientSharesException):
            raise
        except cx_Oracle.DatabaseError:
            conn.rollback()
            raise

    # ----------------------------------------------------------------
    # SUMMARY — aggregate all metrics across an investor's portfolio
    # ----------------------------------------------------------------
    def get_portfolio_summary(self, investor_name):
        holdings     = self.retrieve_portfolio_by_investor(investor_name)
        metrics_list = [self.calculate_holding_metrics(h) for h in holdings]

        total_invested = round(sum(m['invested_value'] for m in metrics_list), 2)
        total_current  = round(sum(m['current_value']  for m in metrics_list), 2)
        total_pl       = round(total_current - total_invested, 2)
        overall_pl_pct = round((total_pl / total_invested) * 100, 2) \
                         if total_invested != 0 else 0.0

        # Best and worst performers by profit/loss percentage
        best  = max(metrics_list, key=lambda m: m['profit_loss_pct'])['symbol']
        worst = min(metrics_list, key=lambda m: m['profit_loss_pct'])['symbol']

        return {
            'investor_name'   : investor_name,
            'holdings'        : metrics_list,
            'total_invested'  : total_invested,
            'total_current'   : total_current,
            'total_pl'        : total_pl,
            'overall_pl_pct'  : overall_pl_pct,
            'best_performer'  : best,
            'worst_performer' : worst
        }

    # ----------------------------------------------------------------
    # FILE WRITE — export full multi-section portfolio report
    # ----------------------------------------------------------------
    def export_portfolio_report(self, summary_dict, sector_groups, filename):
        try:
            now = datetime.now().strftime("%d-%m-%Y %H:%M")
            with open(filename, 'w') as f:
                # Section 1: Header
                f.write("══════════════ PORTFOLIO REPORT ══════════════\n")
                f.write(f"Investor       : {summary_dict['investor_name']}\n")
                f.write(f"Generated On   : {now}\n")
                f.write("─" * 55 + "\n")

                # Section 2: Holdings detail table
                f.write("HOLDINGS DETAIL:\n")
                f.write(f"{'Symbol':<8} {'Company':<22} {'Sector':<10} "
                        f"{'Qty':<5} {'Buy':>8} {'Now':>8} "
                        f"{'P/L':>10} {'P/L%':>7} {'Days':>5}\n")
                f.write("─" * 85 + "\n")
                for h in summary_dict['holdings']:
                    pl_sign = "+" if h['profit_loss'] >= 0 else ""
                    f.write(
                        f"{h['symbol']:<8} {h['company_name'][:22]:<22} "
                        f"{h['sector']:<10} {h['quantity']:<5} "
                        f"{h['buy_price']:>8.2f} {h['current_price']:>8.2f} "
                        f"{pl_sign}{h['profit_loss']:>9.2f} "
                        f"{pl_sign}{h['profit_loss_pct']:>6.2f}% "
                        f"{h['holding_days']:>5}\n"
                    )

                # Section 3: Sector breakdown
                f.write("─" * 55 + "\n")
                f.write("SECTOR BREAKDOWN:\n")
                for sector, items in sector_groups.items():
                    f.write(f"  {sector} : {len(items)} holding(s)\n")

                # Section 4: Summary block
                f.write("─" * 55 + "\n")
                f.write("SUMMARY:\n")
                f.write(f"  Total Invested  : Rs. {summary_dict['total_invested']}\n")
                f.write(f"  Current Value   : Rs. {summary_dict['total_current']}\n")
                pl_sign = "+" if summary_dict['total_pl'] >= 0 else ""
                f.write(f"  Total P/L       : Rs. {pl_sign}{summary_dict['total_pl']}\n")
                f.write(f"  Overall P/L %   : {pl_sign}{summary_dict['overall_pl_pct']}%\n")
                f.write(f"  Best Performer  : {summary_dict['best_performer']}\n")
                f.write(f"  Worst Performer : {summary_dict['worst_performer']}\n")
                f.write("══════════════════════════════════════════════\n")

        except IOError as e:
            raise IOError(f"Failed to write report: {e}")
