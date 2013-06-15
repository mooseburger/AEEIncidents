-- Database: hack

-- DROP DATABASE hack;

CREATE DATABASE hack
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;


-- Table: events


CREATE TABLE events
(
  id character varying(256) NOT NULL,
  created_at timestamp with time zone,
  updated_at timestamp with time zone,
  town character varying(100),
  area character varying(100),
  status character varying(100),
  last_update timestamp without time zone,
  posted boolean,
  CONSTRAINT events_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE events
  OWNER TO postgres;
  
-- Table: messages

CREATE TABLE messages
(
  id character varying(256) NOT NULL,
  created_at timestamp with time zone,
  updated_at timestamp with time zone,
  tw_from character varying(20),
  tw_sms_sid character varying(256),
  tw_account_sid character varying(256),
  tw_to character varying(20),
  tw_body character varying(180),
  tw_from_city character varying(100),
  tw_from_state character varying(100),
  tw_from_zip character varying(15),
  tw_from_country character varying(100),
  tw_to_city character varying(100),
  tw_to_state character varying(100),
  tw_to_zip character varying(15),
  tw_to_country character varying(100),
  sent boolean,
  valid boolean,
  response character varying(180),
  CONSTRAINT messages_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE messages
  OWNER TO postgres;
