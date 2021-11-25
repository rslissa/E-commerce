import React from "react";
import { Card, CardMedia, CardContent, CardActions, Typography, IconButton } from "@material-ui/core";
import { AddShoppingCart, CallMissedSharp } from "@material-ui/icons";
import useStyles from "./styles";

const Product = ({ product, onAddToCart }) => {
  const classes = useStyles();
  if (product.currency_code === "EUR") {
    product.currency_code = "€";
  }
  const handleAddToCart = () => onAddToCart(product.id_product, 1);
  return (
    <div>
      <Card className={classes.root}>
        <CardMedia className={classes.media} image={product.image_url} title={product.name} />
        <CardContent>
          <div className={classes.cardContent}>
            <Typography variant="h5" component="h2" gutterBottom>
              {product.name}
            </Typography>
            <Typography gutterBottom variant="h5" component="h2">
              {product.price} {product.currency_code}
            </Typography>
          </div>
          <Typography
            dangerouslySetInnerHTML={{ __html: product.description }}
            variant="body2"
            color="textSecondary"
            component="p"
          />
        </CardContent>
        <CardActions disableSpacing className={classes.cardActions}>
          <IconButton aria-label="Add to Cart" onClick={handleAddToCart}>
            <AddShoppingCart />
          </IconButton>
        </CardActions>
      </Card>
    </div>
  );
};

export default Product;
