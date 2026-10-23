# DAX Measures Reference: Anti-Bullwhip & DDMRP Buffer Dashboard

Create a dedicated table named `_Measures` in Power BI (`Home` -> `Enter Data` -> Name it `_Measures` -> click `Load`). Place all the measures below inside this table.

---

## 1. Base Volume & Financial Measures

### `Total Customer Demand Qty`
```dax
Total Customer Demand Qty = 
SUM(Fact_CustomerOrders[OrderQty])
```

### `Gross Revenue ($)`
```dax
Gross Revenue ($) = 
SUM(Fact_CustomerOrders[GrossRevenue])
```

### `Total Replenishment PO Qty`
```dax
Total Replenishment PO Qty = 
SUM(Fact_PurchaseOrders[OrderedUnits])
```

### `Total Procurement Spend ($)`
```dax
Total Procurement Spend ($) = 
SUM(Fact_PurchaseOrders[TotalCost])
```

### `Current On-Hand Units`
```dax
Current On-Hand Units = 
VAR MaxDate = MAX(Fact_DailyInventory[Date])
RETURN
CALCULATE(
    SUM(Fact_DailyInventory[OnHandUnits]),
    Fact_DailyInventory[Date] = MaxDate
)
```

---

## 2. Supplier Lead-Time Volatility & Reliability

### `Contracted Lead Time (Avg)`
```dax
Contracted Lead Time (Avg) = 
AVERAGE(Fact_PurchaseOrders[ContractedLeadTimeDays])
```

### `Actual Lead Time (Avg)`
```dax
Actual Lead Time (Avg) = 
AVERAGE(Fact_PurchaseOrders[ActualLeadTimeDays])
```

### `Lead Time Variance (Days)`
```dax
Lead Time Variance (Days) = 
[Actual Lead Time (Avg)] - [Contracted Lead Time (Avg)]
```

### `Lead Time Standard Deviation (Volatility)`
```dax
Lead Time StDev = 
COALESCE(
    STDEV.S(Fact_PurchaseOrders[ActualLeadTimeDays]),
    0
)
```

### `On-Time Delivery Rate (OTIF %)`
```dax
On-Time Delivery % = 
DIVIDE(
    CALCULATE(COUNTROWS(Fact_PurchaseOrders), Fact_PurchaseOrders[DeliveryStatus] = "On-Time"),
    COUNTROWS(Fact_PurchaseOrders),
    0
)
```

### `Severe Delay Rate (>14 Days)`
```dax
Severe Delay % = 
DIVIDE(
    CALCULATE(COUNTROWS(Fact_PurchaseOrders), Fact_PurchaseOrders[DeliveryStatus] = "Severe Delay (>14d)"),
    COUNTROWS(Fact_PurchaseOrders),
    0
)
```

---

## 3. The Bullwhip Effect Amplification Index

The Bullwhip Effect occurs when monthly order variance placed to suppliers significantly exceeds monthly customer demand variance.

### `Monthly Customer Demand Variance`
```dax
Monthly Demand Variance = 
VAR MonthlyTable = 
    ADDCOLUMNS(
        SUMMARIZE(Fact_CustomerOrders, Dim_Calendar[YearMonth]),
        "@MonthlyDemand", [Total Customer Demand Qty]
    )
RETURN
VARX.S(MonthlyTable, [@MonthlyDemand])
```

### `Monthly Replenishment Order Variance`
```dax
Monthly PO Variance = 
VAR MonthlyTable = 
    ADDCOLUMNS(
        SUMMARIZE(Fact_PurchaseOrders, Dim_Calendar[YearMonth]),
        "@MonthlyPO", [Total Replenishment PO Qty]
    )
RETURN
VARX.S(MonthlyTable, [@MonthlyPO])
```

### `Bullwhip Amplification Ratio`
*(Values > 1.2 indicate noticeable demand distortion; values > 2.0 indicate severe panic bullwhip)*
```dax
Bullwhip Amplification Ratio = 
VAR DemandVar = [Monthly Demand Variance]
VAR POVar = [Monthly PO Variance]
RETURN
IF(
    DemandVar > 0,
    DIVIDE(POVar, DemandVar, 1.0),
    BLANK()
)
```

---

## 4. DDMRP Buffer Health & Capital Optimization

### `Buffer Penetration %`
```dax
Buffer Penetration % = 
VAR CurrentStock = [Current On-Hand Units]
VAR TargetBuffer = SUM(Dim_Product[YellowBufferTarget])
RETURN
DIVIDE(CurrentStock, TargetBuffer, 0)
```

### `Trapped Working Capital ($)`
*(Working capital locked in excess inventory beyond the top of the green buffer)*
```dax
Trapped Working Capital ($) = 
VAR MaxDate = MAX(Fact_DailyInventory[Date])
RETURN
CALCULATE(
    SUM(Fact_DailyInventory[TrappedWorkingCapital]),
    Fact_DailyInventory[Date] = MaxDate
)
```

### `Revenue at Risk ($)`
*(Projected lost revenue due to stockouts or buffer starvation in the red zone)*
```dax
Revenue at Risk ($) = 
VAR MaxDate = MAX(Fact_DailyInventory[Date])
RETURN
CALCULATE(
    SUM(Fact_DailyInventory[RevenueAtRisk]),
    Fact_DailyInventory[Date] = MaxDate
)
```

### `Stockout Incident Rate %`
```dax
Stockout Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(Fact_DailyInventory), Fact_DailyInventory[IsStockout] = 1),
    COUNTROWS(Fact_DailyInventory),
    0
)
```

### `Buffer Status Conditional Hex Color`
*(Use this measure for conditional background formatting on tables and cards)*
```dax
Buffer Color Hex = 
VAR CurrentPen = [Buffer Penetration %]
RETURN
SWITCH(
    TRUE(),
    CurrentPen < 0.33, "#DC2626", // Red: Critical Danger
    CurrentPen <= 1.00, "#F59E0B", // Amber: Target Operating Buffer
    "#16A34A"                      // Green: Healthy / Overstocked
)
```

---

## 5. What-If Scenario: Working Capital Unlocked

*Prerequisite: Create a What-If Numeric Range parameter in Power BI:*
`Modeling` -> `New Parameter` -> `Numeric Range`:
* Name: `Variance Reduction %`
* Minimum: `0`
* Maximum: `50`
* Increment: `5`
* Default: `20`

### `Simulated Capital Unlocked ($)`
```dax
Simulated Capital Unlocked ($) = 
VAR ReductionPct = DIVIDE('Variance Reduction %'[Variance Reduction % Value], 100, 0)
VAR CurrentTrapped = [Trapped Working Capital ($)]
RETURN
CurrentTrapped * ReductionPct
```
