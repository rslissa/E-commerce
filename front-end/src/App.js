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
  const [cartProducts, setCartProducts] = useState([]);
  const [order, setOrder] = useState({});
  const [errorMessage, setErrorMessage] = useState("");

  const cartId = 1;

  const listProducts = async () => {
    const res = await axios.get("http://localhost:5000/api/v1/list-products");
    return res.data;
  };

  const listProductsByCart = async (id_cart) => {
    const res = await axios.get(`http://127.0.0.1:5000/api/v1/list-products-by-cart/${id_cart}`);
    return res.data;
  };

  const createCart = async () => {
    const res = await axios.get(`http://localhost:5000/api/v1/cart`);
    return res.data;
  };

  const removeProductOnCart = async (id_product) => {
    const res = await axios.delete(`http://localhost:5000/api/v1/cart/${cart["id_cart"]}/product/${id_product}`);
    refreshCart(cart["id_cart"]);
  };

  const getCartById = async (id_cart) => {
    const res = await axios.get(`http://localhost:5000/api/v1/cart/${id_cart}`);
    return res.data;
  };

  const uploadProductOnCart = async (id_product, operation, quantity) => {
    const payload = `{"operation": "${operation}","quantity": ${quantity}}`;
    const data = JSON.parse(payload);
    const { data: response } = await axios.post(
      `http://localhost:5000/api/v1/cart/${cart["id_cart"]}/product/${id_product}`,
      data
    );
    refreshCart(cart["id_cart"]);
  };

  const handleRemoveFromCart = async (lineItemId) => {
    const response = await commerce.cart.remove(lineItemId);
    setCart(response.cart);
  };

  const handleEmptyCart = async () => {
    const response = await commerce.cart.empty();
    setCart(response.cart);
  };

  // const refreshCart = async () => {
  //   const newCart = await commerce.cart.refresh();

  //   setCart(newCart);
  // };

  const handleCaptureCheckout = async (checkoutTokenId, newOrder) => {
    try {
      const incomingOrder = await commerce.checkout.capture(checkoutTokenId, newOrder);
      setOrder(incomingOrder);
      refreshCart();
    } catch (error) {
      setErrorMessage(error.data.error.message);
    }
  };

  const fetchProducts = () => {
    listProducts()
      .then(function (result) {
        setProducts(result);
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
  };

  const refreshCart = (cartId) => {
    getCartById(cartId)
      .then(function (result) {
        setCart(result);
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
    listProductsByCart(cartId)
      .then(function (result) {
        setCartProducts(result);
      })
      .catch(function (error) {
        console.log("Failed!", error);
      });
  };

  useEffect(() => {
    fetchProducts();
    // addProductOnCart(result["id_cart"], 11, 5);
    //TODO creare un nuovo carrello e non utilizzare sempre lo stesso
    refreshCart(cartId);
  }, []);

  return (
    <>
      <Router>
        <div>
          <Navbar totalItems={cart["total_items"]} />
          <Routes>
            <Route exact path="/" element={<Products products={products} onAddToCart={uploadProductOnCart} />} />
            <Route
              exact
              path="/cart"
              element={
                <Cart
                  cart={cart}
                  cartProducts={cartProducts}
                  uploadProductOnCart={uploadProductOnCart}
                  removeProductOnCart={removeProductOnCart}
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
