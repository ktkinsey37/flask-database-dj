### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?

This is an implementation of the SQL language used to build and manage databases.

- What is the difference between SQL and PostgreSQL?

SQL is a language and protocol,  PostgreSQL is a program that uses SQL

- In `psql`, how do you connect to a database?

\c database;

- What is the difference between `HAVING` and `WHERE`?

Having is used for groups, while where can be single instances.

- What is the difference between an `INNER` and `OUTER` join?

An inner join shows areas where both pieces of data have overlap (so in a list of employees, it might show only employees where a department has a telephone number, while leaving out depts without phone numbers). In an outer join, all pieces of data called for are present.

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?

This differentiates between which table takes preference when choosing which other information to fetch

- What is an ORM? What do they do?

An object relational mapper is a program that bridges the gap between raw SQL data and programming-language-based objects.

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?

Using ajax can be done with javascript without rendering a new browser page, and the information can be played with in javascript by the client side browser. Requests from the server-side can be much more controlled and managed with what information gets passed to what route or URL or API

- What is CSRF? What is the purpose of the CSRF token?

Cross site request forgery is a protocol of sending an authorization token along with form data to prevent cross scripting (where malicious data is sent in a form)

- What is the purpose of `form.hidden_tag()`?

This tag renders hidden form data to be sent, in most cases the CSRF auth token.
