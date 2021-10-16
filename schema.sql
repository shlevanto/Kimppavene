CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username text UNIQUE,
    password text,
    first_name text,
    last_name text,
    email text
);

CREATE TABLE boats (
    id SERIAL PRIMARY KEY,
    created timestamp without time zone,
    name text,
    type text,
    year integer,
    description text,
    key text UNIQUE
);

CREATE TABLE usage (
    id SERIAL PRIMARY KEY,
    usage_type text
);

CREATE TABLE cost_types (
    id SERIAL PRIMARY KEY,
    type text
);

CREATE TABLE income_types (
    id SERIAL PRIMARY KEY,
    type text
);

CREATE TABLE owners (
    id SERIAL PRIMARY KEY,
    user_id integer REFERENCES users(id),
    boat_id integer REFERENCES boats(id),
    boat_admin boolean,
    usage_right numeric,
    usage_hours numeric
);


CREATE TABLE time_rates (
    id SERIAL PRIMARY KEY,
    week numeric,
    ratio numeric,
    boat_id integer REFERENCES boats(id)
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    created timestamp without time zone,
    usage_id integer REFERENCES usage(id),
    amount numeric,
    user_id integer REFERENCES users(id),
    boat_id integer REFERENCES boats(id),
    unit integer,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    race boolean,
    description text,
    cost_type_id integer REFERENCES cost_types(id),
    income_type_id integer REFERENCES income_types(id)
);


CREATE VIEW report_base AS
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
    users.last_name,
    cost_types.type AS cost_type,
    income_types.type AS income_type
   FROM (((transactions t
     JOIN users ON ((t.user_id = users.id)))
     JOIN usage ON ((t.usage_id = usage.id)))
     JOIN boats ON ((t.boat_id = boats.id)))
     LEFT JOIN cost_types ON ((t.cost_type_id = cost_types.id))
     LEFT JOIN income_types ON ((t.income_type_id = income_types.id));

-- Initial values
INSERT INTO usage (usage_type) VALUES
  ('Käyttö'),
  ('Talkoo'),
  ('Kulu'),
  ('Tulo')
;

INSERT INTO cost_types (type) VALUES
  ('Huolto ja ylläpito'),
  ('Korjaukset'),
  ('Uushankinnat'),
  ('Laituripaikka ja telakointi'),
  ('Talkoot ja juhlat'),
  ('Kilpailu')
 ;

INSERT INTO income_types (type) VALUES
  ('Myyntitulo'),
  ('Vuokra'),
  ('Lahjoitus'),
  ('Ylimääräinen vastike')
;
