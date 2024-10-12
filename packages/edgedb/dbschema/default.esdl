module default {
  type Person {
    required name: str;
  }

  type Rule {
    title: str;
    multi owner: Person;
  }
};