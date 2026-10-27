"""Session 1 - Handle data subject requests (access, rectification, erasure, portability).

A small SQLite database stands in for a company's customer system. The handler:
  * verifies the requester's identity before doing anything,
  * calculates the legal deadline (one month, extendable by two more for complex cases),
  * answers ACCESS and PORTABILITY requests with a machine-readable JSON export,
  * applies RECTIFICATION,
  * applies ERASURE but keeps records that a law obliges us to retain (invoices),
  * writes every action to an audit log (accountability).
All people and data are fictional. Everything runs in memory.
Run:  python session-01_dsar_handler.py
"""
import calendar
import json
import sqlite3
from datetime import date


def add_months(d, months):
    """Same day N months later; clamp to the month's last day (31 Jan + 1 month = 28/29 Feb)."""
    m = d.month - 1 + months
    y, m = d.year + m // 12, m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def setup():
    db = sqlite3.connect(":memory:")
    db.executescript("""
    CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT, phone TEXT);
    CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INT, item TEXT, amount REAL, odate TEXT);
    CREATE TABLE invoices(id INTEGER PRIMARY KEY, customer_id INT, order_id INT, total REAL);
    CREATE TABLE marketing(customer_id INT, consent INT, segment TEXT);
    CREATE TABLE audit_log(at TEXT, request TEXT, customer_id INT, action TEXT);
    INSERT INTO customers VALUES (1,'Sara Ahmed','sara@example.com','Karachi','0300-0000001'),
                                 (2,'Bilal Khan','bilal@example.com','Lahore','0300-0000002');
    INSERT INTO orders VALUES (10,1,'Networking Basics',2500,'2026-03-02'),
                              (11,1,'Python for Security',3200,'2026-07-15'),
                              (12,2,'Digital Forensics 101',4100,'2026-05-20');
    INSERT INTO invoices VALUES (100,1,10,2500),(101,1,11,3200),(102,2,12,4100);
    INSERT INTO marketing VALUES (1,1,'tech-books'),(2,0,'none');
    """)
    return db


def log(db, today, req, cid, action):
    db.execute("INSERT INTO audit_log VALUES (?,?,?,?)", (today.isoformat(), req, cid, action))


def verify_identity(db, email, otp_ok):
    row = db.execute("SELECT id FROM customers WHERE email=?", (email,)).fetchone()
    return row[0] if row and otp_ok else None


def export(db, cid):
    """Everything we hold about one person, in a structured, commonly used format (JSON)."""
    cur = db.execute("SELECT name,email,city,phone FROM customers WHERE id=?", (cid,))
    profile = dict(zip([c[0] for c in cur.description], cur.fetchone()))
    orders = [dict(zip(["item", "amount", "date"], r)) for r in
              db.execute("SELECT item,amount,odate FROM orders WHERE customer_id=?", (cid,))]
    mk = db.execute("SELECT consent,segment FROM marketing WHERE customer_id=?", (cid,)).fetchone()
    return {"profile": profile, "orders": orders,
            "marketing": {"consent": bool(mk[0]), "segment": mk[1]} if mk else None,
            "purposes": ["order fulfilment (contract)", "newsletter (consent)"],
            "retention": "orders and invoices 6 years (tax law); marketing until consent withdrawn"}


def handle(db, req, email, otp_ok, received, complex_case=False, **kw):
    cid = verify_identity(db, email, otp_ok)
    due = add_months(received, 3 if complex_case else 1)
    print(f"\n>> {req.upper()} request from {email} received {received}  (respond by {due})")
    if cid is None:
        print("   Identity NOT verified -> ask for more proof; the clock waits. No data disclosed.")
        return
    if req in ("access", "portability"):
        data = export(db, cid)
        print(json.dumps(data, indent=2) if req == "access" else
              "   Portability file (JSON, " + str(len(json.dumps(data))) + " bytes) ready for the user to download")
    elif req == "rectification":
        db.execute("UPDATE customers SET city=? WHERE id=?", (kw["city"], cid))
        print(f"   City corrected to {kw['city']}")
    elif req == "erasure":
        db.execute("DELETE FROM marketing WHERE customer_id=?", (cid,))
        db.execute("UPDATE customers SET name='[erased]', email=NULL, phone=NULL, city=NULL WHERE id=?", (cid,))
        db.execute("UPDATE orders SET item='[erased]' WHERE customer_id=?", (cid,))
        kept = db.execute("SELECT COUNT(*) FROM invoices WHERE customer_id=?", (cid,)).fetchone()[0]
        print(f"   Profile, marketing data and order details erased.")
        print(f"   {kept} invoice(s) RETAINED: legal obligation (tax records) overrides erasure.")
    log(db, received, req, cid, "completed")


def main():
    db = setup()
    handle(db, "access", "sara@example.com", True, date(2026, 10, 1))
    handle(db, "rectification", "sara@example.com", True, date(2026, 10, 2), city="Hyderabad")
    handle(db, "portability", "bilal@example.com", True, date(2026, 1, 31))
    handle(db, "erasure", "bilal@example.com", False, date(2026, 10, 5))
    handle(db, "erasure", "bilal@example.com", True, date(2026, 10, 6), complex_case=True)
    print("\nCustomers table now:")
    for row in db.execute("SELECT * FROM customers"):
        print("  ", row)
    print("Audit log:")
    for row in db.execute("SELECT * FROM audit_log"):
        print("  ", row)


if __name__ == "__main__":
    main()
