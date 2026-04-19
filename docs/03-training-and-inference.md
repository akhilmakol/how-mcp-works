# Training And Inference

## MCP Topic Coverage

The bundled dataset is intentionally small, but it covers the beginner MCP concepts most people need first:

- what MCP is
- why standardization helps
- host, client, and server roles
- tools, resources, and prompts
- lifecycle and capability negotiation
- request and response flow intuition

## Example Scenarios

```mermaid
flowchart LR
    A["User asks AI IDE to inspect a project"] --> B["Host selects filesystem MCP server"]
    B --> C["Server exposes file read capability"]
    C --> D["Host uses results in the response"]
```

```mermaid
flowchart LR
    A["Host starts a session"] --> B["Client and server initialize"]
    B --> C["Capabilities are negotiated"]
    C --> D["Tools and resources become available"]
```

## Generation Pipeline

```mermaid
flowchart LR
    A["User enters an MCP question"] --> B["Encode prompt"]
    B --> C["Crop to context window"]
    C --> D["Forward pass"]
    D --> E["Take final-step logits"]
    E --> F["Apply temperature / top-k"]
    F --> G["Sample next character"]
    G --> H["Append to explanation"]
    H --> C
```

## What To Explore In The App

- Try prompts like `what is mcp: `
- Try prompts like `why mcp: `
- Try prompts like `how mcp works: `
- Compare low-temperature and high-temperature outputs
- Inspect the next-token probabilities to see how the explanation is formed
