import React, { useState, useEffect } from "react";
import { commerce, Commerce } from "./lib/Commerce";
import { Products, Navbar, Cart, Checkout } from "./components";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryCache, QueryClientProvider, useQuery } from "react-query";
import axios from "axios";

const queryClient = new QueryClient();

const fetchProducts = async () => {
  const res = await axios.get("http://localhost:5000/api/v1/list-products");
  return res.data;
};

const fetchCart = async (id_cart) => {
  if (id_cart === 0) {
    const res = await axios.get(`http://localhost:5000/api/v1/cart`);
    return res.data;
  } else {
    const res = await axios.get(`http://localhost:5000/api/v1/cart/${id_cart}`);
    return res.data;
  }
};

const App = () => {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState({});
  const [order, setOrder] = useState({});
  const [errorMessage, setErrorMessage] = useState("");

  const handleAddToCart = async (productId, quantity) => {
    const item = await commerce.cart.add(productId, quantity);
    setCart(item.cart);
  };

  const handleUpdateCartQty = async (lineItemId, quantity) => {
    const response = await commerce.cart.update(lineItemId, { quantity });
    setCart(response.cart);
  };

  const handleRemoveFromCart = async (lineItemId) => {
    const response = await commerce.cart.remove(lineItemId);
    setCart(response.cart);
  };

  const handleEmptyCart = async () => {
    const response = await commerce.cart.empty();

    setCart(response.cart);
  };

  const refreshCart = async () => {
    const newCart = await commerce.cart.refresh();

    setCart(newCart);
  };

  const handleCaptureCheckout = async (checkoutTokenId, newOrder) => {
    try {
      const incomingOrder = await commerce.checkout.capture(checkoutTokenId, newOrder);
      setOrder(incomingOrder);
      refreshCart();
    } catch (error) {
      setErrorMessage(error.data.error.message);
    }
  };

  const fillProducts = (value) => {
    setProducts(value);
  };

  const fillcart = (value) => {
    setCart(value);
  };

  useEffect(() => {
    fetchProducts()
      .then(function (result) {
        console.log(Object.values(result));
        fillProducts(Object.values(result));
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });

    const id_cart = 0;
    if (Object.keys(cart).length !== 0) {
      id_cart = cart.id_cart;
      console.log("the cart is not empty");
    } else {
      console.log("the cart is empty");
    }

    fetchCart(id_cart)
      .then(function (result) {
        console.log(Object.values(result));
        fillcart(Object.values(result));
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
    //fetchProducts();
    // fetchCart();
  }, []);

  return (
    <>
      <Router>
        <div>
          <Navbar totalItems={cart.total_items} />
          <Routes>
            <Route exact path="/" element={<Products products={products} onAddToCart={handleAddToCart} />} />
            <Route
              exact
              path="/cart"
              element={
                <Cart
                  cart={cart}
                  handleUpdateCartQty={handleUpdateCartQty}
                  handleRemoveFromCart={handleRemoveFromCart}
                  handleEmptyCart={handleEmptyCart}
                />
              }
            />
            <Route
              exact
              path="/checkout"
              element={
                <Checkout cart={cart} order={order} onCaptureCheckout={handleCaptureCheckout} error={errorMessage} />
              }
            />
          </Routes>
        </div>
      </Router>
    </>
  );
};

export default function Wraped() {
  return (
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );
}
