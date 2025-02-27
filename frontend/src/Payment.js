import React from "react";
import { useLocation } from "react-router-dom";
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import CheckoutForm from "./CheckoutForm";
import "./Payment.css";

const stripePromise = loadStripe(
  "pk_test_51Q6cczEHbFed1fqcKTZucQQcQjIOxsgQ8NTU7n9yUeSz1yPgZ0KnYeZU3ZpbKpYTnw5obIN0NrMOMu9a9QmvVwZy00noEzpOyk" // pragma: allowlist secret
);

function Payment() {
  const location = useLocation();
  const { nip, deliveryOption, deliveryDetails } = location.state || {};

  const options = {
    mode: "payment",
    amount: 1099,
    currency: "pln",
    locale: "pl",
  };

  return (
    <div className="payment-page">
      <h1>Płatność</h1>
      <div className="payment-form">
        <Elements stripe={stripePromise} options={options}>
          <CheckoutForm
            nip={nip}
            deliveryOption={deliveryOption}
            deliveryDetails={deliveryDetails}
          />
        </Elements>
      </div>
    </div>
  );
}

export default Payment;
