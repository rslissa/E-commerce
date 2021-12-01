import React from "react";

import { Typography, Button, Divider } from "@material-ui/core";
import { Elements, CardElement, ElementsConsumer } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import Review from "./Review";

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLIC_KEY);

const PaymentForm = ({
  cart,
  cartProducts,
  checkoutToken,
  backStep,
  shippingData,
  onCaptureCheckout,
  nextStep,
  timeout,
}) => {
  const handleSubmit = async (event, elements, stripe) => {
    event.preventDefault();

    if (!stripe || !elements) return;

    const cardElement = elements.getElement(CardElement);
    const { error, paymentMethod } = await stripe.createPaymentMethod({ type: "card", card: cardElement });

    if (error) {
      console.log(error);
    } else {
      const orderData = {
        list_items: cartProducts,
        customer: { firstname: shippingData.firstName, lastname: shippingData.lastName, email: shippingData.email },
        shipping: {
          name: "Primary",
          street: shippingData.address1,
          town_city: shippingData.city,
          country_state: shippingData.shippingSubdivision,
          postal_zip_code: shippingData.postalCode,
          country: shippingData.shippingCountry,
        },
        payment: {
          gateway: "stripe",
          stripe: {
            payment_method_id: paymentMethod.id,
          },
        },
      };
      onCaptureCheckout(orderData);
      timeout();
      nextStep();
    }
  };

  return (
    <>
      <Review cart={cart} cartProducts={cartProducts} shippingData={shippingData} />
      <Divider />
      <Typography variant="h6" gutterBottom style={{ margin: "20px 0" }}>
        Payment method
      </Typography>
      <Elements stripe={stripePromise}>
        <ElementsConsumer>
          {({ elements, stripe }) => (
            <form onSubmit={(e) => handleSubmit(e, elements, stripe)}>
              <CardElement />
              <br /> <br />
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <Button variant="outlined" onClick={backStep}>
                  Back
                </Button>
                <Button type="submit" variant="contained" disabled={!stripe} color="primary">
                  Pay {cart.total_price} €
                </Button>
              </div>
            </form>
          )}
        </ElementsConsumer>
      </Elements>
    </>
  );
};

export default PaymentForm;
