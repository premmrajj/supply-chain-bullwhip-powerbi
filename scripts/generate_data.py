import csv
import random
import datetime
import os

random.seed(42)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(BASE_DIR, exist_ok=True)

START_DATE = datetime.date(2025, 1, 1)
END_DATE = datetime.date(2026, 10, 15)

# 1. Dim_Calendar
calendar_rows = []
curr = START_DATE
while curr <= END_DATE:
    calendar_rows.append({
        "Date": curr.strftime("%Y-%m-%d"),
        "DateKey": int(curr.strftime("%Y%m%d")),
        "Year": curr.year,
        "Quarter": f"Q{((curr.month - 1) // 3) + 1}",
        "YearQuarter": f"{curr.year}-Q{((curr.month - 1) // 3) + 1}",
        "Month": curr.month,
        "MonthName": curr.strftime("%B"),
        "YearMonth": curr.strftime("%Y-%m"),
        "DayOfMonth": curr.day,
        "DayOfWeek": curr.strftime("%A"),
        "IsWeekend": 1 if curr.weekday() >= 5 else 0
    })
    curr += datetime.timedelta(days=1)

with open(f"{BASE_DIR}\\Dim_Calendar.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(calendar_rows[0].keys()))
    writer.writeheader()
    writer.writerows(calendar_rows)

# 2. Dim_Supplier
suppliers = [
    {"SupplierID": "SUP-001", "SupplierName": "Apex Silicon Global", "Country": "Taiwan", "Region": "East Asia", "ContractedLeadTimeDays": 45, "ReliabilityTier": "Tier 3 - High Risk", "VarianceProfile": "High", "MeanDelay": 12, "StdevDelay": 9},
    {"SupplierID": "SUP-002", "SupplierName": "Shenzhen Precision Micro", "Country": "China", "Region": "East Asia", "ContractedLeadTimeDays": 30, "ReliabilityTier": "Tier 3 - High Risk", "VarianceProfile": "High", "MeanDelay": 8, "StdevDelay": 7},
    {"SupplierID": "SUP-003", "SupplierName": "Kyoto Advanced Components", "Country": "Japan", "Region": "East Asia", "ContractedLeadTimeDays": 21, "ReliabilityTier": "Tier 1 - Strategic", "VarianceProfile": "Low", "MeanDelay": 0, "StdevDelay": 1.5},
    {"SupplierID": "SUP-004", "Vanguard Power Systems", "Country": "United States", "Region": "North America", "ContractedLeadTimeDays": 14, "ReliabilityTier": "Tier 1 - Strategic", "VarianceProfile": "Low", "MeanDelay": 0.5, "StdevDelay": 1.8},
    {"SupplierID": "SUP-005", "SupplierName": "Nordic Sensor Dynamics", "Country": "Germany", "Region": "Europe", "ContractedLeadTimeDays": 28, "ReliabilityTier": "Tier 2 - Preferred", "VarianceProfile": "Medium", "MeanDelay": 3, "StdevDelay": 4},
    {"SupplierID": "SUP-006", "SupplierName": "Pacific Precision Mold", "Country": "Vietnam", "Region": "Southeast Asia", "ContractedLeadTimeDays": 18, "ReliabilityTier": "Tier 2 - Preferred", "VarianceProfile": "Medium", "MeanDelay": 2, "StdevDelay": 3.5},
    {"SupplierID": "SUP-007", "SupplierName": "Seoul Semiconductor Works", "Country": "South Korea", "Region": "East Asia", "ContractedLeadTimeDays": 35, "ReliabilityTier": "Tier 3 - High Risk", "VarianceProfile": "High", "MeanDelay": 9, "StdevDelay": 8},
    {"SupplierID": "SUP-008", "SupplierName": "Atlas Alloy & Chassis", "Country": "Mexico", "Region": "North America", "ContractedLeadTimeDays": 10, "ReliabilityTier": "Tier 1 - Strategic", "VarianceProfile": "Low", "MeanDelay": 0, "StdevDelay": 1.2}
]
# Fix Vanguard name key
suppliers[3]["SupplierName"] = "Vanguard Power Systems"

with open(f"{BASE_DIR}\\Dim_Supplier.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(suppliers[0].keys()))
    writer.writeheader()
    writer.writerows(suppliers)

# 3. Dim_Product
products_def = [
    ("SKU-MCU-101", "Dual-Core 32-bit Cortex MCU", "Semiconductors", 28.50, 52.00, "SUP-001", 120, 350, 700),
    ("SKU-MCU-102", "Ultra-Low Power IoT MCU", "Semiconductors", 18.20, 36.00, "SUP-001", 150, 400, 850),
    ("SKU-MCU-103", "Automotive Grade Controller", "Semiconductors", 65.00, 118.00, "SUP-007", 80, 240, 500),
    ("SKU-MCU-104", "Industrial DSP SoC 400MHz", "Semiconductors", 95.00, 168.00, "SUP-007", 60, 180, 380),
    ("SKU-MCU-105", "BLE 5.3 RF SoC Integrated", "Semiconductors", 14.80, 31.00, "SUP-002", 200, 550, 1100),
    ("SKU-MCU-106", "High-Voltage Gate Driver IC", "Semiconductors", 22.00, 42.00, "SUP-002", 140, 380, 800),

    ("SKU-PWR-201", "24V 15A DIN-Rail Power Supply", "Power Modules", 48.00, 89.00, "SUP-004", 75, 220, 450),
    ("SKU-PWR-202", "48V Telecom Rectifier Module", "Power Modules", 125.00, 219.00, "SUP-004", 40, 120, 260),
    ("SKU-PWR-203", "DC-DC Buck Converter 5V/10A", "Power Modules", 12.50, 26.00, "SUP-003", 220, 600, 1250),
    ("SKU-PWR-204", "Li-Ion BMS Protection Board", "Power Modules", 32.00, 62.00, "SUP-002", 110, 320, 680),
    ("SKU-PWR-205", "Isolated IGBT Gate Power Pack", "Power Modules", 54.00, 98.00, "SUP-003", 65, 190, 400),
    ("SKU-PWR-206", "Compact AC/DC Converter 12V", "Power Modules", 19.50, 38.00, "SUP-004", 160, 460, 950),

    ("SKU-SEN-301", "Tri-Axis MEMS Accelerometer", "Sensors", 8.40, 19.50, "SUP-005", 250, 700, 1400),
    ("SKU-SEN-302", "Differential Pressure Transducer", "Sensors", 44.00, 84.00, "SUP-005", 70, 200, 420),
    ("SKU-SEN-303", "Infrared Thermal Array Sensor", "Sensors", 78.00, 145.00, "SUP-003", 45, 130, 280),
    ("SKU-SEN-304", "Precision PT100 RTD Probe", "Sensors", 24.00, 49.00, "SUP-005", 130, 360, 750),
    ("SKU-SEN-305", "Optical TOF Distance Sensor", "Sensors", 36.50, 72.00, "SUP-003", 90, 260, 550),
    ("SKU-SEN-306", "Hall-Effect Current Sensor 50A", "Sensors", 16.00, 34.00, "SUP-005", 180, 500, 1050),

    ("SKU-ENC-401", "IP67 Die-Cast Aluminum Enclosure", "Enclosures", 35.00, 68.00, "SUP-008", 90, 260, 520),
    ("SKU-ENC-402", "19-inch 2U Rackmount Steel Chassis", "Enclosures", 82.00, 148.00, "SUP-008", 40, 110, 230),
    ("SKU-ENC-403", "Vented Polycarbonate Housing", "Enclosures", 11.20, 24.00, "SUP-006", 210, 600, 1200),
    ("SKU-ENC-404", "Extruded Heatsink Fin 150mm", "Enclosures", 9.80, 21.00, "SUP-006", 240, 680, 1350),
    ("SKU-ENC-405", "NEMA 4X Stainless Steel Box", "Enclosures", 110.00, 195.00, "SUP-008", 30, 85, 180),
    ("SKU-ENC-406", "Molded Silicon Seal & Gasket Kit", "Enclosures", 4.50, 11.00, "SUP-006", 350, 1000, 2100)
]

products = []
for p in products_def:
    products.append({
        "ProductSKU": p[0], "ProductName": p[1], "Category": p[2],
        "UnitCost": p[3], "SellingPrice": p[4], "PrimarySupplierID": p[5],
        "RedBufferMin": p[6], "YellowBufferTarget": p[7], "GreenBufferMax": p[8]
    })

with open(f"{BASE_DIR}\\Dim_Product.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(products[0].keys()))
    writer.writeheader()
    writer.writerows(products)

sup_lookup = {s["SupplierID"]: s for s in suppliers}

sku_demand_params = {}
for p in products:
    daily_mean = p["YellowBufferTarget"] / 14.0
    sku_demand_params[p["ProductSKU"]] = {"mean": daily_mean, "stdev": daily_mean * 0.22}

customer_orders = []
purchase_orders = []
daily_inventory = []

current_inventory = {}
pending_pos = []
order_counter = 100000
po_counter = 500000

for p in products:
    current_inventory[p["ProductSKU"]] = int(p["YellowBufferTarget"] * 1.15)

days_since_last_po = {p["ProductSKU"]: 10 for p in products}

curr_date = START_DATE

while curr_date <= END_DATE:
    date_str = curr_date.strftime("%Y-%m-%d")
    date_key = int(curr_date.strftime("%Y%m%d"))
    is_weekend = curr_date.weekday() >= 5
    
    arrivals = [po for po in pending_pos if po["ActualDeliveryDate"] == curr_date]
    for arr in arrivals:
        current_inventory[arr["ProductSKU"]] += arr["OrderedUnits"]
    pending_pos = [po for po in pending_pos if po["ActualDeliveryDate"] != curr_date]

    month = curr_date.month
    season_factor = 1.18 if month in [10, 11, 12] else (1.06 if month in [6, 7] else 0.95)

    for p in products:
        sku = p["ProductSKU"]
        days_since_last_po[sku] += 1
        day_mult = 0.35 if is_weekend else 1.0
        params = sku_demand_params[sku]
        
        raw_demand = random.gauss(params["mean"] * season_factor * day_mult, params["stdev"])
        daily_demand = max(0, int(round(raw_demand)))
        
        if daily_demand > 0:
            num_orders = 1 if daily_demand < 15 else random.randint(1, 3)
            rem = daily_demand
            for o_i in range(num_orders):
                qty = rem if o_i == num_orders - 1 else random.randint(1, max(1, rem // 2))
                rem -= qty
                order_counter += 1
                customer_orders.append({
                    "OrderID": f"ORD-{order_counter}", "DateKey": date_key, "OrderDate": date_str,
                    "ProductSKU": sku, "CustomerSegment": random.choice(["Enterprise OEM", "Tier-1 Integrator", "Distributor Network"]),
                    "OrderQty": qty, "UnitPrice": p["SellingPrice"], "GrossRevenue": round(qty * p["SellingPrice"], 2)
                })

        unfulfilled = 0
        if current_inventory[sku] >= daily_demand:
            current_inventory[sku] -= daily_demand
        else:
            unfulfilled = daily_demand - current_inventory[sku]
            current_inventory[sku] = 0

        on_hand = current_inventory[sku]
        on_order = sum(po["OrderedUnits"] for po in pending_pos if po["ProductSKU"] == sku)
        net_stock = on_hand + on_order
        
        should_reorder = False
        mult = 1.0
        
        # Panic buy in Red zone
        if on_hand <= p["RedBufferMin"] and days_since_last_po[sku] >= 6 and net_stock < p["YellowBufferTarget"] * 1.5:
            should_reorder = True
            mult = random.uniform(1.35, 1.8)
        # Routine replenishment
        elif net_stock < p["YellowBufferTarget"] and days_since_last_po[sku] >= 12:
            should_reorder = True
            mult = random.uniform(1.0, 1.25)
        # Periodic cycle reorder for reliable categories (creating healthy overstock in stable parts)
        elif days_since_last_po[sku] >= 20 and p["Category"] in ["Enclosures", "Power Modules"] and net_stock < p["GreenBufferMax"] * 0.95:
            should_reorder = True
            mult = random.uniform(1.1, 1.35)

        if should_reorder:
            days_since_last_po[sku] = 0
            sup = sup_lookup[p["PrimarySupplierID"]]
            needed = (p["YellowBufferTarget"] * 1.35) - net_stock + (params["mean"] * sup["ContractedLeadTimeDays"] * 0.4)
            po_qty = int(max(20, round(needed * mult)))
            
            contracted_lt = sup["ContractedLeadTimeDays"]
            delay = random.gauss(sup["MeanDelay"], sup["StdevDelay"])
            actual_lt = max(3, int(round(contracted_lt + delay)))
            
            promised_date = curr_date + datetime.timedelta(days=contracted_lt)
            actual_date = curr_date + datetime.timedelta(days=actual_lt)
            
            po_counter += 1
            po_id = f"PO-{po_counter}"
            delay_days = max(0, (actual_date - promised_date).days)
            if delay_days == 0:
                del_status = "On-Time"
            elif delay_days <= 7:
                del_status = "Minor Delay (1-7d)"
            elif delay_days <= 14:
                del_status = "Moderate Delay (8-14d)"
            else:
                del_status = "Severe Delay (>14d)"
                
            purchase_orders.append({
                "PO_ID": po_id, "OrderDateKey": date_key, "OrderDate": date_str,
                "PromisedDeliveryDateKey": int(promised_date.strftime("%Y%m%d")),
                "PromisedDeliveryDate": promised_date.strftime("%Y-%m-%d"),
                "ActualDeliveryDateKey": int(actual_date.strftime("%Y%m%d")),
                "ActualDeliveryDate": actual_date.strftime("%Y-%m-%d"),
                "SupplierID": p["PrimarySupplierID"], "ProductSKU": sku,
                "OrderedUnits": po_qty, "UnitCost": p["UnitCost"],
                "TotalCost": round(po_qty * p["UnitCost"], 2),
                "ContractedLeadTimeDays": contracted_lt,
                "ActualLeadTimeDays": actual_lt,
                "VarianceDays": actual_lt - contracted_lt,
                "DeliveryStatus": del_status
            })
            pending_pos.append({
                "PO_ID": po_id, "ProductSKU": sku, "ActualDeliveryDate": actual_date, "OrderedUnits": po_qty
            })

        # Buffer Classification
        if on_hand <= p["RedBufferMin"]:
            buffer_zone = "Red (Danger / Stockout Risk)"
        elif on_hand <= p["YellowBufferTarget"]:
            buffer_zone = "Yellow (Optimal Buffer)"
        elif on_hand <= p["GreenBufferMax"]:
            buffer_zone = "Light Green (Healthy Safety)"
        else:
            buffer_zone = "Dark Green (Overstocked / Trapped Cash)"

        trapped_cash = max(0, on_hand - p["GreenBufferMax"]) * p["UnitCost"]
        
        # Overstock valuation in stable categories
        if on_hand > p["GreenBufferMax"] * 0.85 and p["Category"] in ["Enclosures", "Power Modules", "Sensors"]:
            trapped_cash = max(trapped_cash, (on_hand - p["GreenBufferMax"] * 0.85) * p["UnitCost"])

        if unfulfilled > 0:
            rev_risk = unfulfilled * p["SellingPrice"]
        elif on_hand <= p["RedBufferMin"]:
            rev_risk = (p["RedBufferMin"] - on_hand + 8) * p["SellingPrice"] * 0.50
        else:
            rev_risk = 0.0

        daily_inventory.append({
            "DateKey": date_key, "Date": date_str, "ProductSKU": sku,
            "OnHandUnits": on_hand, "OnOrderUnits": on_order,
            "NetStockUnits": on_hand + on_order, "BufferZone": buffer_zone,
            "IsStockout": 1 if on_hand == 0 else 0,
            "TrappedWorkingCapital": round(trapped_cash, 2),
            "RevenueAtRisk": round(rev_risk, 2)
        })

    curr_date += datetime.timedelta(days=1)

with open(f"{BASE_DIR}\\Fact_CustomerOrders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(customer_orders[0].keys()))
    writer.writeheader()
    writer.writerows(customer_orders)

with open(f"{BASE_DIR}\\Fact_PurchaseOrders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(purchase_orders[0].keys()))
    writer.writeheader()
    writer.writerows(purchase_orders)

with open(f"{BASE_DIR}\\Fact_DailyInventory.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(daily_inventory[0].keys()))
    writer.writeheader()
    writer.writerows(daily_inventory)

last_day = [r for r in daily_inventory if r["Date"] == "2026-10-15"]
tc = sum(r["TrappedWorkingCapital"] for r in last_day)
rr = sum(r["RevenueAtRisk"] for r in last_day)
print(f"Trapped Capital on Max Date: ${tc:,.2f}")
print(f"Revenue at Risk on Max Date: ${rr:,.2f}")
print(f"Red: {sum(1 for r in last_day if 'Red' in r['BufferZone'])}, Yellow: {sum(1 for r in last_day if 'Yellow' in r['BufferZone'])}, Green: {sum(1 for r in last_day if 'Green' in r['BufferZone'])}")
