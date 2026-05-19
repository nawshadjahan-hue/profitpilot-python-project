"""Report export helpers for ProfitPilot.

This module builds the plain-text and HTML reports. Keeping report generation
outside the GUI makes the main application file shorter and easier to follow.
"""

import html
import os


def export_business_reports(products: list, output_dir: str) -> tuple[str, str]:
    """Write plain-text and HTML reports, then return both output paths."""
    if not products:
        raise ValueError("Cannot export a report without products.")

    total_revenue = sum(product["revenue"] for product in products)
    total_profit = sum(product["profit"] for product in products)
    best_product = max(products, key=lambda p: p["score"])
    worst_product = min(products, key=lambda p: p["score"])
    report_path = os.path.join(output_dir, "profitpilot_report.txt")
    html_report_path = os.path.join(output_dir, "profitpilot_report.html")

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("ProfitPilot Business Report\n")
        file.write("===========================\n\n")
        file.write(f"Total Products   : {len(products)}\n")
        file.write(f"Total Revenue    : ${total_revenue:.2f}\n")
        file.write(f"Total Profit     : ${total_profit:.2f}\n")
        file.write(f"Best Product     : {best_product['name']} ({best_product['score']}/100)\n")
        file.write(f"Weakest Product  : {worst_product['name']} ({worst_product['score']}/100)\n\n")

        file.write("Product Details\n")
        file.write("---------------\n")
        for product in products:
            file.write(f"\n{product['name']}\n")
            file.write(f"Revenue          : ${product['revenue']:.2f}\n")
            file.write(f"Profit           : ${product['profit']:.2f}\n")
            file.write(f"Margin           : {product['margin']:.2f}%\n")
            file.write(f"Score            : {product['score']}/100\n")
            file.write(f"Decision         : {product['status']}\n")
            file.write(f"Recommendation  : {product['recommendation']}\n")

    table_rows = ""
    for product in products:
        profit = float(product["profit"])
        status_class = str(product["status"]).lower().replace(" ", "-")
        table_rows += f"""
            <tr>
                <td>{html.escape(str(product["name"]))}</td>
                <td>${float(product["revenue"]):.2f}</td>
                <td class="{'loss' if profit < 0 else 'profit'}">${profit:.2f}</td>
                <td>{float(product["margin"]):.2f}%</td>
                <td>{int(product["score"])}/100</td>
                <td><span class="badge {status_class}">{html.escape(str(product["status"]))}</span></td>
                <td>{html.escape(str(product["recommendation"]))}</td>
            </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ProfitPilot Business Report</title>
    <style>
        body {{ margin: 0; background: #edf3f8; color: #17202a; font-family: Segoe UI, Arial, sans-serif; }}
        .page {{ max-width: 1000px; margin: 32px auto; background: #ffffff; padding: 32px; border: 1px solid #cfe0e8; }}
        h1 {{ margin: 0; color: #0f3d56; font-size: 30px; }}
        .subtitle {{ color: #5d6d7e; margin-top: 6px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 28px 0; }}
        .card {{ background: #f8fbfd; border-left: 5px solid #1f7a8c; padding: 16px; }}
        .card-icon {{ font-size: 24px; margin-bottom: 8px; }}
        .label {{ color: #5d6d7e; font-size: 13px; font-weight: 700; text-transform: uppercase; }}
        .value {{ margin-top: 8px; font-size: 22px; font-weight: 800; color: #0f3d56; }}
        .workflow {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 4px 0 28px; }}
        .workflow-step {{ background: #ffffff; border: 1px solid #d7e6ed; border-top: 4px solid #1f7a8c; padding: 12px; font-size: 13px; font-weight: 700; color: #0f3d56; }}
        .workflow-step span {{ display: block; font-size: 22px; margin-bottom: 6px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 14px; }}
        th {{ background: #d8e8ef; color: #0f3d56; text-align: left; padding: 10px; }}
        td {{ border-bottom: 1px solid #e2edf2; padding: 10px; vertical-align: top; }}
        .profit {{ color: #2e8b57; font-weight: 700; }}
        .loss {{ color: #c94c4c; font-weight: 700; }}
        .badge {{ display: inline-block; padding: 5px 9px; color: white; font-weight: 700; font-size: 12px; }}
        .high-potential {{ background: #2e8b57; }}
        .good-performer {{ background: #1f7a8c; }}
        .needs-improvement {{ background: #f2a541; color: #17202a; }}
        .at-risk {{ background: #c94c4c; }}
        .note {{ margin-top: 24px; color: #5d6d7e; font-size: 13px; }}
        @media print {{ body {{ background: white; }} .page {{ margin: 0; border: none; }} }}
    </style>
</head>
<body>
    <main class="page">
        <h1>ProfitPilot Business Report</h1>
        <p class="subtitle">Campus side-hustle performance summary</p>
        <section class="summary">
            <div class="card"><div class="card-icon">#</div><div class="label">Products</div><div class="value">{len(products)}</div></div>
            <div class="card"><div class="card-icon">$</div><div class="label">Revenue</div><div class="value">${total_revenue:.2f}</div></div>
            <div class="card"><div class="card-icon">+</div><div class="label">Profit</div><div class="value">${total_profit:.2f}</div></div>
            <div class="card"><div class="card-icon">TOP</div><div class="label">Top Product</div><div class="value">{html.escape(str(best_product["name"]))}</div></div>
        </section>
        <h2>ProfitPilot Workflow</h2>
        <section class="workflow">
            <div class="workflow-step"><span>1</span>Product Snapshot</div>
            <div class="workflow-step"><span>2</span>Business Summary</div>
            <div class="workflow-step"><span>3</span>Test Scenario</div>
            <div class="workflow-step"><span>4</span>Break-Even Plan</div>
            <div class="workflow-step"><span>5</span>Export Business Report</div>
        </section>
        <h2>Product Details</h2>
        <table>
            <thead><tr><th>Product</th><th>Revenue</th><th>Profit</th><th>Margin</th><th>Score</th><th>Decision</th><th>Recommendation</th></tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
        <p class="note">Tip: open this HTML file in a browser and choose Print or Save as PDF to create a formatted PDF.</p>
    </main>
</body>
</html>
"""

    with open(html_report_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    return report_path, html_report_path
