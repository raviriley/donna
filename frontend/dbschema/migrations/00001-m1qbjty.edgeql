CREATE MIGRATION m1qbjtyxphk5ldpkft6udqu3eo3sasm5wqd6vmxgsaqslojsw6w2ja
    ONTO initial
{
  CREATE EXTENSION pgcrypto VERSION '1.3';
  CREATE EXTENSION auth VERSION '1.0';
  CREATE TYPE default::Person {
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY phone_number: std::str;
  };
  CREATE TYPE default::Rule {
      CREATE MULTI LINK owner: default::Person;
      CREATE PROPERTY title: std::str;
  };
};
