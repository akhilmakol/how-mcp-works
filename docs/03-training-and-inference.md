# Training And Inference

## Banking Topic Coverage

The bundled dataset is intentionally small, but it covers the beginner banking concepts most people need first:

- checking and savings accounts
- deposits and withdrawals
- interest and repayment
- loans and credit risk
- liquidity and reserves
- payment flows

## Example Scenarios

```mermaid
flowchart LR
    A["Maria gets paid"] --> B["Salary enters checking account"]
    B --> C["Bills are paid"]
    C --> D["Remaining cash may move to savings"]
```

```mermaid
flowchart LR
    A["Borrower requests a loan"] --> B["Bank reviews income and risk"]
    B --> C["Loan is approved or declined"]
    C --> D["Approved loan is repaid with interest"]
```

## Generation Pipeline

```mermaid
flowchart LR
    A["User enters a banking prompt"] --> B["Encode prompt"]
    B --> C["Crop to context window"]
    C --> D["Forward pass"]
    D --> E["Take final-step logits"]
    E --> F["Apply temperature / top-k"]
    F --> G["Sample next character"]
    G --> H["Append to explanation"]
    H --> C
```

## What To Explore In The App

- Try prompts like `banking concept: interest`
- Try prompts like `scenario: a customer compares checking and savings`
- Compare low-temperature and high-temperature outputs
- Inspect the next-token probabilities to see how the explanation is formed
