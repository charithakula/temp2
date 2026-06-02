# MCP curl test commands

Reference for testing the Orders and Customers MCP servers exposed by Azure
API Management, plus the chat BFF and MCP-config REST endpoints in the local
Next.js app. Two flavors of every command: **bash** (Git Bash on Windows,
WSL, macOS, Linux) and **PowerShell** (Windows native).

> ⚠️ Replace the `KEY` value in every snippet with your own APIM subscription
> key. The one shown here is a placeholder. See [Getting the key](#getting-the-key)
> at the bottom for how to retrieve it.

---

## Set variables once

### bash

```bash
KEY="REPLACE_WITH_YOUR_APIM_SUBSCRIPTION_KEY"
ORD="https://ai-apim-1234.azure-api.net/ordersmcp/mcp"
CUST="https://ai-apim-1234.azure-api.net/customersmcp/mcp"
APP="http://localhost:3000"
```

### PowerShell

```powershell
$KEY  = "REPLACE_WITH_YOUR_APIM_SUBSCRIPTION_KEY"
$ORD  = "https://ai-apim-1234.azure-api.net/ordersmcp/mcp"
$CUST = "https://ai-apim-1234.azure-api.net/customersmcp/mcp"
$APP  = "http://localhost:3000"
```

### Required headers (apply to every MCP call)

| Header | Why |
|---|---|
| `Content-Type: application/json` | The request body is JSON-RPC |
| `Accept: application/json, text/event-stream` | APIM's MCP endpoint requires both — without `text/event-stream` you get **406 Not Acceptable** |
| `Ocp-Apim-Subscription-Key: <key>` | APIM authentication |

---

## 1. Initialize (handshake — proves auth + URL work)

### bash

```bash
curl -s -X POST "$ORD" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}'
```

### PowerShell

```powershell
curl -s -X POST "$ORD" `
  -H "Content-Type: application/json" `
  -H "Accept: application/json, text/event-stream" `
  -H "Ocp-Apim-Subscription-Key: $KEY" `
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2025-03-26\",\"capabilities\":{},\"clientInfo\":{\"name\":\"curl\",\"version\":\"1\"}}}"
```

**Expected:**

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-03-26","capabilities":{"tools":{"listChanged":true}},"serverInfo":{"name":"Azure API Management","version":"1.0.0"}}}
```

---

## 2. List tools

### Orders MCP

#### bash

```bash
curl -s -X POST "$ORD" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

#### PowerShell

```powershell
curl -s -X POST "$ORD" `
  -H "Content-Type: application/json" `
  -H "Accept: application/json, text/event-stream" `
  -H "Ocp-Apim-Subscription-Key: $KEY" `
  -d "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\",\"params\":{}}"
```

**Expected:** one tool — `getAnOrderById`.

### Customers MCP

Same command, just swap `$ORD` → `$CUST`. Expected three tools:
`getACustomerById`, `getTheOrderIDsForACustomer`, `listCustomers`.

---

## 3. Call a tool

### 3a. Orders — `getAnOrderById`

#### bash

```bash
curl -s -X POST "$ORD" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"getAnOrderById","arguments":{"id":"42"}}}'
```

#### PowerShell

```powershell
curl -s -X POST "$ORD" `
  -H "Content-Type: application/json" `
  -H "Accept: application/json, text/event-stream" `
  -H "Ocp-Apim-Subscription-Key: $KEY" `
  -d "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"getAnOrderById\",\"arguments\":{\"id\":\"42\"}}}"
```

**Expected:** `result.content[0].text` is a JSON-encoded order with
`id: "42"`, `customer: "Charith Akula"`, `total: 249.97`, etc.

### 3b. Customers — `getACustomerById`

#### bash

```bash
curl -s -X POST "$CUST" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"getACustomerById","arguments":{"id":"c-1001"}}}'
```

#### PowerShell

```powershell
curl -s -X POST "$CUST" `
  -H "Content-Type: application/json" `
  -H "Accept: application/json, text/event-stream" `
  -H "Ocp-Apim-Subscription-Key: $KEY" `
  -d "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"getACustomerById\",\"arguments\":{\"id\":\"c-1001\"}}}"
```

### 3c. Customers — `getTheOrderIDsForACustomer`

#### bash

```bash
curl -s -X POST "$CUST" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"getTheOrderIDsForACustomer","arguments":{"id":"c-1001"}}}'
```

#### PowerShell

```powershell
curl -s -X POST "$CUST" `
  -H "Content-Type: application/json" `
  -H "Accept: application/json, text/event-stream" `
  -H "Ocp-Apim-Subscription-Key: $KEY" `
  -d "{\"jsonrpc\":\"2.0\",\"id\":4,\"method\":\"tools/call\",\"params\":{\"name\":\"getTheOrderIDsForACustomer\",\"arguments\":{\"id\":\"c-1001\"}}}"
```

**Expected:** `{"customerId":"c-1001","orders":["42","43","99"]}`.

### 3d. Customers — `listCustomers` (with optional filters)

#### bash

```bash
# Filter to Gold tier, limit 5
curl -s -X POST "$CUST" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"listCustomers","arguments":{"tier":"Gold","limit":5}}}'

# No filter — all customers
curl -s -X POST "$CUST" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"listCustomers","arguments":{}}}'
```

#### PowerShell

```powershell
curl -s -X POST "$CUST" `
  -H "Content-Type: application/json" `
  -H "Accept: application/json, text/event-stream" `
  -H "Ocp-Apim-Subscription-Key: $KEY" `
  -d "{\"jsonrpc\":\"2.0\",\"id\":5,\"method\":\"tools/call\",\"params\":{\"name\":\"listCustomers\",\"arguments\":{\"tier\":\"Gold\",\"limit\":5}}}"
```

---

## 4. Pretty-print MCP results (bash + jq)

The MCP tool result is wrapped twice: `result.content[0].text` is a *string*
of JSON. Unwrap both layers:

```bash
curl -s -X POST "$CUST" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Ocp-Apim-Subscription-Key: $KEY" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"getACustomerById","arguments":{"id":"c-1001"}}}' \
  | jq -r '.result.content[0].text' \
  | jq .
```

---

## 5. Smoke-test loops

### bash — every Customers MCP tool

```bash
for name in getACustomerById getTheOrderIDsForACustomer listCustomers; do
  echo "=== $name ==="
  case $name in
    listCustomers) args='{}';;
    *)             args='{"id":"c-1001"}';;
  esac
  curl -s -X POST "$CUST" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "Ocp-Apim-Subscription-Key: $KEY" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":$args}}" \
    | jq -r '.result.content[0].text' | jq .
  echo
done
```

### PowerShell — list tools on both MCPs

```powershell
foreach ($name in 'ordersmcp','customersmcp') {
  $url = "https://ai-apim-1234.azure-api.net/$name/mcp"
  Write-Host "`n=== $name ===" -ForegroundColor Cyan
  curl -s -X POST $url `
    -H "Content-Type: application/json" `
    -H "Accept: application/json, text/event-stream" `
    -H "Ocp-Apim-Subscription-Key: $KEY" `
    -d '{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\",\"params\":{}}'
}
```

---

## 6. Underlying REST APIs (skip the MCP layer)

The same APIM gateway exposes the raw operations behind the MCP. Useful for
narrowing whether a problem is in the MCP layer or the API itself.

```bash
# Orders API
curl -s -H "Ocp-Apim-Subscription-Key: $KEY" \
  "https://ai-apim-1234.azure-api.net/orders/42"

# Customers API
curl -s -H "Ocp-Apim-Subscription-Key: $KEY" \
  "https://ai-apim-1234.azure-api.net/customers/c-1001"

curl -s -H "Ocp-Apim-Subscription-Key: $KEY" \
  "https://ai-apim-1234.azure-api.net/customers?tier=Gold&limit=5"

curl -s -H "Ocp-Apim-Subscription-Key: $KEY" \
  "https://ai-apim-1234.azure-api.net/customers/c-1001/orders"
```

If the REST call works but the MCP call fails, the issue is in the
MCP-server configuration in APIM, not the API.

---

## 7. Local Next.js endpoints

These don't need the APIM key — they're your own BFF.

### Chat (full LLM-driven turn)

```bash
curl -s -X POST "$APP/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"id":"m1","role":"user","parts":[{"type":"text","text":"Get order 42 customer only."}]}]}'
```

Response is a streaming SSE event-stream. Pipe to `grep` to see only the tool
calls and text:

```bash
curl -s -N -X POST "$APP/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"id":"m1","role":"user","parts":[{"type":"text","text":"Get order 42 customer only."}]}]}' \
  | grep -E "tool-input-available|tool-output-available|text-delta"
```

### MCP-config REST endpoints

```bash
# List all configured MCP servers
curl -s "$APP/api/mcp-servers"

# Probe an MCP endpoint without saving
curl -s -X POST "$APP/api/mcp-servers/test" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$CUST\",\"authHeader\":\"Ocp-Apim-Subscription-Key\",\"authValue\":\"$KEY\"}"

# Add a new MCP server
curl -s -X POST "$APP/api/mcp-servers" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"customers\",\"url\":\"$CUST\",\"authHeader\":\"Ocp-Apim-Subscription-Key\",\"authValue\":\"$KEY\"}"

# Update a server (PUT to /:name)
curl -s -X PUT "$APP/api/mcp-servers/customers" \
  -H "Content-Type: application/json" \
  -d '{"disabled":true}'

# Delete a server
curl -s -X DELETE "$APP/api/mcp-servers/customers"
```

---

## Common errors

| HTTP / response | Diagnosis |
|---|---|
| `404 Resource not found` | URL slug wrong (case-sensitive — `ordersmcp`, not `ordersMcp`), or MCP server not yet created in APIM |
| `401 Access denied` | Subscription key invalid, missing, or not scoped to this API/Product |
| `406 Not Acceptable` | Missing the `text/event-stream` value in the `Accept` header |
| `400` JSON-RPC error in body | Body shape wrong — check `params` matches the schema from `tools/list` |
| `200` but `error` inside body | Tool call valid but the underlying API returned an error (e.g. mock policy not saved) |

---

## Getting the key

### Azure Portal

1. Portal → your APIM (`ai-apim-1234`) → left menu → **Subscriptions**.
2. Find the row whose **Scope** covers the API you want (e.g. `Service`).
   The default is **"Built-in all-access subscription"**.
3. `⋯` (three-dot menu) → **Show/hide keys** → copy **Primary key**.

### Azure CLI

```bash
az apim subscription list \
  --resource-group ai-rg \
  --service-name ai-apim-1234 \
  --query "[].{name:displayName, scope:scope, primary:primaryKey}" \
  -o table
```

To pull a single subscription's primary key by name:

```bash
az apim subscription list \
  --resource-group ai-rg \
  --service-name ai-apim-1234 \
  --query "[?displayName=='MCPSub'].primaryKey | [0]" \
  -o tsv
```

### Key rotation (zero-downtime)

1. Regenerate **Secondary key** in the portal.
2. Switch your app/clients to the new secondary value.
3. Regenerate **Primary key**.
4. Switch back to the new primary if you prefer using primary by convention.

Both keys are always valid simultaneously, so the swap is hitless.
