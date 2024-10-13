using extension auth;

module default {
  scalar type RuleImportance extending enum<important, normal>;

  global current_user := (
    assert_single((
      select User
      filter .identity = global ext::auth::ClientTokenIdentity
    ))
  );

  type User {
    required identity: ext::auth::Identity {
      constraint exclusive;
    };
    required name: str;
    email: str {
      constraint exclusive;
    };
    phone_number: str;

    created: datetime {
      rewrite insert using (datetime_of_statement());
    }
    updated: datetime {
      rewrite insert using (datetime_of_statement());
      rewrite update using (datetime_of_statement());
    }

    access policy current_user_has_full_access
      allow all
      using (.id ?= global current_user.id);
    access policy everyone_insert_only
      allow insert;
  }

  type CallScreeningRule {
    required description: str;
    importance: RuleImportance {
      default := RuleImportance.normal;
    };
    expiry_date: datetime;
    required created_by: User {
      default := global current_user;
    }

    created: datetime {
      rewrite insert using (datetime_of_statement());
    }
    updated: datetime {
      rewrite insert using (datetime_of_statement());
      rewrite update using (datetime_of_statement());
    }

    access policy creator_has_full_access
      allow all
      using (.created_by ?= global current_user);
    access policy others_read_only
      allow select;
  }
}