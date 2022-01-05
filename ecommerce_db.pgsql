--
-- PostgreSQL database dump
--

-- Dumped from database version 10.14
-- Dumped by pg_dump version 10.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address (
    id_address integer NOT NULL,
    city character varying NOT NULL,
    address character varying NOT NULL,
    postal_code character varying NOT NULL,
    country character varying NOT NULL,
    region character varying NOT NULL,
    id_user bigint NOT NULL
);


ALTER TABLE public.address OWNER TO postgres;

--
-- Name: address_id_address_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.address_id_address_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.address_id_address_seq OWNER TO postgres;

--
-- Name: address_id_address_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.address_id_address_seq OWNED BY public.address.id_address;


--
-- Name: cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart (
    id_cart integer NOT NULL,
    creation timestamp without time zone NOT NULL,
    last_update timestamp without time zone NOT NULL,
    buyed boolean NOT NULL,
    id_user bigint,
    expiring_date timestamp without time zone NOT NULL,
    total_items bigint,
    total_unique_items bigint,
    total_price bigint
);


ALTER TABLE public.cart OWNER TO postgres;

--
-- Name: cart_id_cart_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_id_cart_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cart_id_cart_seq OWNER TO postgres;

--
-- Name: cart_id_cart_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_id_cart_seq OWNED BY public.cart.id_cart;


--
-- Name: cart_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_product (
    id_cart bigint NOT NULL,
    id_product bigint NOT NULL,
    quantity bigint NOT NULL,
    last_update timestamp without time zone
);


ALTER TABLE public.cart_product OWNER TO postgres;

--
-- Name: countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.countries (
    country_code character varying NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.countries OWNER TO postgres;

--
-- Name: countries_subdivisions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.countries_subdivisions (
    id_subdivision bigint NOT NULL,
    code character varying NOT NULL,
    name character varying NOT NULL,
    country_code character varying NOT NULL
);


ALTER TABLE public.countries_subdivisions OWNER TO postgres;

--
-- Name: countries_subdivisons_id_subdivision_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.countries_subdivisons_id_subdivision_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.countries_subdivisons_id_subdivision_seq OWNER TO postgres;

--
-- Name: countries_subdivisons_id_subdivision_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.countries_subdivisons_id_subdivision_seq OWNED BY public.countries_subdivisions.id_subdivision;


--
-- Name: order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order" (
    id_shipping bigint NOT NULL,
    id_user bigint NOT NULL,
    id_address bigint NOT NULL,
    id_cart bigint NOT NULL
);


ALTER TABLE public."order" OWNER TO postgres;

--
-- Name: product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product (
    id_product integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    price real NOT NULL,
    currency_code character varying(3) NOT NULL,
    image_url character varying NOT NULL,
    status boolean NOT NULL,
    stock bigint NOT NULL,
    last_update timestamp without time zone NOT NULL
);


ALTER TABLE public.product OWNER TO postgres;

--
-- Name: product_id_product_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_id_product_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_id_product_seq OWNER TO postgres;

--
-- Name: product_id_product_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_id_product_seq OWNED BY public.product.id_product;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id_user integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_user_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_user_seq OWNER TO postgres;

--
-- Name: user_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_user_seq OWNED BY public."user".id_user;


--
-- Name: address id_address; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address ALTER COLUMN id_address SET DEFAULT nextval('public.address_id_address_seq'::regclass);


--
-- Name: cart id_cart; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart ALTER COLUMN id_cart SET DEFAULT nextval('public.cart_id_cart_seq'::regclass);


--
-- Name: countries_subdivisions id_subdivision; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries_subdivisions ALTER COLUMN id_subdivision SET DEFAULT nextval('public.countries_subdivisons_id_subdivision_seq'::regclass);


--
-- Name: product id_product; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product ALTER COLUMN id_product SET DEFAULT nextval('public.product_id_product_seq'::regclass);


--
-- Name: user id_user; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id_user SET DEFAULT nextval('public.user_id_user_seq'::regclass);


--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.address (id_address, city, address, postal_code, country, region, id_user) FROM stdin;
\.


--
-- Data for Name: cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart (id_cart, creation, last_update, buyed, id_user, expiring_date, total_items, total_unique_items, total_price) FROM stdin;
1	2021-11-26 18:31:06.428957	2021-11-08 18:47:59.422	f	\N	2021-12-07 16:31:06.428957	0	0	0
\.


--
-- Data for Name: cart_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_product (id_cart, id_product, quantity, last_update) FROM stdin;
1	4	1	2021-11-08 18:47:36.193
\.


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countries (country_code, name) FROM stdin;
IT	Italy
\.


--
-- Data for Name: countries_subdivisions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countries_subdivisions (id_subdivision, code, name, country_code) FROM stdin;
2	AG	Agrigento	IT
3	AL	Alessandria	IT
4	AN	Ancona	IT
5	AR	Arezzo	IT
6	AP	Ascoli Piceno	IT
7	AT	Asti	IT
8	AV	Avellino	IT
9	BA	Bari	IT
10	BT	Barletta-Andria-Trani	IT
11	BL	Belluno	IT
12	BN	Benevento	IT
13	BG	Bergamo	IT
14	BI	Biella	IT
15	BO	Bologna	IT
16	BZ	Bolzano	IT
17	BS	Brescia	IT
18	BR	Brindisi	IT
19	CA	Cagliari	IT
20	CL	Caltanissetta	IT
21	CB	Campobasso	IT
22	CE	Caserta	IT
23	CT	Catania	IT
24	CZ	Catanzaro	IT
25	CH	Chieti	IT
26	CO	Como	IT
27	CS	Cosenza	IT
28	CR	Cremona	IT
29	KR	Crotone	IT
30	CN	Cuneo	IT
31	FM	Fermo	IT
32	FE	Ferrara	IT
33	FI	Firenze	IT
34	FG	Foggia	IT
35	FC	Forli-Cesena	IT
36	FR	Frosinone	IT
37	GE	Genova	IT
38	GO	Gorizia	IT
39	GR	Grosseto	IT
40	IM	Imperia	IT
41	IS	Isernia	IT
42	LT	Latina	IT
43	LE	Lecce	IT
44	LC	Lecco	IT
45	LI	Livorno	IT
46	LO	Lodi	IT
47	LU	Lucca	IT
48	MC	Macerata	IT
49	MN	Mantova	IT
50	MS	Massa-Carrara	IT
51	MT	Matera	IT
52	ME	Messina	IT
53	MI	Milano	IT
54	MO	Modena	IT
55	MB	Monza e Brianza	IT
56	NA	Napoli	IT
57	NO	Novara	IT
58	NU	Nuoro	IT
59	PD	Padova	IT
60	PA	Palermo	IT
61	PR	Parma	IT
62	PV	Pavia	IT
63	PU	Pesaro e Urbino	IT
64	PE	Pescara	IT
65	PC	Piacenza	IT
66	PI	Pisa	IT
67	PT	Pistoia	IT
68	PN	Pordenone	IT
69	PZ	Potenza	IT
70	PO	Prato	IT
71	RG	Ragusa	IT
72	RA	Ravenna	IT
73	RM	Roma	IT
74	RO	Rovigo	IT
75	SA	Salerno	IT
76	SS	Sassari	IT
77	SV	Savona	IT
78	SI	Siena	IT
79	SR	Siracusa	IT
80	SO	Sondrio	IT
81	SU	Sud Sardegna	IT
82	TA	Taranto	IT
83	TE	Teramo	IT
84	TR	Terni	IT
85	TO	Torino	IT
86	TP	Trapani	IT
87	TV	Treviso	IT
88	TS	Trieste	IT
89	UD	Udine	IT
90	VA	Varese	IT
91	VE	Venezia	IT
92	VB	Verbano-Cusio-Ossola	IT
93	VC	Vercelli	IT
94	VR	Verona	IT
95	VV	Vibo Valentia	IT
96	VI	Vicenza	IT
\.


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."order" (id_shipping, id_user, id_address, id_cart) FROM stdin;
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product (id_product, name, description, price, currency_code, image_url, status, stock, last_update) FROM stdin;
2	Prosecco	Prodotto in Veneto, dal gusto dolce	20	EUR	https://i.ibb.co/kSZtDQJ/vino-bianco.jpg	t	30	2021-12-06 11:15:28.968609
4	Nero dAvola	Rosso dal gusto deciso, siciliano DOC	15	EUR	https://i.ibb.co/L9p2D14/vino-rosso.jpg	t	60	2021-12-06 11:15:28.968609
10	Grillo	Bianco, ottimo con cibi a base di pesce	13	EUR	https://i.ibb.co/St8ZK3B/vino-bianco-2.jpg	t	40	2021-12-06 11:15:28.968609
11	Moscato	vino liquoroso, ottimo da accompagnare con i dolci	20	EUR	https://i.ibb.co/L9p2D14/vino-rosso.jpg	t	30	2021-12-06 11:15:28.968609
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id_user, first_name, last_name, email) FROM stdin;
1	Mario	Rossi	mario.rossi@gmail.com
\.


--
-- Name: address_id_address_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.address_id_address_seq', 1, false);


--
-- Name: cart_id_cart_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_id_cart_seq', 14, true);


--
-- Name: countries_subdivisons_id_subdivision_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.countries_subdivisons_id_subdivision_seq', 96, true);


--
-- Name: product_id_product_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_id_product_seq', 35, true);


--
-- Name: user_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_user_seq', 1, true);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id_address);


--
-- Name: cart cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_pkey PRIMARY KEY (id_cart);


--
-- Name: cart_product cart_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_product
    ADD CONSTRAINT cart_product_pkey PRIMARY KEY (id_cart, id_product);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (country_code);


--
-- Name: countries_subdivisions countries_subdivisons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries_subdivisions
    ADD CONSTRAINT countries_subdivisons_pkey PRIMARY KEY (id_subdivision);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id_product);


--
-- Name: order shipping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT shipping_pkey PRIMARY KEY (id_shipping);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id_user);


--
-- Name: address address_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_id_user_fkey FOREIGN KEY (id_user) REFERENCES public."user"(id_user) NOT VALID;


--
-- Name: cart cart_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_id_user_fkey FOREIGN KEY (id_user) REFERENCES public."user"(id_user) NOT VALID;


--
-- Name: cart_product cart_product_id_cart_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_product
    ADD CONSTRAINT cart_product_id_cart_fkey FOREIGN KEY (id_cart) REFERENCES public.cart(id_cart);


--
-- Name: cart_product cart_product_id_product_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_product
    ADD CONSTRAINT cart_product_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.product(id_product);


--
-- Name: countries_subdivisions countries_subdivisons_country_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries_subdivisions
    ADD CONSTRAINT countries_subdivisons_country_code_fkey FOREIGN KEY (country_code) REFERENCES public.countries(country_code);


--
-- Name: order shipping_id_address_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT shipping_id_address_fkey FOREIGN KEY (id_address) REFERENCES public.address(id_address);


--
-- Name: order shipping_id_cart_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT shipping_id_cart_fkey FOREIGN KEY (id_cart) REFERENCES public.cart(id_cart);


--
-- Name: order shipping_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT shipping_id_user_fkey FOREIGN KEY (id_user) REFERENCES public."user"(id_user);


--
-- PostgreSQL database dump complete
--

