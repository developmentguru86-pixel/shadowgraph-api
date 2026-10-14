# Paid calls with the Machine Payments Protocol

ShadowGraph sells deeper intelligence per request, without accounts or API keys, using the open [Machine Payments Protocol](https://paymentauth.org) with Stripe as the payment method. Prices: $0.50 to $5.00 per call. Nothing is charged unless your client presents a valid credential for a challenge the server issued.

## Over HTTP

1. Call the endpoint without credentials, e.g. `POST /_api/machine/intelligence` with `{"mode":"hidden_chain"}`.
2. The response is `402 Payment Required` with a `WWW-Authenticate: Payment ...` header (`method="stripe"`, `intent="charge"`, amount in cents inside the base64url `request` parameter) and an RFC 9457 problem body.
3. Your agent's wallet creates a Stripe shared payment token for exactly that challenge and builds the credential.
4. Repeat the identical request with `Authorization: Payment <base64url credential>`. Success returns `200`, the result and a `Payment-Receipt` header. A failed payment returns a fresh challenge.

```bash
curl -si -X POST https://shadowalpha.online/_api/machine/intelligence \
  -H "Content-Type: application/json" \
  -d '{"mode":"hidden_chain"}'
```

| Mode | Price |
|---|---|
| `hidden_chain` | $0.50 |
| `alpha` | $0.75 |
| `opportunity` | $1.00 |
| `global_brief` | $2.50 |
| `deep_research` | $5.00 |

## Over MCP

An unpaid `tools/call` returns JSON-RPC error `-32042` with `error.data.challenges`:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32042,
    "message": "Payment Required",
    "data": {
      "httpStatus": 402,
      "challenges": [{
        "id": "…",
        "realm": "shadowalpha.online",
        "method": "stripe",
        "intent": "charge",
        "request": { "amount": "50", "currency": "usd" },
        "description": "ShadowGraph hidden_chain intelligence",
        "expires": "…"
      }]
    }
  }
}
```

Retry the identical `tools/call` with the credential in `params._meta["org.paymentauth/credential"]` (`{ "challenge": <as received>, "payload": { "spt": "spt_…" } }`). The receipt comes back in `result._meta["org.paymentauth/receipt"]`. Error `-32043` means the payment could not be verified.

Results are probabilistic intelligence: inferred relationships and statistical lead/lag are hypotheses, not proof, and not investment advice.
