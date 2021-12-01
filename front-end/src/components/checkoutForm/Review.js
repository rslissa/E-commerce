import React from "react";
import { Typography, List, ListItem, ListItemText } from "@material-ui/core";

const Review = ({ cart, cartProducts, shippingData }) => {
  return (
    <>
      <Typography variant="h6" gutterBottom>
        Order Summary
      </Typography>
      <List disablePadding>
        {cartProducts.map((product) => (
          <ListItem style={{ padding: "10px 0" }} key={product.name}>
            <ListItemText primary={product.name} secondary={`Quantity: ${product.quantity}`} />
            <Typography variant="body2">{product.total_product_price} €</Typography>
          </ListItem>
        ))}
        <ListItem style={{ padding: "10px 0" }}>
          <ListItemText primary="Total" />
          <Typography variant="subtitle1" style={{ fontWight: 700 }}>
            {cart.total_price} €
          </Typography>
        </ListItem>
      </List>
    </>
  );
};

export default Review;
