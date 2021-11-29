import React from "react";
import { Typography, Button, Card, CardActions, CardContent, CardMedia } from "@material-ui/core";

import useStyles from "./styles";

const CartItem = ({ item, uploadProductOnCart, onRemoveFromCart }) => {
  const classes = useStyles();
  return (
    <Card>
      <CardMedia image={item.image_url} alt={item.name} className={classes.media} />
      <CardContent className={classes.cardContent}>
        <Typography variant="h4">{item.name}</Typography>
        <Typography variant="h5">{item.total_product_price} €</Typography>
      </CardContent>
      <CardActions className={classes.CardActions}>
        <div className={classes.buttons}>
          <Button type="button" size="small" onClick={() => uploadProductOnCart(item.id_product, "sub", 1)}>
            -
          </Button>
          <Typography>{item.quantity}</Typography>
          <Button type="button" size="small" onClick={() => uploadProductOnCart(item.id_product, "add", 1)}>
            +
          </Button>
        </div>
        <Button variant="contained" type="button" color="secondary" onClick={() => onRemoveFromCart(item.id_product)}>
          Remove
        </Button>
      </CardActions>
    </Card>
  );
};

export default CartItem;
