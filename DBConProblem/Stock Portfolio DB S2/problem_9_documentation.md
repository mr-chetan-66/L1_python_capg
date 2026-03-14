# Problem 9 — Stock Portfolio Management System

## Overview

A **multi-table, class-based system** using a **single domain class** (`StockPortfolioSystem`) that encapsulates all DB operations, calculations, grouping, and file export in one place. This is architecturally different from Problems 2–8 — there is no separate DAO and util split. All 8 methods live inside the system class itself, using `self.conn`.

---

## File Structure

```
problem_9_portfolio/
│
├── database.properties          → DB credentials config
├── stock.py                     → Entity class (6 fields, getters & setters)
├── portfolio.py                 → Entity class (7 fields, getters & setters)
├── exceptions.py                → 5 custom exception classes
├── stock_portfolio_system.py    → StockPortfolioSystem class — all 8 methods + VALID_SECTORS
└── main.py                      → Entry point (3-choice menu)
```

---

## Why No DAO / Util Split Here?

In Problems 2–8 the pattern was:
- `*_dao.py` → class that only touches the DB
- `*_util.py` → standalone functions that never touch the DB

This problem is specified with a **single class** `StockPortfolioSystem` that blends both responsibilities — every method (`retrieve_*`, `calculate_*`, `group_*`, `add_*`, `sell_*`, `get_summary`, `export_*`) lives inside the class and shares `self.conn`. This is intentional — it mirrors a real-world service/facade class pattern.

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `stock.py` | Entity class — 6 fields, getters & setters |
| `portfolio.py` | Entity class — 7 fields, getters & setters |
| `exceptions.py` | 5 custom exceptions isolated in one place |
| `stock_portfolio_system.py` | `StockPortfolioSystem(conn)` — all 8 methods + `VALID_SECTORS` constant |
| `main.py` | Entry point — 3-choice menu: view → add → sell |

---

## Oracle Tables

```sql
CREATE TABLE stock (
    stock_id       NUMBER PRIMARY KEY,
    symbol         VARCHAR2(10) UNIQUE,
    company_name   VARCHAR2(100),
    sector         VARCHAR2(30),
    current_price  NUMBER(10, 2),
    listed_date    DATE
);

CREATE TABLE portfolio (
    portfolio_id   NUMBER PRIMARY KEY,
    investor_name  VARCHAR2(100),
    stock_id       NUMBER,
    symbol         VARCHAR2(10),
    quantity       NUMBER,
    buy_price      NUMBER(10, 2),
    buy_date       DATE
);
```

---

## Entity Class — `stock.py`

| Field | Type | Description |
|-------|------|-------------|
| `stock_id` | NUMBER | Primary key |
| `symbol` | VARCHAR2(10) | Ticker symbol e.g. `INFY`, `TCS` |
| `company_name` | VARCHAR2(100) | Full company name |
| `sector` | VARCHAR2(30) | Sector e.g. `IT`, `Banking` |
| `current_price` | NUMBER(10,2) | Current market price per share |
| `listed_date` | DATE | Date listed on exchange |

---

## Entity Class — `portfolio.py`

| Field | Type | Description |
|-------|------|-------------|
| `portfolio_id` | NUMBER | Primary key (`stock_id * 1000 + now().second`) |
| `investor_name` | VARCHAR2(100) | Investor full name |
| `stock_id` | NUMBER | FK → stock table |
| `symbol` | VARCHAR2(10) | Ticker symbol |
| `quantity` | NUMBER | Number of shares held |
| `buy_price` | NUMBER(10,2) | Price per share at purchase |
| `buy_date` | DATE | Date shares were bought |

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `InvestorNotFoundException` | No portfolio for investor; OR no holding for investor in given symbol |
| `StockNotFoundException` | Symbol not found in stock table |
| `InsufficientSharesException` | Sell qty > held qty; OR `quantity < 1`; OR `buy_price <= 0` |
| `InvalidSectorException` | Stock's sector not in `VALID_SECTORS` |
| `DuplicateHoldingException` | Investor already holds the specified symbol |

---

## System Class — `stock_portfolio_system.py`

```python
class StockPortfolioSystem:
    def __init__(self, conn):
        self.conn = conn   # public — used by all methods
```

### Constants (module-level)

```python
VALID_SECTORS = ['it', 'banking', 'pharma', 'energy', 'fmcg', 'auto']
```

---

### Method 1: `retrieve_portfolio_by_investor(investor_name)`
- `WHERE LOWER(investor_name) = :1` sorted by `buy_date ASC`
- Safely converts Oracle DATE → `date`
- Raises `InvestorNotFoundException` if empty
- Returns list of `Portfolio` objects

---

### Method 2: `retrieve_stock_by_symbol(symbol)`
- `WHERE LOWER(symbol) = :1`
- Safely converts Oracle DATE → `date`
- Raises `StockNotFoundException` if not found
- Returns `Stock` object

---

### Method 3: `calculate_holding_metrics(portfolio_obj)`
Calls `retrieve_stock_by_symbol()` internally. Returns metrics dict:

| Key | Formula |
|-----|---------|
| `invested_value` | `quantity × buy_price` |
| `current_value` | `quantity × current_price` |
| `profit_loss` | `current_value − invested_value` |
| `profit_loss_pct` | `(profit_loss / invested_value) × 100` |
| `holding_days` | `(today − buy_date).days` |

Also includes: `symbol`, `company_name`, `sector`, `quantity`, `buy_price`, `current_price`. All floats rounded to 2 dp.

---

### Method 4: `group_portfolio_by_sector(portfolio_list)`
- Calls `retrieve_stock_by_symbol()` per holding
- Groups into `{title_cased_sector: [Portfolio, ...]}` dict
- Raises `InvalidSectorException` if sector not in `VALID_SECTORS`

---

### Method 5: `add_holding(investor_name, symbol, quantity, buy_price, buy_date_str)`
Validates in this **exact order**:

1. Stock exists → `StockNotFoundException`
2. Investor doesn't already hold symbol → `DuplicateHoldingException`
3. `quantity >= 1` → `InsufficientSharesException`
4. `buy_price > 0` → `InsufficientSharesException`

Then: parses `buy_date_str` with `"%d-%m-%Y"`, generates `portfolio_id = stock_id * 1000 + now().second`, INSERTs, commits, returns `Portfolio` object. Rollback on `cx_Oracle.DatabaseError`.

---

### Method 6: `sell_holding(investor_name, symbol, sell_quantity, conn)`
Validates in this **exact order**:

1. Stock exists → `StockNotFoundException`
2. Holding exists → `InvestorNotFoundException`
3. `sell_quantity <= current_qty` → `InsufficientSharesException`

- `sell_quantity == current_qty` → **DELETE** row, return `"Sold N share(s) of SYMBOL. Holding removed."`
- `sell_quantity < current_qty` → **UPDATE** quantity, return `"Sold N share(s) of SYMBOL. Remaining: M share(s)."`

---

### Method 7: `get_portfolio_summary(investor_name)`
Returns aggregated summary dict:

| Key | Value |
|-----|-------|
| `investor_name` | str |
| `holdings` | list of metrics dicts |
| `total_invested` | sum of `invested_value` |
| `total_current` | sum of `current_value` |
| `total_pl` | `total_current − total_invested` |
| `overall_pl_pct` | `(total_pl / total_invested) × 100` |
| `best_performer` | symbol with highest `profit_loss_pct` |
| `worst_performer` | symbol with lowest `profit_loss_pct` |

---

### Method 8: `export_portfolio_report(summary_dict, sector_groups, filename)`
Writes 4-section overwrite-mode report:
1. Header — investor name + generated datetime
2. Holdings detail — aligned column table with all metrics
3. Sector breakdown — sector → holding count
4. Summary block — totals, best/worst performer

Raises `IOError` if file cannot be written.

---

## Main Program Flow — `main.py`

```
Menu:
  1. View Portfolio
  2. Add Holding
  3. Sell Holding

Choice 1 — VIEW PORTFOLIO
    ├── Call: sps.get_portfolio_summary(investor_name)
    ├── Display: per-holding P/L + totals + best/worst
    ├── Call: sps.retrieve_portfolio_by_investor(investor_name)
    ├── Call: sps.group_portfolio_by_sector(holdings_list)
    ├── Display: sector breakdown
    └── Export: sps.export_portfolio_report(summary, sector_groups, filename)

Choice 2 — ADD HOLDING
    ├── Input: investor_name, symbol, quantity, buy_price, buy_date_str
    ├── Call: sps.add_holding(...)
    └── Display: new portfolio ID + holding details

Choice 3 — SELL HOLDING
    ├── Input: investor_name, symbol, sell_qty
    ├── Call: sps.sell_holding(investor_name, symbol, sell_qty, conn)
    └── Display: result message
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Investor not in portfolio table | `InvestorNotFoundException` — "No portfolio found for investor: `<name>`" |
| Symbol not in stock table | `StockNotFoundException` — "Stock not found for symbol: `<symbol>`" |
| Investor already holds symbol | `DuplicateHoldingException` — "Investor already holds `<SYMBOL>`. Use sell to modify." |
| `quantity < 1` on add | `InsufficientSharesException` — "Quantity must be at least 1." |
| `buy_price <= 0` on add | `InsufficientSharesException` — "Buy price must be greater than 0." |
| No holding to sell | `InvestorNotFoundException` — "No holding found for `<name>` in `<SYMBOL>`." |
| Sell qty > held qty | `InsufficientSharesException` — "Cannot sell N shares. Only M held." |
| Unknown sector in grouping | `InvalidSectorException` — "Unknown sector encountered: `<sector>`" |
| DB error on INSERT/UPDATE/DELETE | `conn.rollback()` called; `cx_Oracle.DatabaseError` re-raised |
| Report file write fails | `IOError` raised from `export_portfolio_report` |

---

## Key Python Concepts Used

```python
# portfolio_id formula
portfolio_id = stock_id * 1000 + datetime.now().second

# Holding metrics — all in one dict
invested_value  = round(quantity * buy_price, 2)
current_value   = round(quantity * current_price, 2)
profit_loss     = round(current_value - invested_value, 2)
pl_pct          = round((profit_loss / invested_value) * 100, 2)
holding_days    = (date.today() - buy_date).days

# Best/worst performer using lambda + max/min
best  = max(metrics_list, key=lambda m: m['profit_loss_pct'])['symbol']
worst = min(metrics_list, key=lambda m: m['profit_loss_pct'])['symbol']

# Sector grouping with VALID_SECTORS (list of lowercase strings)
if sector.lower() not in VALID_SECTORS:
    raise InvalidSectorException(...)
key = sector.title()

# sell_holding — DELETE vs UPDATE based on qty comparison
if sell_quantity == current_qty:
    DELETE FROM portfolio WHERE portfolio_id = :1
else:
    UPDATE portfolio SET quantity = :1 WHERE portfolio_id = :2

# Aligned column formatting in report
f"{h['symbol']:<8} {h['company_name'][:22]:<22} ... {h['profit_loss']:>9.2f}"

# Sign prefix for P/L display
pl_sign = "+" if h['profit_loss'] >= 0 else ""
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| 2 | Employee Payroll | SELECT + salary dict + experience calc + file report |
| 3 | Hospital Appointment | SELECT + COUNT slot check + dict grouping + CSV export |
| 4 | Inventory Restock | Two-step SELECT + urgency dict + post-build exception + UPDATE + append log |
| 5 | Event Booking | Two-table DAO + 4-step validation + INSERT+UPDATE transaction + nested dict |
| 6 | Crime Record Management | Two-table DAO + Custom Exceptions + Dict Grouping + File Report |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Courier Tracking | Two-table DAO + State-Machine + Bulk CSV + File Report |
| **9** | **Stock Portfolio** | **Single system class + Full CRUD + 5 exceptions + metrics dict + sector grouping + multi-section report** |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
