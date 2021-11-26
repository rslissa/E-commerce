import React, { useState, useEffect } from "react";
import { commerce, Commerce } from "./lib/Commerce";
import { Products, Navbar, Cart, Checkout } from "./components";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryCache, QueryClientProvider, useQuery } from "react-query";
import axios from "axios";
import { ReactQueryDevtools } from "react-query/devtools";

const queryClient = new QueryClient();

const App = () => {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState({});
  const [order, setOrder] = useState({});
  const [errorMessage, setErrorMessage] = useState("");

  const fetchProducts = async () => {
    const res = await axios.get("http://localhost:5000/api/v1/list-products");
    return res.data;
  };

  const fetchCart = async (id_cart) => {
    //if the ID is 0 create a new cart, else refresh the cart
    if (id_cart === 0) {
      const res = await axios.get(`http://localhost:5000/api/v1/cart`);
      return res.data;
    } else {
      const res = await axios.get(`http://localhost:5000/api/v1/cart/${id_cart}`);
      return res.data;
    }
  };

  const addProductOnCart = async (id_cart, id_product, quantity) => {
    const payload = `{
              "quantity": ${quantity}
            }`;
    const data = JSON.parse(payload);
    const { data: response } = await axios.post(
      `http://localhost:5000/api/v1/cart/${id_cart}/product/${id_product}`,
      data
    );
    return response.data;
  };

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

  const fillProducts = () => {
    fetchProducts()
      .then(function (result) {
        setProducts(result);
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
  };

  const fillcart = async () => {
    let id_cart = 0;
    if (Object.keys(cart).length !== 0) {
      id_cart = cart["id_cart"];
    }

    fetchCart(id_cart)
      .then(function (result) {
        setCart(result);
        console.log("100 result: ", result);
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
  };

  useEffect(() => {
    fillProducts();
    fillcart();

    addProductOnCart(cart["id_cart"], 11, 5)
      .then(function (result) {
        setCart(result);
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
    console.log("110 cart: ", cart);
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
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
