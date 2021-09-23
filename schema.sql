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
-- Name: cost_types; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.cost_types (
    id integer NOT NULL,
    type text
);


ALTER TABLE public.cost_types OWNER TO levantsi;

--
-- Name: cost_types_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.cost_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cost_types_id_seq OWNER TO levantsi;

--
-- Name: cost_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.cost_types_id_seq OWNED BY public.cost_types.id;


--
-- Name: income_types; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.income_types (
    id integer NOT NULL,
    type text
);


ALTER TABLE public.income_types OWNER TO levantsi;

--
-- Name: income_types_id_seq; Type: SEQUENCE; Schema: public; Owner: levantsi
--

CREATE SEQUENCE public.income_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.income_types_id_seq OWNER TO levantsi;

--
-- Name: income_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: levantsi
--

ALTER SEQUENCE public.income_types_id_seq OWNED BY public.income_types.id;


--
-- Name: owners; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.owners (
    id integer NOT NULL,
    user_id integer,
    boat_id integer,
    boat_admin boolean,
    usage_right numeric,
    usage_hours numeric
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
-- Name: transactions; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    created timestamp without time zone,
    usage_id integer,
    amount numeric,
    user_id integer,
    boat_id integer,
    unit integer,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    race boolean,
    description text,
    cost_type_id integer,
    income_type_id integer
);


ALTER TABLE public.transactions OWNER TO levantsi;

--
-- Name: usage; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.usage (
    id integer NOT NULL,
    usage_type text
);


ALTER TABLE public.usage OWNER TO levantsi;

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
-- Name: report_base; Type: VIEW; Schema: public; Owner: levantsi
--

CREATE VIEW public.report_base AS
 SELECT t.created,
    usage.usage_type,
    t.usage_id,
    t.amount,
    t.boat_id,
    t.start_date,
    t.end_date,
    t.race,
    t.description,
    t.cost_type_id,
    t.income_type_id,
    users.first_name,
    users.last_name
   FROM (((public.transactions t
     JOIN public.users ON ((t.user_id = users.id)))
     JOIN public.usage ON ((t.usage_id = usage.id)))
     JOIN public.boats ON ((t.boat_id = boats.id)));


ALTER TABLE public.report_base OWNER TO levantsi;

--
-- Name: time_rates; Type: TABLE; Schema: public; Owner: levantsi
--

CREATE TABLE public.time_rates (
    id integer NOT NULL,
    start_week numeric,
    end_week numeric,
    ratio numeric,
    boat_id integer
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
    unit text
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
-- Name: cost_types id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.cost_types ALTER COLUMN id SET DEFAULT nextval('public.cost_types_id_seq'::regclass);


--
-- Name: income_types id; Type: DEFAULT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.income_types ALTER COLUMN id SET DEFAULT nextval('public.income_types_id_seq'::regclass);


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
10	Mama Cass	Omega 34	1982	Hiäno!	2504ee
11	La Mila	Targa 96	1970	Myyty	f68718
12	Balboa	Rock 20	1979	Pieni mutta pippurinen	c28f2f
13	Newstart	Omega 34	1981	Lainassa	515917
14	a	aa	1980	aa	3863be
\.


--
-- Data for Name: cost_types; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.cost_types (id, type) FROM stdin;
1	Huolto ja ylläpito
2	Korjaukset
3	Uushankinnat
4	Laituripaikka ja telakointi
5	Talkoot ja juhlat
6	Kilpailu
\.


--
-- Data for Name: income_types; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.income_types (id, type) FROM stdin;
1	Myyntitulo
2	Vuokra
3	Lahjoitus
4	Ylimääräinen vastike
\.


--
-- Data for Name: owners; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.owners (id, user_id, boat_id, boat_admin, usage_right, usage_hours) FROM stdin;
32	2	\N	\N	\N	288
33	2	\N	\N	\N	288
34	2	13	t	\N	282.0
27	2	10	t	\N	288.0
30	11	10	\N	\N	287.0
28	2	11	t	\N	303
36	2	14	t	\N	288
37	14	10	\N	\N	288
31	2	12	t	\N	286.0
\.


--
-- Data for Name: time_rates; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.time_rates (id, start_week, end_week, ratio, boat_id) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.transactions (id, created, usage_id, amount, user_id, boat_id, unit, start_date, end_date, race, description, cost_type_id, income_type_id) FROM stdin;
2	2021-09-17 17:13:03.585125	1	2	2	13	\N	2021-09-17 17:10:00	2021-09-17 19:10:00	f	\N	\N	\N
3	2021-09-17 17:15:33.399699	1	2	2	13	\N	2021-09-17 17:10:00	2021-09-17 19:10:00	f	\N	\N	\N
4	2021-09-17 17:15:44.48842	1	2	2	13	\N	2021-09-17 17:10:00	2021-09-17 19:10:00	f	\N	\N	\N
5	2021-09-17 17:20:12.990234	1	2	2	10	\N	2021-09-17 17:19:00	2021-09-17 19:20:00	f	\N	\N	\N
6	2021-09-17 17:20:13.004451	1	2	11	10	\N	2021-09-17 17:19:00	2021-09-17 19:20:00	f	\N	\N	\N
7	2021-09-17 17:42:50.054823	2	0	2	11	\N	2021-09-17 17:42:00	2021-09-17 17:42:00	\N	\N	\N	\N
8	2021-09-17 17:56:41.812078	2	1	2	11	\N	2021-09-17 17:55:00	2021-09-17 18:55:00	\N	foi	\N	\N
9	2021-09-17 17:57:38.963658	2	1	2	11	\N	2021-09-17 17:57:00	2021-09-17 18:57:00	\N	foi	\N	\N
10	2021-09-17 17:58:41.173897	2	1	2	11	\N	2021-09-17 17:58:00	2021-09-17 18:58:00	\N	foi	\N	\N
11	2021-09-17 17:59:36.891062	2	1	2	11	\N	2021-09-24 17:59:00	2021-09-24 18:59:00	\N	foi	\N	\N
12	2021-09-17 18:01:43.454921	2	1	2	11	\N	2021-09-17 18:00:00	2021-09-17 19:00:00	\N	joi	\N	\N
14	2021-09-17 18:49:25.300989	3	133.33	2	11	\N	2021-09-17 18:46:00	2021-09-17 18:46:00	\N	heijaa	1	\N
15	2021-09-18 12:02:52.253902	4	100	2	14	\N	2021-09-18 12:02:00	2021-09-18 12:02:00	\N	faaalaa	\N	1
16	2021-09-20 21:44:14.061025	1	2	2	12	\N	2021-09-20 21:44:00	2021-09-20 23:44:00	f	\N	\N	\N
17	2021-09-20 22:03:55.12284	3	200	2	12	\N	2021-09-20 22:03:00	2021-09-20 22:03:00	\N	jotain	1	\N
18	2021-09-20 22:04:14.504066	3	500	2	12	\N	2021-09-20 22:04:00	2021-09-20 22:04:00	\N	bileet	5	\N
\.


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.units (id, unit) FROM stdin;
\.


--
-- Data for Name: usage; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.usage (id, usage_type) FROM stdin;
1	sailing
2	maintenance
4	income
3	cost
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: levantsi
--

COPY public.users (id, username, password, first_name, last_name, email) FROM stdin;
2	bob	pbkdf2:sha256:260000$XpLaRKoZiu2m9Cmf$eedc7f133104440629d6f1deaea2ae84de3fffc57c3702f0463a3d81f3ba8ac4	Robert	Paulson	bigbob@paperstreet.co
11	muumipappa	pbkdf2:sha256:260000$ZWihMDTxeEo284ke$78dee4912c63237bf1cfa84d1e8e95b8a405a5ce226a3e57304f47790a17f5ba	Muumi	Pappa	muumi@huumi.fi
13	bib	pbkdf2:sha256:260000$EHrSa7dLdxLbJCpV$b1468d47e44f2b74987126c9867dafd7247460227b521bbc5a145b150ab60181	Bill	Bibbit	bi@bi.bi
14	Paavo	pbkdf2:sha256:260000$2XFRPgTJtP4qBOyO$b8402feee8cd238924096f1cbe2e859b93242c407c261a2c09d35c127b7f41f1	Paavo	Pesusieni	a@s.d
\.


--
-- Name: boats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.boats_id_seq', 14, true);


--
-- Name: cost_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.cost_types_id_seq', 7, true);


--
-- Name: income_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.income_types_id_seq', 4, true);


--
-- Name: owners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.owners_id_seq', 69, true);


--
-- Name: time_rates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.time_rates_id_seq', 1, false);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.transactions_id_seq', 18, true);


--
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.units_id_seq', 1, false);


--
-- Name: usage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.usage_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: levantsi
--

SELECT pg_catalog.setval('public.users_id_seq', 14, true);


--
-- Name: boats boats_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.boats
    ADD CONSTRAINT boats_pkey PRIMARY KEY (id);


--
-- Name: cost_types cost_types_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.cost_types
    ADD CONSTRAINT cost_types_pkey PRIMARY KEY (id);


--
-- Name: income_types income_types_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.income_types
    ADD CONSTRAINT income_types_pkey PRIMARY KEY (id);


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
-- Name: users username_unique; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT username_unique UNIQUE (username);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: owners boat_fk; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT boat_fk FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: transactions boat_id; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT boat_id FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: time_rates boat_id; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.time_rates
    ADD CONSTRAINT boat_id FOREIGN KEY (boat_id) REFERENCES public.boats(id);


--
-- Name: transactions cost_type; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT cost_type FOREIGN KEY (cost_type_id) REFERENCES public.cost_types(id);


--
-- Name: transactions income_type; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT income_type FOREIGN KEY (income_type_id) REFERENCES public.income_types(id);


--
-- Name: transactions unit_id; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT unit_id FOREIGN KEY (unit) REFERENCES public.units(id);


--
-- Name: transactions usage_id; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT usage_id FOREIGN KEY (usage_id) REFERENCES public.usage(id);


--
-- Name: owners user_fk; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: transactions user_id; Type: FK CONSTRAINT; Schema: public; Owner: levantsi
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

