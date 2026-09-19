# Payments, orders, and commerce workflows

## Model the transaction

Load this for WooCommerce extensions and other checkout, booking-payment, subscription, refund, or fulfillment features. Map customer and guest checkout, cart/session, order, merchant/staff, external gateway, and any vendor or tenant. Derive rules for who may read or mutate an order, which amount/currency/line items belong to it, what confirms payment, and when fulfillment or refund may occur. A posted order ID or order key does not by itself settle ownership or payment authority. [WooCommerce knowledge](../knowledge/wordpress/woocommerce.md) provides version-sensitive platform semantics, including order storage and guest flows; verify the installed configuration.

## Trace money and state across requests

Follow **cart inputs → server price/discount computation → order creation → payment intent/reference → callback or webhook → order/status update → fulfillment/refund**. At every handoff, record who controls amount, currency, customer ID, order key, gateway reference, coupon, quantity, status, and destination account. Ask whether the payment result is bound to the intended order and merchant, whether a client can report paid status, whether duplicate/stale events are idempotent, and whether an out-of-order cancellation or refund can leave inconsistent obligations. Guest and logged-in order paths may use different identity or verification rules; test both when in scope.

Order ownership, callback authenticity, and business-state validity are separate checks. An authentic gateway event can still name the wrong local order; an authorized customer may still not be allowed to choose a final price. An order CRUD save or status setter records a change but does not prove the transition was authorized. Use [authorization](authorization-and-isolation.md), [business logic/races](business-logic-and-races.md), and [webhooks](network-and-webhooks.md) for those specific edges.

## Counterevidence and validation

Seek server-derived totals, trusted gateway confirmation, amount/currency/order-reference matching, correct guest verification, explicit transition guards, idempotency records, and restricted refund authority. Check feature and gateway configuration: code for an inactive payment method may be unreachable. A strong claim needs the stated actor's control of a specific step and an observable economic, order, or fulfillment effect, not merely a surprising status value.

For an authorized local test, use sandbox payments or disposable orders. Compare own versus another order, expected versus altered amount/reference, valid versus duplicate or out-of-order callback, and record final order/payment/fulfillment state. Do not infer a financial loss without evidence of the actual downstream action; restore test state where possible.
