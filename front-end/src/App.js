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

  const currentDate = () => {
    var today = new Date();
    var date = today.getFullYear() + "-" + today.getMonth() + "-" + today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds() + "." + today.getMilliseconds();
    const dateTime = date + "T" + time;
    return dateTime;
  };

  const listProducts = async () => {
    const res = await axios.get("http://localhost:5000/bridge/v1/list-products");
    return res.data;
  };

  const listProductsByCart = async (id_cart) => {
    const res = await axios.get(`http://127.0.0.1:5000/bridge/v1/list-products-by-cart/${id_cart}`);
    return res.data;
  };

  const createCart = async () => {
    const res = await axios.get(`http://localhost:5000/bridge/v1/cart`);
    return res.data;
  };

  const removeProductOnCart = async (id_product) => {
    const res = await axios.delete(`http://localhost:5000/bridge/v1/cart/${cart["id_cart"]}/product/${id_product}`);
    refreshCart(cart["id_cart"]);
  };

  const removeProductsOnCart = async (id_product) => {
    const res = await axios.delete(`http://localhost:5000/bridge/v1/cart/${cart["id_cart"]}`);
    refreshCart(cart["id_cart"]);
  };

  const getCartById = async (id_cart) => {
    const res = await axios.get(`http://localhost:5000/bridge/v1/cart/${id_cart}`);
    return res.data;
  };

  const uploadProductOnCart = async (id_product, operation, quantity) => {
    const dateTime = currentDate();
    const payload = `{"operation": "${operation}","quantity": ${quantity},"last_update":"${dateTime}"}`;
    const data = JSON.parse(payload);
    const { data: response } = await axios.post(
      `http://localhost:5000/bridge/v1/cart/${cart["id_cart"]}/product/${id_product}`,
      data
    );
    refreshCart(cart["id_cart"]);
  };

  const handleCaptureCheckout = async (incomingOrder) => {
    setOrder(incomingOrder);
    removeProductsOnCart(cartId);
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
                  removeProductsOnCart={removeProductsOnCart}
                />
              }
            />
            <Route
              exact
              path="/checkout"
              element={
                <Checkout
                  cart={cart}
                  cartProducts={cartProducts}
                  order={order}
                  onCaptureCheckout={handleCaptureCheckout}
                  error={errorMessage}
                />
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
