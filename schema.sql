drop table if exists googleauth;
create table googleauth (
  id integer primary key autoincrement,
  username text not null,
  secret_key text not null,
  last_number text
);