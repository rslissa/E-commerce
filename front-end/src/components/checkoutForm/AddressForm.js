import React, { useState, useEffect } from "react";
import { InputLabel, Select, MenuItem, Button, Grid, Typography } from "@material-ui/core";
import { useForm, FormProvider } from "react-hook-form";
import { Link } from "react-router-dom";
import { QueryClient, QueryCache, QueryClientProvider, useQuery } from "react-query";
import axios from "axios";
import FormInput from "./FormInput";

const AddressForm = ({ next }) => {
  const [shippingCountries, setShippingCountries] = useState([]);
  const [shippingCountry, setShippingCountry] = useState("");
  const [shippingSubdivisions, setShippingSubdivisions] = useState([]);
  const [shippingSubdivision, setShippingSubdivision] = useState("");
  const methods = useForm();

  const fetchCountries = async () => {
    const res = await axios.get(`http://127.0.0.1:5000/api/v1/list-countries`);
    setShippingCountries(res.data);
    setShippingCountry(res.data[0]);
    return res.data;
  };

  const fetchSubdivisions = async (country_code) => {
    const res = await axios.get(`http://127.0.0.1:5000/api/v1/list-subcountries/${country_code}`);
    setShippingSubdivisions(res.data);
    setShippingSubdivision(res.data[0]);
    return res.data;
  };

  useEffect(() => {
    fetchCountries();
  }, []);

  useEffect(() => {
    if (shippingCountry) fetchSubdivisions(shippingCountry["country_code"]);
  }, [shippingCountry]);

  return (
    <>
      <Typography variant="h6" gutterBottom>
        Shipping Address
      </Typography>
      <FormProvider {...methods}>
        <form
          onSubmit={methods.handleSubmit((data) => {
            next({ ...data, shippingCountry, shippingSubdivision });
          })}
        >
          <Grid container spacing={3}>
            <FormInput required name="firstName" label="First name" />
            <FormInput required name="lastName" label="Last name" />
            <FormInput required name="address1" label="Address" />
            <FormInput required name="email" label="Email" />
            <FormInput required name="city" label="City" />
            <FormInput required name="postalCode" label="Postal code" />
            <Grid item xs={12} sm={6}>
              <InputLabel>Shipping Country</InputLabel>
              <Select value={shippingCountry["name"] || ""} required fullWidth>
                {shippingCountries.map((country) => (
                  <MenuItem key={country.country_code} value={country.name}>
                    {country.name}
                  </MenuItem>
                ))}
              </Select>
            </Grid>
            <Grid item xs={12} sm={6}>
              <InputLabel>Shipping Subdivision</InputLabel>
              <Select
                value={shippingSubdivision || ""}
                required
                fullWidth
                onChange={(e) => setShippingSubdivision(e.target.value)}
              >
                {shippingSubdivisions.map((subdivision) => (
                  <MenuItem key={subdivision.id_subdivision} value={subdivision.name}>
                    {subdivision.name}
                  </MenuItem>
                ))}
              </Select>
            </Grid>
          </Grid>
          <br />
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <Button component={Link} to="/cart" variant="outlined">
              Back to Cart
            </Button>
            <Button type="submit" variant="contained" color="primary">
              Next
            </Button>
          </div>
        </form>
      </FormProvider>
    </>
  );
};

export default AddressForm;
