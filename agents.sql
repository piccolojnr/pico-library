-- ************************************** "public".agent_type

CREATE TABLE "public".agent_type
(
 "id"   integer NOT NULL,
 name character NULL,
 CONSTRAINT agent_type_pkey PRIMARY KEY ( "id" )
);


-- ************************************** "public".agents
CREATE TABLE "public".agents
(
 "id"         integer NOT NULL,
 name       character NULL,
 alias      character NULL,
 birth_date character NULL,
 death_date character NULL,
 webpage    character NULL,
 type_id    integer NULL,
 CONSTRAINT agents_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT agents_type_id_name_alias_birth_date_death_date_webpage_key UNIQUE ( type_id, name, alias, birth_date, death_date, webpage ),
 CONSTRAINT agents_type_id_fkey FOREIGN KEY ( type_id ) REFERENCES "public".agent_type ( "id" ) ON DELETE CASCADE
);



-- ************************************** "public".book_agents
CREATE TABLE "public".book_agents
(
 book_id  integer NOT NULL,
 agent_id integer NOT NULL,
 CONSTRAINT book_agents_pkey PRIMARY KEY ( book_id, agent_id ),
 CONSTRAINT book_agents_agent_id_fkey FOREIGN KEY ( agent_id ) REFERENCES "public".agents ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_agents_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE
);








