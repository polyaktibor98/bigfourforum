from . import db
from flask_login import UserMixin
from datetime import datetime

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/


# USER
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    bio = db.Column(db.String(1000))
    nfl = db.Column(db.String(100))
    nba = db.Column(db.String(100))
    mlb = db.Column(db.String(100))
    nhl = db.Column(db.String(100))
    posts_forum_nfl = db.relationship(
        "Post_nfl", backref="user", passive_deletes=True)
    posts_forum_nba = db.relationship(
        "Post_nba", backref="user", passive_deletes=True)
    posts_forum_mlb = db.relationship(
        "Post_mlb", backref="user", passive_deletes=True)
    posts_forum_nhl = db.relationship(
        "Post_nhl", backref="user", passive_deletes=True)
    comments_forum_nfl = db.relationship(
        "Comment_nfl", backref="user", passive_deletes=True)
    comments_forum_nba = db.relationship(
        "Comment_nba", backref="user", passive_deletes=True)
    comments_forum_mlb = db.relationship(
        "Comment_mlb", backref="user", passive_deletes=True)
    comments_forum_nhl = db.relationship(
        "Comment_nhl", backref="user", passive_deletes=True)
    likes_forum_nfl = db.relationship(
        "Like_nfl", backref="user", passive_deletes=True)
    likes_forum_nba = db.relationship(
        "Like_nba", backref="user", passive_deletes=True)
    likes_forum_mlb = db.relationship(
        "Like_mlb", backref="user", passive_deletes=True)
    likes_forum_nhl = db.relationship(
        "Like_nhl", backref="user", passive_deletes=True)


# Posztok
class Post_nfl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_of_post = db.Column(db.DateTime(
        timezone=True), default=datetime.now)
    comments_forum_nfl = db.relationship(
        "Comment_nfl", back_populates="post_nfl", cascade="all, delete, delete-orphan")
    likes_forum_nfl = db.relationship(
        "Like_nfl", back_populates="post_nfl", cascade="all, delete, delete-orphan")


class Post_nba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_of_post = db.Column(db.DateTime(timezone=True), default=datetime.now)
    comments_forum_nba = db.relationship(
        "Comment_nba", back_populates="post_nba", cascade="all, delete, delete-orphan")
    likes_forum_nba = db.relationship(
        "Like_nba", back_populates="post_nba", cascade="all, delete, delete-orphan")


class Post_mlb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_of_post = db.Column(db.DateTime(timezone=True), default=datetime.now)
    comments_forum_mlb = db.relationship(
        "Comment_mlb", back_populates="post_mlb", cascade="all, delete, delete-orphan")
    likes_forum_mlb = db.relationship(
        "Like_mlb", back_populates="post_mlb", cascade="all, delete, delete-orphan")


class Post_nhl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_of_post = db.Column(db.DateTime(timezone=True), default=datetime.now)
    comments_forum_nhl = db.relationship(
        "Comment_nhl", back_populates="post_nhl", cascade="all, delete, delete-orphan")
    likes_forum_nhl = db.relationship(
        "Like_nhl", back_populates="post_nhl", cascade="all, delete, delete-orphan")


# Hozzászólások
class Comment_nfl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_nfl.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_nfl = db.relationship("Post_nfl", back_populates="comments_forum_nfl")
    text = db.Column(db.String(200), nullable=False)
    date_of_comment = db.Column(db.DateTime(
        timezone=True), default=datetime.now)


class Comment_nba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_nba.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_nba = db.relationship("Post_nba", back_populates="comments_forum_nba")
    text = db.Column(db.String(200), nullable=False)
    date_of_comment = db.Column(db.DateTime(
        timezone=True), default=datetime.now)


class Comment_mlb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_mlb.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_mlb = db.relationship("Post_mlb", back_populates="comments_forum_mlb")
    text = db.Column(db.String(200), nullable=False)
    date_of_comment = db.Column(db.DateTime(
        timezone=True), default=datetime.now)


class Comment_nhl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_nhl.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_nhl = db.relationship("Post_nhl", back_populates="comments_forum_nhl")
    text = db.Column(db.String(200), nullable=False)
    date_of_comment = db.Column(db.DateTime(
        timezone=True), default=datetime.now)


# Lájkok
class Like_nfl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_nfl.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_nfl = db.relationship("Post_nfl", back_populates="likes_forum_nfl")


class Like_nba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_nba.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_nba = db.relationship("Post_nba", back_populates="likes_forum_nba")


class Like_mlb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_mlb.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_mlb = db.relationship("Post_mlb", back_populates="likes_forum_mlb")


class Like_nhl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post_nhl.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_nhl = db.relationship("Post_nhl", back_populates="likes_forum_nhl")
