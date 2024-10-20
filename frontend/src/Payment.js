import React from "react";
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import CheckoutForm from "./CheckoutForm";
import "./Payment.css";

const stripePromise = loadStripe(
  "pk_test_51Q6cczEHbFed1fqcKTZucQQcQjIOxsgQ8NTU7n9yUeSz1yPgZ0KnYeZU3ZpbKpYTnw5obIN0NrMOMu9a9QmvVwZy00noEzpOyk" // pragma: allowlist secret
);

function Payment() {
  const options = {
    mode: "payment",
    amount: 1099,
    currency: "pln",
    appearance: {
      theme: "flat",
      labels: "floating",
    },
  };

  return (
    <div className="payment-page">
      <h1>Complete your Payment</h1>
      <div className="payment-form">
        <Elements stripe={stripePromise} options={options}>
          <CheckoutForm />
        </Elements>
      </div>
    </div>
  );
}

export default Payment;
