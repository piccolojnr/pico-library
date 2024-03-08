
-- ************************************** "public".resource_type

CREATE TABLE IF NOT EXISTS "public".resource_type
(
 "id"   integer NOT NULL,
 name character NULL,
 CONSTRAINT resource_type_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT resource_type_name_key UNIQUE ( name )
);


-- ************************************** "public".book_resources

CREATE TABLE IF NOT EXISTS "public".book_resources
(
 book_id     integer NOT NULL,
 resource_id integer NOT NULL,
 CONSTRAINT book_resources_pkey PRIMARY KEY ( book_id, resource_id ),
 CONSTRAINT book_resources_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_resources_resource_id_fkey FOREIGN KEY ( resource_id ) REFERENCES "public".resources ( "id" ) ON DELETE CASCADE
);


-- ************************************** "public".resources

CREATE TABLE IF NOT EXISTS "public".resources
(
 "id"       integer NOT NULL,
 url      character NULL,
 "size"     integer NULL,
 modified timestamp NULL,
 type_id  integer NULL,
 CONSTRAINT resources_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT resources_url_key UNIQUE ( url ),
 CONSTRAINT resources_type_id_fkey FOREIGN KEY ( type_id ) REFERENCES "public".resource_type ( "id" )
);



