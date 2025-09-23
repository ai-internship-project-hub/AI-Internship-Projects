import math
from collections import defaultdict, Counter

# Optional pretty output with 'rich' (falls back to plain prints)
USE_RICH = True
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.rule import Rule
    from rich import box
    console = Console()
except Exception:
    USE_RICH = False

# -----------------------------
# Helpers for printing
# -----------------------------
def cprint(text="", style=None):
    if USE_RICH:
        console.print(text, style=style)
    else:
        print(text)

def hr(title=None):
    if USE_RICH:
        if title:
            console.rule(f"[bold]{title}[/bold]")
        else:
            console.rule()
    else:
        print("\n" + ("=" * 60))
        if title:
            print(title)
            print("-" * 60)

def fmt_money(x: float) -> str:
    try:
        return f"{x:,.2f}"
    except Exception:
        return str(round(x, 2))

# -----------------------------
# Categorization rules
# -----------------------------
NEEDS_KEYS = {
    "rent","mortgage","groceries","food","provisions","staples",
    "utilities","electricity","water","gas","internet","wifi","phone",
    "transport","fuel","bus","metro","commute","insurance","medical","health",
    "education","tuition","childcare","tax","maintenance","emi","loan","loans"
}
WANTS_KEYS = {
    "dining","restaurants","coffee","entertainment","movies","games","shopping",
    "fashion","travel","vacation","hobbies","gadgets","subscriptions","netflix",
    "spotify","prime","disney","gym","salon","beauty","water bill"
}
DEBT_KEYS = {"loan","loans","debt","credit","emi","card"}
SAVINGS_KEYS = {"savings","invest","investment","investments","sip","mutual","rd","fd"}

def bucket_for(category: str) -> str:
    key = category.strip().lower()
    # exact/contains check
    def hit(words):
        return any(w in key for w in words)
    if hit(SAVINGS_KEYS): return "Savings/Investments"
    if hit(DEBT_KEYS):    return "Debt/Loans"
    if hit(NEEDS_KEYS):   return "Needs"
    if hit(WANTS_KEYS):   return "Wants"
    # default guess
    return "Wants"

# -----------------------------
# Core analysis
# -----------------------------
def analyze(income: float, expense_pairs: list[tuple[str, float]]):
    # Sum by category and bucket
    by_category = defaultdict(float)
    for cat, amt in expense_pairs:
        by_category[cat.strip().title()] += float(max(0.0, amt))

    by_bucket = defaultdict(float)
    for cat, amt in by_category.items():
        b = bucket_for(cat)
        by_bucket[b] += amt

    total_expenses = sum(by_category.values())
    savings_monthly = max(0.0, income - total_expenses)
    savings_rate = (savings_monthly / income) * 100 if income > 0 else 0.0

    # 50/30/20 benchmark
    target_needs  = 0.50 * income
    target_wants  = 0.30 * income
    target_save   = 0.20 * income

    needs  = by_bucket.get("Needs", 0.0) + min(by_bucket.get("Debt/Loans", 0.0), target_needs * 0.4)  # treat minimum debt as needs-ish
    wants  = by_bucket.get("Wants", 0.0)
    debt   = by_bucket.get("Debt/Loans", 0.0)
    saved_in_expense = by_bucket.get("Savings/Investments", 0.0)
    # Effective monthly saving = leftover + anything user already labeled as savings/investments
    effective_saving = savings_monthly + saved_in_expense

    # Emergency fund: 3–6× monthly needs (use "needs" baseline; fall back to essentials=0.5*income)
    essentials = needs if needs > 0 else 0.5 * income
    ef_min = 3 * essentials
    ef_max = 6 * essentials
    months_to_ef_min = math.inf if effective_saving <= 0 else ef_min / max(1e-9, effective_saving)

    # Top spending categories
    top_cats = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:5]

    result = {
        "income": income,
        "by_category": dict(by_category),
        "by_bucket": dict(by_bucket),
        "total_expenses": total_expenses,
        "savings_monthly": savings_monthly,
        "effective_saving": effective_saving,
        "savings_rate": savings_rate,
        "targets": {
            "needs": target_needs,
            "wants": target_wants,
            "savings": target_save
        },
        "bench_now": {
            "needs": needs,
            "wants": wants,
            "debt": debt,
            "explicit_saving": saved_in_expense
        },
        "emergency_fund": {
            "min_target": ef_min,
            "max_target": ef_max,
            "months_to_min": months_to_ef_min
        },
        "top_categories": top_cats
    }
    return result

# -----------------------------
# Tips/Recommendations (rules)
# -----------------------------
def build_tips(analysis: dict) -> list[str]:
    tips = []
    inc  = analysis["income"]
    exp  = analysis["total_expenses"]
    sv   = analysis["savings_monthly"]
    effs = analysis["effective_saving"]
    needs = analysis["bench_now"]["needs"]
    wants = analysis["bench_now"]["wants"]
    debt  = analysis["bench_now"]["debt"]
    tgt   = analysis["targets"]

    # Deficit or low savings
    if exp > inc:
        tips.append("You’re in a monthly deficit. Aim to trim 10–15% from top ‘Wants’ categories and renegotiate any fixed bills.")
    elif (sv / inc) < 0.10:
        tips.append("Your savings rate is below 10%. Try to push towards 15–20% by cutting a small % from Wants and renegotiating fixed costs.")

    # 50/30/20 nudges
    if needs > tgt["needs"] * 1.10:
        tips.append("Needs exceed the 50% guideline. Consider lowering rent/utilities/insurance or optimizing commute.")
    if wants > tgt["wants"] * 1.10:
        tips.append("Wants exceed the 30% guideline. Audit subscriptions, dining, shopping; cap each at a fixed monthly limit.")
    if (effs) < tgt["savings"] * 0.8:
        tips.append("Savings below the 20% benchmark. Automate transfers on payday to make saving the default.")

    # Debt strategies
    if debt > 0:
        tips.append("You have loan/credit outflow. Use **Avalanche** (pay highest interest first) or **Snowball** (smallest balance first) for faster payoff. Make at least the minimums on all debts.")

    # Emergency fund
    ef = analysis["emergency_fund"]
    if math.isfinite(ef["months_to_min"]):
        tips.append(f"Build an emergency fund (~3–6× needs). At your current saving pace, ~{ef['months_to_min']:.1f} months to reach 3×.")
    else:
        tips.append("Set up an emergency fund target of ~3–6× monthly needs. Start with a small, automatic monthly transfer.")

    # Category-specific trims
    common_hints = {
        "Rent": "Negotiate renewal or consider a slightly smaller place/roommate to reduce % of income.",
        "Utilities": "Optimize thermostat, use LED bulbs, and reduce standby power.",
        "Dining": "Set a weekly dining cap; try meal prep for workdays.",
        "Subscriptions": "Cancel rarely used services; switch to annual plans if cheaper.",
        "Transport": "Use passes/carpool; plan errands to reduce trips.",
        "Groceries": "Buy staples in bulk; plan meals around weekly offers."
    }
    for cat, _ in analysis["top_categories"]:
        base = cat.split()[0].title()
        if base in common_hints and len(tips) < 8:
            tips.append(f"{base}: {common_hints[base]}")

    # Make tips unique & concise
    deduped = []
    seen = set()
    for t in tips:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped[:8]

# -----------------------------
# Investment split (educational only)
# -----------------------------
def sample_investment_split(monthly_saving: float):
    # Balanced, simple example (NOT financial advice)
    if monthly_saving <= 0:
        return []
    parts = [
        ("Broad-market index funds/ETFs", 0.60),
        ("Short/medium-term fixed income", 0.30),
        ("Cash buffer (high-yield/recurring)", 0.10),
    ]
    return [(name, pct, monthly_saving * pct) for name, pct in parts]

# -----------------------------
# Pretty reporting
# -----------------------------
def render_report(analysis: dict):
    inc  = analysis["income"]
    exp  = analysis["total_expenses"]
    sv   = analysis["savings_monthly"]
    effs = analysis["effective_saving"]
    sr   = analysis["savings_rate"]
    bnow = analysis["bench_now"]
    tgt  = analysis["targets"]

    # Title
    if USE_RICH:
        console.print(Panel.fit("💰 AI Personal Finance Assistant", style="bold cyan"), justify="center")
    else:
        print("\n" + "="*60 + "\n💰 AI Personal Finance Assistant\n" + "="*60)

    # Summary
    hr("Summary")
    cprint(f"Monthly Income: ₹{fmt_money(inc)}")
    cprint(f"Total Expenses: ₹{fmt_money(exp)}")
    cprint(f"Leftover (raw): ₹{fmt_money(sv)}")
    if bnow["explicit_saving"] > 0:
        cprint(f"User-labeled Savings/Investments: ₹{fmt_money(bnow['explicit_saving'])}")
    cprint(f"Effective Monthly Saving: ₹{fmt_money(effs)}  (Savings Rate: {sr:.1f}%)")

    # Bucket table
    hr("Spending by Buckets")
    rows = [
        ("Needs", bnow["needs"], tgt["needs"]),
        ("Wants", bnow["wants"], tgt["wants"]),
        ("Debt/Loans", bnow["debt"], 0.15 * inc),  # soft guide: keep debt service reasonable
        ("Savings/Investments (labeled)", analysis["by_bucket"].get("Savings/Investments", 0.0), tgt["savings"])
    ]
    if USE_RICH:
        t = Table(title="Current vs. Guideline (50/30/20)", box=box.SIMPLE_HEAVY)
        t.add_column("Bucket", style="bold")
        t.add_column("Current (₹)", justify="right")
        t.add_column("Guideline (₹)", justify="right")
        for name, cur, goal in rows:
            t.add_row(name, fmt_money(cur), fmt_money(goal))
        console.print(t)
    else:
        print("{:<30} {:>15} {:>18}".format("Bucket","Current (₹)","Guideline (₹)"))
        for name, cur, goal in rows:
            print("{:<30} {:>15} {:>18}".format(name, fmt_money(cur), fmt_money(goal)))

    # Top categories
    hr("Top Spending Categories")
    if USE_RICH:
        tc = Table(box=box.MINIMAL_DOUBLE_HEAD)
        tc.add_column("#", justify="right")
        tc.add_column("Category")
        tc.add_column("Amount (₹)", justify="right")
        for i, (cat, amt) in enumerate(analysis["top_categories"], 1):
            tc.add_row(str(i), cat, fmt_money(amt))
        console.print(tc)
    else:
        for i, (cat, amt) in enumerate(analysis["top_categories"], 1):
            print(f"{i}. {cat}: ₹{fmt_money(amt)}")

    # Emergency fund
    ef = analysis["emergency_fund"]
    hr("Emergency Fund Plan")
    cprint(f"Target: ₹{fmt_money(ef['min_target'])} to ₹{fmt_money(ef['max_target'])} (≈3–6× monthly needs)")
    if math.isfinite(ef["months_to_min"]):
        cprint(f"At current saving pace, ≈ {ef['months_to_min']:.1f} months to reach 3× needs.")
    else:
        cprint("Start with a small automatic monthly transfer to build your 3–6× needs buffer.")

    # Investment split (educational only)
    inv = sample_investment_split(analysis["effective_saving"])
    if inv:
        hr("Sample Monthly Investment Split (Educational Only)")
        if USE_RICH:
            it = Table(box=box.SIMPLE)
            it.add_column("Bucket")
            it.add_column("Percent", justify="right")
            it.add_column("Amount (₹)", justify="right")
            for name, pct, amt in inv:
                it.add_row(name, f"{int(pct*100)}%", fmt_money(amt))
            console.print(it)
        else:
            print("{:<40} {:>8} {:>15}".format("Bucket","Percent","Amount (₹)"))
            for name, pct, amt in inv:
                print("{:<40} {:>7}% {:>15}".format(name, int(pct*100), fmt_money(amt)))

    # Tips
    tips = build_tips(analysis)
    hr("Recommendations")
    for i, tip in enumerate(tips, 1):
        cprint(f"{i}. {tip}")

    # Disclaimer
    hr()
    cprint("[Note] This tool uses simple rules for educational purposes and isn’t financial advice.", style="dim" if USE_RICH else None)

# -----------------------------
# Input handling
# -----------------------------
def parse_expenses(raw: str):
    """
    Parse comma-separated 'category:amount' pairs.
    Example: rent:15000, groceries:6000, transport:2000, dining:1500, utilities:2200, loan:3000
    """
    items = []
    for part in raw.split(","):
        if not part.strip():
            continue
        if ":" not in part:
            # treat as unknown category
            cat = part.strip().title()
            amt = 0.0
        else:
            cat, amt = part.split(":", 1)
            cat = cat.strip().title()
            try:
                amt = float(amt.strip())
            except Exception:
                amt = 0.0
        items.append((cat, amt))
    return items

# -----------------------------
# Main
# -----------------------------
def main():
    # Heading
    if USE_RICH:
        console.print(Panel.fit("🧮 AI Personal Finance Assistant", style="bold green"))
    else:
        print("\n" + "="*60 + "\n🧮 AI Personal Finance Assistant\n" + "="*60)

    # Inputs
    try:
        income = float(input("Enter your monthly income (numbers only): ").strip())
    except Exception:
        income = 0.0

    exp_raw = input(
        "Enter monthly expenses as 'category:amount' pairs, comma-separated\n"
        "e.g. rent:15000, groceries:6000, transport:2000, dining:1500, utilities:2200, loan:3000\n> "
    ).strip()

    expenses = parse_expenses(exp_raw)
    analysis = analyze(income, expenses)
    render_report(analysis)

if __name__ == "__main__":
    main()
