# Power BI Visual & Dashboard Design Guide

Follow this guide to build the 3-page interactive dashboard in Power BI Desktop.

---

## Step 1: Data Ingestion & Model Relationships

1. Open Power BI Desktop.
2. Click **Get Data** -> **Text/CSV**, and import all 6 CSV files from:
   `C:\Users\hp\.gemini\antigravity\scratch\supply_chain_bullwhip_powerbi\`
3. Verify data types:
   * Dates: `Date` type
   * Keys (`DateKey`): `Whole Number`
   * Quantities, Days: `Whole Number`
   * UnitCost, SellingPrice, Revenues, Costs: `Fixed Decimal Number` ($)
4. Go to **Model View** and establish **1-to-Many (`1:*`) Single Direction** relationships:

| From Dimension (1) | To Fact Table (*) | Key Field |
| :--- | :--- | :--- |
| `Dim_Calendar` | `Fact_CustomerOrders` | `DateKey` -> `DateKey` |
| `Dim_Calendar` | `Fact_PurchaseOrders` | `DateKey` -> `OrderDateKey` *(Active)* |
| `Dim_Calendar` | `Fact_DailyInventory` | `DateKey` -> `DateKey` |
| `Dim_Product` | `Fact_CustomerOrders` | `ProductSKU` -> `ProductSKU` |
| `Dim_Product` | `Fact_PurchaseOrders` | `ProductSKU` -> `ProductSKU` |
| `Dim_Product` | `Fact_DailyInventory` | `ProductSKU` -> `ProductSKU` |
| `Dim_Supplier` | `Fact_PurchaseOrders` | `SupplierID` -> `SupplierID` |
| `Dim_Supplier` | `Dim_Product` | `SupplierID` -> `PrimarySupplierID` |

5. Apply Theme: Go to **View** -> **Themes** -> **Browse for themes** -> select `theme.json`.

---

## Page 1: Executive Buffer & Capital Risk

> **Purpose:** Give supply chain executives an instant diagnostic of stockout vulnerabilities and working capital trapped in excess safety buffers.

### Layout & Visuals:
1. **Header Banner (Dark Navy `#0F2942`):**
   * Title: **"Supply Chain Resilience & Buffer Penetration Command Center"**
   * Subtitle: *"Demand-Driven Material Requirements Planning (DDMRP) & Working Capital Diagnostics"*
   * Global Slicers: `Dim_Product[Category]`, `Dim_Supplier[Region]`, `Dim_Calendar[YearQuarter]`

2. **Top KPI Cards (Row of 4 Cards):**
   * **Card 1:** `Trapped Working Capital ($)` (Formatted as Currency, e.g., `$184K`)
   * **Card 2:** `Revenue at Risk ($)` (Formatted as Currency, Red callout `#DC2626`)
   * **Card 3:** `Stockout Rate %` (Formatted as `0.0%`)
   * **Card 4:** `On-Time Delivery %` (Formatted as `0.0%`)

3. **Middle Left Visual: Buffer Zone Distribution (Stacked 100% Bar Chart)**
   * **Y-Axis:** `Dim_Product[Category]`
   * **X-Axis:** `Fact_DailyInventory[OnHandUnits]`
   * **Legend:** `Fact_DailyInventory[BufferZone]`
   * *Insight:* Instantly highlights which categories (e.g. Semiconductors) are running dry in the Red Zone vs. overstocked in the Green Zone.

4. **Middle Right Visual: Inbound Supplier Delay Breakdown (Donut Chart)**
   * **Legend:** `Fact_PurchaseOrders[DeliveryStatus]`
   * **Values:** `Fact_PurchaseOrders[PO_ID]` (Count)
   * *Colors:* On-Time (`#16A34A`), Minor Delay (`#F59E0B`), Moderate Delay (`#EA580C`), Severe Delay (`#DC2626`).

5. **Bottom Visual: Critical Red-Zone Vulnerability Matrix (Table)**
   * **Fields:** `Dim_Product[ProductSKU]`, `Dim_Product[ProductName]`, `Dim_Supplier[SupplierName]`, `[Current On-Hand Units]`, `Dim_Product[RedBufferMin]`, `[Buffer Penetration %]`, `[Revenue at Risk ($)]`
   * **Conditional Formatting:** Apply background color on `[Buffer Penetration %]` using field value `[Buffer Color Hex]`.

---

## Page 2: Bullwhip Diagnostics & Demand Distortion

> **Purpose:** Visually expose the classic Bullwhip phenomenon—showing how smooth customer buying patterns turn into chaotic supplier order spikes.

### Layout & Visuals:
1. **Signature Visual: The Bullwhip Oscillation (Dual-Axis Line Chart)**
   * **X-Axis:** `Dim_Calendar[YearMonth]`
   * **Line 1 (Left Y-Axis):** `[Total Customer Demand Qty]` (Format: Smooth dark teal/blue line `#0284C7`)
   * **Line 2 (Right Y-Axis):** `[Total Replenishment PO Qty]` (Format: Dashed or jagged red/navy line `#0F2942`)
   * *Story:* The smooth demand line juxtaposed against wild swings in purchase orders proves the presence of the Bullwhip Effect!

2. **Left Diagnostic Visual: Bullwhip Amplification Index by Category (Clustered Bar Chart)**
   * **Y-Axis:** `Dim_Product[Category]`
   * **X-Axis:** `[Bullwhip Amplification Ratio]`
   * **Reference Line:** Add a constant line at `1.0` (Threshold where ordering matches demand).
   * *Insight:* Semiconductors show the highest ratio (> 2.5x), while Enclosures show minimal distortion (~1.1x).

3. **Right Diagnostic Visual: Root-Cause Decomposition Tree**
   * **Analyze:** `[Total Replenishment PO Qty]`
   * **Explain By:** `Dim_Product[Category]`, `Dim_Supplier[ReliabilityTier]`, `Dim_Supplier[SupplierName]`, `Dim_Product[ProductSKU]`.

---

## Page 3: Supplier Volatility Scorecard & What-If Optimizer

> **Purpose:** Identify unreliable vendors causing lead time variance and simulate the financial return of stabilizing supplier lead times.

### Layout & Visuals:
1. **Interactive What-If Scenario Section (Top Left Callout Box):**
   * **Slicer:** `Variance Reduction %` (Slider from 0% to 50%)
   * **Simulated KPI Card:** `[Simulated Capital Unlocked ($)]`
   * *Caption:* *"Reducing supplier lead time variance unlocks safety stock cash back into operational cash flow."*

2. **Lead Time Volatility Quadrant Matrix (Scatter Plot):**
   * **X-Axis:** `[Lead Time Variance (Days)]` (Delays beyond promise)
   * **Y-Axis:** `[Lead Time StDev]` (Unpredictability / Volatility)
   * **Size / Details:** `Dim_Supplier[SupplierName]`
   * **Color:** `Dim_Supplier[ReliabilityTier]`
   * *Quadrants:* 
     * Bottom-Left: Strategic Partners (Low variance, on-time).
     * Top-Right: Chronic Bottlenecks (High variance, erratic delays $\rightarrow$ primary drivers of panic buying).

3. **Bottom Matrix: Supplier Performance & Penalty Benchmark (Table)**
   * **Columns:** `Dim_Supplier[SupplierName]`, `Dim_Supplier[Country]`, `[Contracted Lead Time (Avg)]`, `[Actual Lead Time (Avg)]`, `[Lead Time StDev]`, `[On-Time Delivery %]`, `[Severe Delay %]`, `[Total Procurement Spend ($)]`.
