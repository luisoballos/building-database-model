from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=True)
    lastname: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # Relationships
    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    # Followers
    followers_rel: Mapped[List["Follower"]] = relationship(
        primaryjoin="User.id == Follower.user_to_id",
        back_populates="followed_user"
    )
    # Following
    following_rel: Mapped[List["Follower"]] = relationship(
        primaryjoin="User.id == Follower.user_from_id",
        back_populates="follower_user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationships:
    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(back_populates="post_rel")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post_rel")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # Relationships:
    post_rel: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text(), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # Relationships:
    author: Mapped["User"] = relationship(back_populates="comments")
    post_rel: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationships:
    follower_user: Mapped["User"] = relationship(
        foreign_keys=[user_from_id],
        back_populates="following_rel"
    )
    followed_user: Mapped["User"] = relationship(
        foreign_keys=[user_to_id],
        back_populates="followers_rel"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }