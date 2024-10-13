CREATE MIGRATION m1xevzcsp4wnjdh7ozkxql62mga4etzfzfmydvoqdki2gijcftwl4a
    ONTO m1qbjtyxphk5ldpkft6udqu3eo3sasm5wqd6vmxgsaqslojsw6w2ja
{
  CREATE TYPE default::User {
      CREATE REQUIRED LINK identity: ext::auth::Identity {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY created: std::datetime {
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
      };
      CREATE PROPERTY email: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY phone_number: std::str;
      CREATE PROPERTY updated: std::datetime {
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_of_statement());
      };
      CREATE ACCESS POLICY everyone_insert_only
          ALLOW INSERT ;
  };
  CREATE GLOBAL default::current_user := (std::assert_single((SELECT
      default::User
  FILTER
      (.identity = GLOBAL ext::auth::ClientTokenIdentity)
  )));
  CREATE SCALAR TYPE default::RuleImportance EXTENDING enum<important, normal>;
  CREATE TYPE default::CallScreeningRule {
      CREATE REQUIRED LINK created_by: default::User {
          SET default := (GLOBAL default::current_user);
      };
      CREATE ACCESS POLICY creator_has_full_access
          ALLOW ALL USING ((.created_by ?= GLOBAL default::current_user));
      CREATE ACCESS POLICY others_read_only
          ALLOW SELECT ;
      CREATE PROPERTY created: std::datetime {
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
      };
      CREATE REQUIRED PROPERTY description: std::str;
      CREATE PROPERTY expiry_date: std::datetime;
      CREATE PROPERTY importance: default::RuleImportance {
          SET default := (default::RuleImportance.normal);
      };
      CREATE PROPERTY updated: std::datetime {
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_of_statement());
      };
  };
  ALTER TYPE default::User {
      CREATE ACCESS POLICY current_user_has_full_access
          ALLOW ALL USING ((.id ?= (GLOBAL default::current_user).id));
  };
  ALTER TYPE default::Person {
      DROP PROPERTY name;
      DROP PROPERTY phone_number;
  };
  DROP TYPE default::Rule;
  DROP TYPE default::Person;
};
