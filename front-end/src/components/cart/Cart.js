import React from "react";
import { Container, Typography, Button, Grid } from "@material-ui/core";
import CartItem from "./cartItem/CartItem";
import useStyles from "./styles";
import { Link } from "react-router-dom";
const Cart = ({ cart, cartProducts, uploadProductOnCart, removeProductOnCart }) => {
  const classes = useStyles();
  const EmptyCart = () => (
    <Typography variant="subtitle1">
      You have no items in your shopping cart,
      <Link to="/" className={classes.link}>
        Start adding some!
      </Link>
    </Typography>
  );

  const FilledCart = () => (
    <>
      <Grid container spacing={3}>
        {cartProducts.map((item) => (
          <Grid item xs={12} sm={4} key={item.id}>
            <CartItem item={item} uploadProductOnCart={uploadProductOnCart} onRemoveFromCart={removeProductOnCart} />
          </Grid>
        ))}
      </Grid>
      <div className={classes.cardDetails}>
        <Typography variant="h4">Subtotal: {cart.total_price} €</Typography>
        <div>
          <Button
            className={classes.emptyButton}
            size="large"
            type="button"
            variant="contained"
            color="secondary"
            onClick={removeProductOnCart}
          >
            Empty Cart
          </Button>
          <Button
            component={Link}
            to="/checkout"
            className={classes.checkoutButton}
            size="large"
            type="button"
            variant="contained"
            color="primary"
          >
            CheckOut
          </Button>
        </div>
      </div>
    </>
  );

  if (!cartProducts) return "Loading";

  return (
    <Container>
      <div className={classes.toolbar} />
      <Typography className={classes.title} variant="h3" gutterBottom>
        Your Shopping Cart
      </Typography>

      {!cartProducts.length ? <EmptyCart /> : <FilledCart />}
    </Container>
  );
};

export default Cart;
