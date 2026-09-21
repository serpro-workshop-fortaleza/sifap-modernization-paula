# Cost estimation reference

Formulas and patterns for converting Azure unit prices into monthly and annual cost estimates.

## Standard time-based calculations

### Hours per month

Azure uses **730 hours/month** as the standard billing period (365 days × 24 hours / 12 months).

```text
Monthly cost = hourly unit price × 730
Annual cost  = monthly cost × 12
```

### Common multipliers

| Period | Hours | Calculation |
|--------|-------|-------------|
| 1 hour | 1 | Unit price |
| 1 day | 24 | Unit price × 24 |
| 1 week | 168 | Unit price × 168 |
| 1 month | 730 | Unit price × 730 |
| 1 year | 8,760 | Unit price × 8,760 |

## Service-specific formulas

### Virtual machines (compute)

```text
Monthly cost = hourly price × 730
```

For VMs running only during business hours (8 h/day, 22 days/month):

```text
Monthly cost = hourly price × 176
```

### Azure Functions

```text
Execution cost = price per execution × execution count
Compute cost = price per GB-s × (memory in GB × execution time in seconds × execution count)
Monthly total = execution cost + compute cost
```

Free allowance: 1 million executions and 400,000 GB-s per month.

### Azure Blob Storage

```text
Storage cost = price per GB × storage in GB
Transaction cost = price per 10,000 operations × (operations / 10,000)
Egress cost = price per GB × egress in GB
Monthly total = storage cost + transaction cost + egress cost
```

### Azure Cosmos DB

#### Provisioned throughput

```text
Monthly cost = (RU/s / 100) × price per 100 RU/s × 730
```

#### Serverless

```text
Monthly cost = (total RUs consumed / 1,000,000) × price per 1 million RUs
```

### Azure SQL Database

#### DTU model

```text
Monthly cost = price per DTU × DTUs × 730
```

#### vCore model

```text
Monthly cost = vCore price × vCores × 730 + storage price per GB × storage in GB
```

### Azure Kubernetes Service (AKS)

```text
Monthly cost = node VM price × 730 × node count
```

The control plane is free in the Standard tier.

### Azure App Service

```text
Monthly cost = plan price × 730 (for hourly-priced plans)
```

Or use the fixed monthly price for fixed-tier plans.

### Azure OpenAI

```text
Monthly cost = (input tokens / 1,000) × input price per thousand tokens
              + (output tokens / 1,000) × output price per thousand tokens
```

## Reservation versus pay-as-you-go comparison

When presenting pricing options, always show the comparison:

```markdown
| Pricing model | Monthly cost | Annual cost | Savings versus pay-as-you-go (PAYG) |
|---------------|-------------|-------------|------------------|
| Pay-as-you-go | $X | $Y | N/A |
| 1-year reservation | $A | $B | Z% |
| 3-year reservation | $C | $D | W% |
| Savings plan (1 year) | $E | $F | V% |
| Savings plan (3 years) | $G | $H | U% |
| Spot (if available) | $I | N/A | T% |
```

Savings percentage formula:

```text
Savings % = ((PAYG price - reserved price) / PAYG price) × 100
```

## Cost summary table template

Always present results in this format:

```markdown
| Service | SKU | Region | Unit price | Unit | Monthly estimate | Annual estimate |
|---------|-----|--------|-----------|------|-------------|-------------|
| Virtual Machines | Standard_D4s_v5 | East US | $0.192/h | 1 hour | $140.16 | $1,681.92 |
```

## Tips

- Always clarify the **usage pattern** before estimating (24 hours a day, business hours, or sporadic use).
- For **storage**, ask about the expected data volume and access patterns.
- For **databases**, ask about throughput requirements (RU/s, DTUs, or vCores).
- For **serverless** services, ask about expected invocation count and duration.
- Round displayed values to two decimal places.
- State that prices are in **USD** unless otherwise specified.
