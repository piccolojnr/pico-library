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
-- ************************************** "public".book_languages

CREATE TABLE IF NOT EXISTS "public".book_languages
(
 book_id     integer NOT NULL,
 language_id character NOT NULL,
 CONSTRAINT book_languages_pkey PRIMARY KEY ( book_id, language_id ),
 CONSTRAINT book_languages_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_languages_language_id_fkey FOREIGN KEY ( language_id ) REFERENCES "public".languages ( code ) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "public".languages
(
 code character NOT NULL,
 CONSTRAINT languages_pkey PRIMARY KEY ( code )
);

-- ************************************** "public".book_bookshelves

CREATE TABLE "public".book_bookshelves
(
 book_id      integer NOT NULL,
 bookshelf_id integer NOT NULL,
 CONSTRAINT book_bookshelves_pkey PRIMARY KEY ( book_id, bookshelf_id ),
 CONSTRAINT book_bookshelves_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_bookshelves_bookshelf_id_fkey FOREIGN KEY ( bookshelf_id ) REFERENCES "public".bookshelves ( "id" ) ON DELETE CASCADE
);

-- ************************************** "public".bookshelves

CREATE TABLE IF NOT EXISTS "public".bookshelves
(
 "id"   integer NOT NULL,
 name character NULL,
 CONSTRAINT bookshelves_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT bookshelves_name_key UNIQUE ( name )
);
-- ************************************** "public".book_publishers

CREATE TABLE IF NOT EXISTS "public".book_publishers
(
 book_id      integer NOT NULL,
 publisher_id character NOT NULL,
 CONSTRAINT book_publishers_pkey PRIMARY KEY ( book_id, publisher_id ),
 CONSTRAINT book_publishers_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_publishers_publisher_id_fkey FOREIGN KEY ( publisher_id ) REFERENCES "public".publishers ( name ) ON DELETE CASCADE
);


-- ************************************** "public".publishers

CREATE TABLE IF NOT EXISTS "public".publishers
(
 name character NOT NULL,
 CONSTRAINT publishers_pkey PRIMARY KEY ( name )
);

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
-- ************************************** "public".book_subjects

CREATE TABLE IF NOT EXISTS "public".book_subjects
(
 book_id    integer NOT NULL,
 subject_id integer NOT NULL,
 CONSTRAINT book_subjects_pkey PRIMARY KEY ( book_id, subject_id ),
 CONSTRAINT book_subjects_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_subjects_subject_id_fkey FOREIGN KEY ( subject_id ) REFERENCES "public".subjects ( "id" ) ON DELETE CASCADE
);


-- ************************************** "public".subjects

CREATE TABLE IF NOT EXISTS "public".subjects
(
 "id"   integer NOT NULL,
 name character NULL,
 CONSTRAINT subjects_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT subjects_name_key UNIQUE ( name )
);
-- ************************************** "public".books

CREATE TABLE IF NOT EXISTS "public".books
(
 "id"           integer NOT NULL,
 "format"       character NULL,
 title        character NULL,
 description  text NULL,
 downloads    integer NULL,
 license      character NULL,
 date_created timestamp NULL,
 CONSTRAINT books_pkey PRIMARY KEY ( "id" )
);



-- ************************************** "public".bookmarks

CREATE TABLE IF NOT EXISTS "public".bookmarks
(
 user_id    integer NOT NULL,
 book_id    integer NOT NULL,
 status     public NULL,
 last_read  timestamp NOT NULL,
 created_at timestamp NULL,
 CONSTRAINT bookmarks_pkey PRIMARY KEY ( user_id, book_id ),
 CONSTRAINT bookmarks_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT bookmarks_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);
-- ************************************** "public".comment_votes

CREATE TABLE IF NOT EXISTS "public".comment_votes
(
 "id"         integer NOT NULL,
 vote_type  public NULL,
 created_at timestamp NULL,
 updated_at timestamp NULL,
 comment_id integer NULL,
 user_id    integer NULL,
 CONSTRAINT comment_votes_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT comment_votes_comment_id_fkey FOREIGN KEY ( comment_id ) REFERENCES "public".comments ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comment_votes_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);


-- ************************************** "public".comments

CREATE TABLE IF NOT EXISTS "public".comments
(
 "id"         integer NOT NULL,
 content    text NULL,
 created_at timestamp NULL,
 updated_at timestamp NULL,
 book_id    integer NULL,
 user_id    integer NULL,
 parent_id  integer NULL,
 review_id  integer NULL,
 CONSTRAINT comments_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT comments_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comments_parent_id_fkey FOREIGN KEY ( parent_id ) REFERENCES "public".comments ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comments_review_id_fkey FOREIGN KEY ( review_id ) REFERENCES "public".reviews ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comments_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);
-- ************************************** "public".profile

CREATE TABLE IF NOT EXISTS "public".profile
(
 "id"            integer NOT NULL,
 user_id       integer NULL,
 full_name     character NULL,
 bio           text NULL,
 occupation    character NULL,
 location      character NULL,
 profile_image character NULL,
 created_at    timestamp NULL,
 CONSTRAINT profile_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT profile_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);
-- ************************************** "public".reviews

CREATE TABLE IF NOT EXISTS "public".reviews
(
 "id"         integer NOT NULL,
 title      character NOT NULL,
 review     character NOT NULL,
 book_id    integer NOT NULL,
 user_id    integer NOT NULL,
 created_at timestamp NULL,
 CONSTRAINT reviews_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT reviews_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT reviews_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);

-- ************************************** "public".ratings

CREATE TABLE IF NOT EXISTS "public".ratings
(
 user_id integer NOT NULL,
 book_id integer NOT NULL,
 rating  double NULL,
 CONSTRAINT ratings_pkey PRIMARY KEY ( user_id, book_id ),
 CONSTRAINT ratings_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT ratings_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);
-- ************************************** "public".users

CREATE TABLE IF NOT EXISTS "public".users
(
 "id"             integer NOT NULL,
 email          character NULL,
 gender         public NOT NULL,
 password_hash  character NULL,
 created_at     timestamp NULL,
 last_logged_in timestamp NULL,
 CONSTRAINT users_pkey PRIMARY KEY ( "id" )
);
