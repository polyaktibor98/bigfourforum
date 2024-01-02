# bigfourforum
(Szakdolgozat)

This is a forum-like web application hosted on render.com.
The main topic is the four USA major leagues, frequently referred as "Big Four" - NFL, NBA, MLB, NHL.
I have used Python and the Flask web framework, along with SQLite (later PostreSQL) and SQLAlchemy ORM to maintain the backend functionality.
In terms of frontend, I have used HTML, Bootstrap, and Jinja trio (no JavaScript).

The application is available at the following URL - https://big-four-forum.onrender.com/

-------

The SQLite "problem" - https://community.render.com/t/python-sqlite3/7540

Every time, when the Render servers restarted, the SQLite database lost its content.
Since I am using the Free Plan on Render, I had to use its PostgreSQL database feature.

-------

This is a personal project and currently I don't intend to change to a paid plan on Render.
Therefore, I must create and use a new free PostgreSQL database every 90 days.

2023.03.24. - New database

2024.01.02. - New database