--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: boats; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.boats (
    id integer NOT NULL,
    name text,
    type text,
    year integer,
    description text,
    key text
);


ALTER TABLE public.boats OWNER TO levantsi;

--
-- Name: boats_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.boats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boats_id_seq OWNER TO levantsi;

--
-- Name: boats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.boats_id_seq OWNED BY public.boats.id;


--
-- Name: owners; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.owners (
    id integer NOT NULL,
    user_id integer NOT NULL,
    boat_id integer NOT NULL,
    boat_admin boolean
);


ALTER TABLE public.owners OWNER TO levantsi;

--
-- Name: owners_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.owners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.owners_id_seq OWNER TO levantsi;

--
-- Name: owners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.owners_id_seq OWNED BY public.owners.id;


--
-- Name: pie; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.pie (
    name text,
    id numeric
);


ALTER TABLE public.pie OWNER TO levantsi;

--
-- Name: time_rates; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.time_rates (
    id integer NOT NULL,
    start_week integer,
    end_week integer,
    ratio numeric
);


ALTER TABLE public.time_rates OWNER TO levantsi;

--
-- Name: time_rates_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.time_rates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.time_rates_id_seq OWNER TO levantsi;

--
-- Name: time_rates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.time_rates_id_seq OWNED BY public.time_rates.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    created timestamp without time zone,
    usage integer,
    amount numeric,
    user_id integer,
    unit integer,
    started_date date NOT NULL,
    boat_id integer
);


ALTER TABLE public.transactions OWNER TO levantsi;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transactions_id_seq OWNER TO levantsi;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: units; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.units (
    id integer NOT NULL,
    type text
);


ALTER TABLE public.units OWNER TO levantsi;

--
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.units_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.units_id_seq OWNER TO levantsi;

--
-- Name: units_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.units_id_seq OWNED BY public.units.id;


--
-- Name: usage; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.usage (
    id integer NOT NULL,
    type text
);


ALTER TABLE public.usage OWNER TO levantsi;

--
-- Name: usage_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.usage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usage_id_seq OWNER TO levantsi;

--
-- Name: usage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.usage_id_seq OWNED BY public.usage.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text,
    password text,
    first_name text,
    last_name text,
    email text
);


ALTER TABLE public.users OWNER TO levantsi;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO levantsi;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: boats id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.boats ALTER COLUMN id SET DEFAULT nextval('public.boats_id_seq'::regclass);


--
-- Name: owners id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.owners ALTER COLUMN id SET DEFAULT nextval('public.owners_id_seq'::regclass);


--
-- Name: time_rates id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.time_rates ALTER COLUMN id SET DEFAULT nextval('public.time_rates_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: units id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.units ALTER COLUMN id SET DEFAULT nextval('public.units_id_seq'::regclass);


--
-- Name: usage id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.usage ALTER COLUMN id SET DEFAULT nextval('public.usage_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: boats; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.boats (id, name, type, year, description, key) FROM stdin;
1	Merenhuiske	H-vene	1975	Hassunhauska H	abc
2	La Mila	Targa 96	1982	Moottoripursi	xyz
5	Mama Cass	Omega 34	1981	Meidän	ac7e73
6	Mama Cass	Omega 34	1981	Meidän	e46aa9
7	Mama Cass	Omega 34	5	fds	82ac13
8	n	n	1981	fdsasd	d43703
9	Ilderim	8mR	1925	Hiäno!	8b55c2
10	Ilderim	8mR	1925	Hiäno!	4d43ad
11	Kuin Meri	Storbåt	1990	Vanhan oloinen	1234
12	HurenMeiske	puu	1901		eab47e
13	Nils	X-99	1999	Kisapaatti	bc9224
14	Nals	X-99	1991		123
63	a	a	1		e77d39
\.


--
-- Data for Name: owners; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.owners (id, user_id, boat_id, boat_admin) FROM stdin;
1	1	1	t
2	4	2	f
3	1	10	t
4	4	11	\N
5	4	12	\N
6	4	12	t
\.


--
-- Data for Name: pie; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.pie (name, id) FROM stdin;
paavo	1
paavo	1
\N	2
paavo	1
Pentti	2
paavo	1
paavo	1
pentti	1
\.


--
-- Data for Name: time_rates; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.time_rates (id, start_week, end_week, ratio) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.transactions (id, created, usage, amount, user_id, unit, started_date, boat_id) FROM stdin;
2	2021-09-02 22:41:01.41308	1	3	1	1	2021-08-31	1
3	2021-09-02 22:41:31.21726	2	3	1	1	2021-08-31	1
\.


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.units (id, type) FROM stdin;
1	tuntia
\.


--
-- Data for Name: usage; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.usage (id, type) FROM stdin;
1	sailing
2	working
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.users (id, username, password, first_name, last_name, email) FROM stdin;
1	bob	pbkdf2:sha256:260000$OdZExH0D2OcOPKem$e63ab8f22267db17de83aa18ee9e98b84f66edcde967448dbfbbc3e46421c6cf	Robert	Paulson	project.mayhem@paperstreet.com
4	muumipappa	pbkdf2:sha256:260000$tMVl873ZHmzmM62f$99d363d01f6a2829813e5c81345935b04c11116e925b32391bca9b041f19b7fd	Muumi	Pappa	moomindaddy69@yahoo.com
7	niilo	pbkdf2:sha256:260000$4xxT7q9jL98iJXyR$0e25e99c9cf9fced0e26b0e0b48a42c84c39779235ed08582a615bab67e45202	Niilo	Niilonen	nii@lo.fi
8	folkewest	pbkdf2:sha256:260000$EaGsKxJWOwuAOB6j$f46be7c12a263185130765339cac12c531bc6a51026c41dd0a4173625f2b3f90	Folke	West	folke@yle.fi
\.


--
-- Name: boats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.boats_id_seq', 64, true);


--
-- Name: owners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.owners_id_seq', 75, true);


--
-- Name: time_rates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.time_rates_id_seq', 1, false);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.transactions_id_seq', 3, true);


--
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.units_id_seq', 1, true);


--
-- Name: usage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.usage_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: boats boats_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_pkey PRIMARY KEY (id);


--
-- Name: boats key; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT key UNIQUE (key);


--
-- Name: owners owners_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT owners_pkey PRIMARY KEY (id);


--
-- Name: time_rates time_rates_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.time_rates
    ADD CONSTRAINT time_rates_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- Name: usage usage_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.usage
    ADD CONSTRAINT usage_pkey PRIMARY KEY (id);


--
-- Name: users username; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT username UNIQUE (username);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: owners fk_boat; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT fk_boat FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: transactions fk_boat; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT fk_boat FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: owners fk_user; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: transactions transactions_unit_fkey; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_unit_fkey FOREIGN KEY (unit) REFERENCES public.units(id);


--
-- Name: transactions transactions_usage_fkey; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_usage_fkey FOREIGN KEY (usage) REFERENCES public.usage(id);


--
-- Name: transactions transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

