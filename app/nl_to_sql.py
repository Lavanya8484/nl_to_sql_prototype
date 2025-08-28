import re
import datetime

def nl_to_sql(nl_query: str, schema_metadata: dict = None):
    q = nl_query.lower().strip()
    params = {}

    # Pattern: Show me all customers from <state>
    m = re.search(r'customers from ([a-zA-Z ]+)', q)
    if m:
        state = m.group(1).strip().title()
        params['state'] = state
        sql = "SELECT customer_id, name, email_address FROM customers WHERE state = :state"
        return sql, params

    # Pattern: total revenue this month
    if "total revenue this month" in q or "total revenue this month?" in q:
        today = datetime.date.today()
        start = today.replace(day=1).isoformat()
        end = today.isoformat()
        params['start'] = start
        params['end'] = end
        sql = ("SELECT SUM(total_amount - COALESCE(discount_applied,0)) AS total_revenue "
               "FROM sales_analytics WHERE order_date >= :start AND order_date <= :end")
        return sql, params

    # Pattern: customers placed orders > $X in last Y months but haven't ordered in last Z days
    m = re.search(r'placed orders worth more than \$?(\d+) in the last (\d+) months but haven\'t ordered in the past (\d+) days', q)
    if m:
        amount = float(m.group(1))
        months = int(m.group(2))
        days = int(m.group(3))
        params['min_total'] = amount
        sql = (f"""WITH recent AS (
  SELECT customer_id, SUM(total_amount - COALESCE(discount_applied,0)) AS spend_6m,
         MAX(order_date) AS last_order_date
  FROM orders
  WHERE order_date >= date('now','-{months} months')
  GROUP BY customer_id
)
SELECT c.customer_id, c.name, r.spend_6m, r.last_order_date
FROM customers c
JOIN recent r ON r.customer_id = c.customer_id
WHERE r.spend_6m > :min_total
  AND r.last_order_date < date('now','-{days} days');""")
        return sql, params

    # Fallback
    return "SELECT 1 as ok", {}
