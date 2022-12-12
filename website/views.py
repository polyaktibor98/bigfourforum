from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .database_models import User, Post_nfl, Post_nba, Post_mlb, Post_nhl, Comment_nfl, Comment_nba, Comment_mlb, Comment_nhl, Like_nfl, Like_nba, Like_mlb, Like_nhl
from sqlalchemy import desc


views = Blueprint("views", __name__)


# HOME
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user_active=current_user)


# USER PROFILE
@views.route("/user/<username>")
@login_required
def user_profile(username):
    all_users = User.query.all()
    all_users_usernames = []
    for user in all_users:
        all_users_usernames.append(user.username)
    if username not in all_users_usernames:
        flash("There is no such user - " + username, category="error")
        return redirect(url_for("views.user_profile", username=current_user.username))
    else:
        specific_user_by_username = User.query.filter_by(
            username=username).first()
        return render_template("user_profile.html", user_active=current_user, specific_user_profile=specific_user_by_username)


# EDIT USER PROFILE
@views.route("/edit-user/<username>", methods=["GET", "POST"])
@login_required
def edit_user_profile(username):
    specific_user_by_username = User.query.filter_by(username=username).first()
    if specific_user_by_username != current_user:
        flash("You can only edit your profile!", category="error")
        return redirect(url_for("views.user_profile", username=current_user.username))
    else:
        pass
    if request.method == "POST":
        bio_edit = request.form.get("editUserBioTextArea")
        nfl_edit = request.form.get("editUserNflSelect")
        nba_edit = request.form.get("editUserNbaSelect")
        mlb_edit = request.form.get("editUserMlbSelect")
        nhl_edit = request.form.get("editUserNhlSelect")
        current_user.bio = bio_edit
        current_user.nfl = nfl_edit
        current_user.nba = nba_edit
        current_user.mlb = mlb_edit
        current_user.nhl = nhl_edit
        db.session.commit()
        flash("You have successfully edited your profile")
        return redirect(url_for("views.user_profile", username=current_user.username))
    else:
        pass
    return render_template("user_profile_edit.html", user_active=current_user)


# NFL
@views.route("/nfl-forum/<int:page_number>", methods=["GET", "POST"])
@login_required
def nfl_forum(page_number):
    posts_nfl_paginated = Post_nfl.query.order_by(desc('id')).paginate(
        per_page=3, page=page_number, error_out=True)

    # My profile-ról komment linkek
    if request.method == "POST":
        comment_to_post_id = request.form.get("nflCommentLinkToPostId")
        comment_to_post_object = Post_nfl.query.filter_by(
            id=comment_to_post_id).first()
        found_page = -1
        page_on = 1
        while page_on <= posts_nfl_paginated.pages:
            if comment_to_post_object in posts_nfl_paginated.items:
                found_page = page_on
                return redirect(url_for("views.nfl_forum", page_number=found_page))
            page_on += 1
            posts_nfl_paginated = posts_nfl_paginated.next()

    return render_template("forum_nfl.html", user_active=current_user, all_nfl_posts=posts_nfl_paginated)


@views.route("/create-forum-nfl-post", methods=["GET", "POST"])
@login_required
def create_forum_nfl_post():
    if request.method == "POST":
        text_of_post = request.form.get("createForumNflPostTextarea")
        if not text_of_post:
            flash("Post text area cannot be empty.")
        else:
            post_itself = Post_nfl(text=text_of_post, author=current_user.id)
            db.session.add(post_itself)
            db.session.commit()
            flash("Post created")
            return redirect(url_for("views.nfl_forum", page_number=1))
    return render_template("create_forum_nfl_post.html", user_active=current_user)


@views.route("/delete-forum-nfl-post/<id>", methods=["GET", "POST"])
@login_required
def delete_nfl_post(id):
    post_to_delete = Post_nfl.query.filter_by(id=id).first()
    if not post_to_delete:
        flash("Post does not exist.")
    elif current_user.id != post_to_delete.author:
        flash("You do not have permission to delete this post!", category="error")
    else:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted")
    current_page = int(request.form.get("currentPageForumNflDeletingPost"))
    # all_pages == az oldalak száma, egyben az utolsó oldal száma is
    all_pages = int(request.form.get("allPagesForumNflDeletingPost"))
    per_page = int(request.form.get("perPageForumNflDeletingPost"))
    total_left = int(request.form.get("totalForumNflDeletingPost"))-1
    max_total = per_page * all_pages
    if max_total - total_left == per_page and current_page == all_pages and current_page != 1:
        # ha az utolsó oldal eltűnik
        return redirect(url_for("views.nfl_forum", page_number=all_pages-1))
    else:
        return redirect(url_for("views.nfl_forum", page_number=current_page))


@views.route("/create-forum-nfl-comment/<post_id>", methods=["POST"])
@login_required
def create_forum_nfl_comment(post_id):
    text_of_comment = request.form.get("createForumNflCommentInput")
    if not text_of_comment:
        flash("Comment text area cannot be empty.")
    else:
        commented_post = Post_nfl.query.filter_by(id=post_id)
        if commented_post:
            comment_itself = Comment_nfl(
                text=text_of_comment, post_id=post_id, author=current_user.id)
            db.session.add(comment_itself)
            db.session.commit()
            flash("Comment added")
        else:
            flash("Post does not exist.")
    current_page = request.form.get("currentPageForumNflCommenting")
    return redirect(url_for("views.nfl_forum", page_number=current_page))


@views.route("/delete-forum-nfl-comment/<comment_id>", methods=["POST"])
@login_required
def delete_nfl_comment(comment_id):
    comment_to_delete = Comment_nfl.query.filter_by(id=comment_id).first()
    if not comment_to_delete:
        flash("Comment does not exist.")
    elif current_user.id != comment_to_delete.author and current_user.id != comment_to_delete.post_nfl.author:
        flash("You do not have permission to delete this comment!", category="error")
    else:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash("Comment deleted")
    current_page = request.form.get("currentPageForumNflDeletingComment")
    return redirect(url_for("views.nfl_forum", page_number=current_page))


@views.route("/like-forum-nfl/<post_id>", methods=["POST"])
@login_required
def like_nfl_post(post_id):
    liked_post = Post_nfl.query.filter_by(id=post_id).first()
    like_itself = Like_nfl.query.filter_by(
        post_id=post_id, author=current_user.id).first()
    if not liked_post:
        flash("Post does not exist.")
    else:
        if current_user.id != liked_post.author:
            if like_itself:
                db.session.delete(like_itself)
                db.session.commit()
            else:
                like_itself = Like_nfl(post_id=post_id, author=current_user.id)
                db.session.add(like_itself)
                db.session.commit()
        else:
            pass
    current_page = request.form.get("currentPageForumNflLiking")
    return redirect(url_for("views.nfl_forum", page_number=current_page))


@views.route("/nfl-facts")
def nfl_facts():
    return render_template("facts_nfl.html", user_active=current_user)


@views.route("/nfl-tickets")
def nfl_tickets():
    return render_template("tickets_nfl.html", user_active=current_user)


# NBA
@views.route("/nba-forum/<int:page_number>", methods=["GET", "POST"])
@login_required
def nba_forum(page_number):
    posts_nba_paginated = Post_nba.query.order_by(desc('id')).paginate(
        per_page=3, page=page_number, error_out=True)

    # My profile-ról komment linkek
    if request.method == "POST":
        comment_to_post_id = request.form.get("nbaCommentLinkToPostId")
        comment_to_post_object = Post_nba.query.filter_by(
            id=comment_to_post_id).first()
        found_page = -1
        page_on = 1
        while page_on <= posts_nba_paginated.pages:
            if comment_to_post_object in posts_nba_paginated.items:
                found_page = page_on
                return redirect(url_for("views.nba_forum", page_number=found_page))
            page_on += 1
            posts_nba_paginated = posts_nba_paginated.next()

    return render_template("forum_nba.html", user_active=current_user, all_nba_posts=posts_nba_paginated)


@views.route("/create-forum-nba-post", methods=["GET", "POST"])
@login_required
def create_forum_nba_post():
    if request.method == "POST":
        text_of_post = request.form.get("createForumNbaPostTextarea")
        if not text_of_post:
            flash("Post text area cannot be empty.")
        else:
            post_itself = Post_nba(text=text_of_post, author=current_user.id)
            db.session.add(post_itself)
            db.session.commit()
            flash("Post created")
            return redirect(url_for("views.nba_forum", page_number=1))
    return render_template("create_forum_nba_post.html", user_active=current_user)


@views.route("/delete-forum-nba-post/<id>", methods=["GET", "POST"])
@login_required
def delete_nba_post(id):
    post_to_delete = Post_nba.query.filter_by(id=id).first()
    if not post_to_delete:
        flash("Post does not exist.")
    elif current_user.id != post_to_delete.author:
        flash("You do not have permission to delete this post!", category="error")
    else:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted")
    current_page = int(request.form.get("currentPageForumNbaDeletingPost"))
    # all_pages == az oldalak száma, egyben az utolsó oldal száma is
    all_pages = int(request.form.get("allPagesForumNbaDeletingPost"))
    per_page = int(request.form.get("perPageForumNbaDeletingPost"))
    total_left = int(request.form.get("totalForumNbaDeletingPost"))-1
    max_total = per_page * all_pages
    if max_total - total_left == per_page and current_page == all_pages and current_page != 1:
        # ha az utolsó oldal eltűnik
        return redirect(url_for("views.nba_forum", page_number=all_pages-1))
    else:
        return redirect(url_for("views.nba_forum", page_number=current_page))


@views.route("/create-forum-nba-comment/<post_id>", methods=["POST"])
@login_required
def create_forum_nba_comment(post_id):
    text_of_comment = request.form.get("createForumNbaCommentInput")
    if not text_of_comment:
        flash("Comment text area cannot be empty.")
    else:
        commented_post = Post_nba.query.filter_by(id=post_id)
        if commented_post:
            comment_itself = Comment_nba(
                text=text_of_comment, post_id=post_id, author=current_user.id)
            db.session.add(comment_itself)
            db.session.commit()
            flash("Comment added")
        else:
            flash("Post does not exist.")
    current_page = request.form.get("currentPageForumNbaCommenting")
    return redirect(url_for("views.nba_forum", page_number=current_page))


@views.route("/delete-forum-nba-comment/<comment_id>", methods=["POST"])
@login_required
def delete_nba_comment(comment_id):
    comment_to_delete = Comment_nba.query.filter_by(id=comment_id).first()
    if not comment_to_delete:
        flash("Comment does not exist.")
    elif current_user.id != comment_to_delete.author and current_user.id != comment_to_delete.post_nba.author:
        flash("You do not have permission to delete this comment!", category="error")
    else:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash("Comment deleted")
    current_page = request.form.get("currentPageForumNbaDeletingComment")
    return redirect(url_for("views.nba_forum", page_number=current_page))


@views.route("/like-forum-nba/<post_id>", methods=["POST"])
@login_required
def like_nba_post(post_id):
    liked_post = Post_nba.query.filter_by(id=post_id).first()
    like_itself = Like_nba.query.filter_by(
        post_id=post_id, author=current_user.id).first()
    if not liked_post:
        flash("Post does not exist.")
    else:
        if current_user.id != liked_post.author:
            if like_itself:
                db.session.delete(like_itself)
                db.session.commit()
            else:
                like_itself = Like_nba(post_id=post_id, author=current_user.id)
                db.session.add(like_itself)
                db.session.commit()
        else:
            pass
    current_page = request.form.get("currentPageForumNbaLiking")
    return redirect(url_for("views.nba_forum", page_number=current_page))


@views.route("/nba-facts")
def nba_facts():
    return render_template("facts_nba.html", user_active=current_user)


@views.route("/nba-tickets")
def nba_tickets():
    return render_template("tickets_nba.html", user_active=current_user)


# MLB
@views.route("/mlb-forum/<int:page_number>", methods=["GET", "POST"])
@login_required
def mlb_forum(page_number):
    posts_mlb_paginated = Post_mlb.query.order_by(desc('id')).paginate(
        per_page=3, page=page_number, error_out=True)

    # My profile-ról komment link megoldás
    if request.method == "POST":
        comment_to_post_id = request.form.get("mlbCommentLinkToPostId")
        comment_to_post_object = Post_mlb.query.filter_by(
            id=comment_to_post_id).first()
        found_page = -1
        page_on = 1
        while page_on <= posts_mlb_paginated.pages:
            if comment_to_post_object in posts_mlb_paginated.items:
                found_page = page_on
                return redirect(url_for("views.mlb_forum", page_number=found_page))
            page_on += 1
            posts_mlb_paginated = posts_mlb_paginated.next()

    return render_template("forum_mlb.html", user_active=current_user, all_mlb_posts=posts_mlb_paginated)


@views.route("/create-forum-mlb-post", methods=["GET", "POST"])
@login_required
def create_forum_mlb_post():
    if request.method == "POST":
        text_of_post = request.form.get("createForumMlbPostTextarea")
        if not text_of_post:
            flash("Post text area cannot be empty.")
        else:
            post_itself = Post_mlb(text=text_of_post, author=current_user.id)
            db.session.add(post_itself)
            db.session.commit()
            flash("Post created")
            return redirect(url_for("views.mlb_forum", page_number=1))
    return render_template("create_forum_mlb_post.html", user_active=current_user)


@views.route("/delete-forum-mlb-post/<id>", methods=["GET", "POST"])
@login_required
def delete_mlb_post(id):
    post_to_delete = Post_mlb.query.filter_by(id=id).first()
    if not post_to_delete:
        flash("Post does not exist.")
    elif current_user.id != post_to_delete.author:
        flash("You do not have permission to delete this post!", category="error")
    else:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted")
    current_page = int(request.form.get("currentPageForumMlbDeletingPost"))
    # all_pages == az oldalak száma, egyben az utolsó oldal száma is
    all_pages = int(request.form.get("allPagesForumMlbDeletingPost"))
    per_page = int(request.form.get("perPageForumMlbDeletingPost"))
    total_left = int(request.form.get("totalForumMlbDeletingPost"))-1
    max_total = per_page * all_pages
    if max_total - total_left == per_page and current_page == all_pages and current_page != 1:
        # ha az utolsó oldal eltűnik
        return redirect(url_for("views.mlb_forum", page_number=all_pages-1))
    else:
        return redirect(url_for("views.mlb_forum", page_number=current_page))


@views.route("/create-forum-mlb-comment/<post_id>", methods=["POST"])
@login_required
def create_forum_mlb_comment(post_id):
    text_of_comment = request.form.get("createForumMlbCommentInput")
    if not text_of_comment:
        flash("Comment text area cannot be empty.")
    else:
        commented_post = Post_mlb.query.filter_by(id=post_id)
        if commented_post:
            comment_itself = Comment_mlb(
                text=text_of_comment, post_id=post_id, author=current_user.id)
            db.session.add(comment_itself)
            db.session.commit()
            flash("Comment added")
        else:
            flash("Post does not exist.")
    current_page = request.form.get("currentPageForumMlbCommenting")
    return redirect(url_for("views.mlb_forum", page_number=current_page))


@views.route("/delete-forum-mlb-comment/<comment_id>", methods=["POST"])
@login_required
def delete_mlb_comment(comment_id):
    comment_to_delete = Comment_mlb.query.filter_by(id=comment_id).first()
    if not comment_to_delete:
        flash("Comment does not exist.")
    elif current_user.id != comment_to_delete.author and current_user.id != comment_to_delete.post_mlb.author:
        flash("You do not have permission to delete this comment!", category="error")
    else:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash("Comment deleted")
    current_page = request.form.get("currentPageForumMlbDeletingComment")
    return redirect(url_for("views.mlb_forum", page_number=current_page))


@views.route("/like-forum-mlb/<post_id>", methods=["POST"])
@login_required
def like_mlb_post(post_id):
    liked_post = Post_mlb.query.filter_by(id=post_id).first()
    like_itself = Like_mlb.query.filter_by(
        post_id=post_id, author=current_user.id).first()
    if not liked_post:
        flash("Post does not exist.")
    else:
        if current_user.id != liked_post.author:
            if like_itself:
                db.session.delete(like_itself)
                db.session.commit()
            else:
                like_itself = Like_mlb(post_id=post_id, author=current_user.id)
                db.session.add(like_itself)
                db.session.commit()
        else:
            pass
    current_page = request.form.get("currentPageForumMlbLiking")
    return redirect(url_for("views.mlb_forum", page_number=current_page))


@views.route("/mlb-facts")
def mlb_facts():
    return render_template("facts_mlb.html", user_active=current_user)


@views.route("/mlb-tickets")
def mlb_tickets():
    return render_template("tickets_mlb.html", user_active=current_user)


# NHL
@views.route("/nhl-forum/<int:page_number>", methods=["GET", "POST"])
@login_required
def nhl_forum(page_number):
    posts_nhl_paginated = Post_nhl.query.order_by(desc('id')).paginate(
        per_page=3, page=page_number, error_out=True)

    # My profile-ról komment link megoldás
    if request.method == "POST":
        comment_to_post_id = request.form.get("nhlCommentLinkToPostId")
        comment_to_post_object = Post_nhl.query.filter_by(
            id=comment_to_post_id).first()
        found_page = -1
        page_on = 1
        while page_on <= posts_nhl_paginated.pages:
            if comment_to_post_object in posts_nhl_paginated.items:
                found_page = page_on
                return redirect(url_for("views.nhl_forum", page_number=found_page))
            page_on += 1
            posts_nhl_paginated = posts_nhl_paginated.next()

    return render_template("forum_nhl.html", user_active=current_user, all_nhl_posts=posts_nhl_paginated)


@views.route("/create-forum-nhl-post", methods=["GET", "POST"])
@login_required
def create_forum_nhl_post():
    if request.method == "POST":
        text_of_post = request.form.get("createForumNhlPostTextarea")
        if not text_of_post:
            flash("Post text area cannot be empty.")
        else:
            post_itself = Post_nhl(text=text_of_post, author=current_user.id)
            db.session.add(post_itself)
            db.session.commit()
            flash("Post created")
            return redirect(url_for("views.nhl_forum", page_number=1))
    return render_template("create_forum_nhl_post.html", user_active=current_user)


@views.route("/delete-forum-nhl-post/<id>", methods=["GET", "POST"])
@login_required
def delete_nhl_post(id):
    post_to_delete = Post_nhl.query.filter_by(id=id).first()
    if not post_to_delete:
        flash("Post does not exist.")
    elif current_user.id != post_to_delete.author:
        flash("You do not have permission to delete this post!", category="error")
    else:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted")
    current_page = int(request.form.get("currentPageForumNhlDeletingPost"))
    # all_pages == az oldalak száma, egyben az utolsó oldal száma is
    all_pages = int(request.form.get("allPagesForumNhlDeletingPost"))
    per_page = int(request.form.get("perPageForumNhlDeletingPost"))
    total_left = int(request.form.get("totalForumNhlDeletingPost"))-1
    max_total = per_page * all_pages
    if max_total - total_left == per_page and current_page == all_pages and current_page != 1:
        # ha az utolsó oldal eltűnik
        return redirect(url_for("views.nhl_forum", page_number=all_pages-1))
    else:
        return redirect(url_for("views.nhl_forum", page_number=current_page))


@views.route("/create-forum-nhl-comment/<post_id>", methods=["POST"])
@login_required
def create_forum_nhl_comment(post_id):
    text_of_comment = request.form.get("createForumNhlCommentInput")
    if not text_of_comment:
        flash("Comment text area cannot be empty.")
    else:
        commented_post = Post_nhl.query.filter_by(id=post_id)
        if commented_post:
            comment_itself = Comment_nhl(
                text=text_of_comment, post_id=post_id, author=current_user.id)
            db.session.add(comment_itself)
            db.session.commit()
            flash("Comment added")
        else:
            flash("Post does not exist.")
    current_page = request.form.get("currentPageForumNhlCommenting")
    return redirect(url_for("views.nhl_forum", page_number=current_page))


@views.route("/delete-forum-nhl-comment/<comment_id>", methods=["POST"])
@login_required
def delete_nhl_comment(comment_id):
    comment_to_delete = Comment_nhl.query.filter_by(id=comment_id).first()
    if not comment_to_delete:
        flash("Comment does not exist.")
    elif current_user.id != comment_to_delete.author and current_user.id != comment_to_delete.post_nhl.author:
        flash("You do not have permission to delete this comment!", category="error")
    else:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash("Comment deleted")
    current_page = request.form.get("currentPageForumNhlDeletingComment")
    return redirect(url_for("views.nhl_forum", page_number=current_page))


@views.route("/like-forum-nhl/<post_id>", methods=["POST"])
@login_required
def like_nhl_post(post_id):
    liked_post = Post_nhl.query.filter_by(id=post_id).first()
    like_itself = Like_nhl.query.filter_by(
        post_id=post_id, author=current_user.id).first()
    if not liked_post:
        flash("Post does not exist.")
    else:
        if current_user.id != liked_post.author:
            if like_itself:
                db.session.delete(like_itself)
                db.session.commit()
            else:
                like_itself = Like_nhl(post_id=post_id, author=current_user.id)
                db.session.add(like_itself)
                db.session.commit()
        else:
            pass
    current_page = request.form.get("currentPageForumNhlLiking")
    return redirect(url_for("views.nhl_forum", page_number=current_page))


@views.route("/nhl-facts")
def nhl_facts():
    return render_template("facts_nhl.html", user_active=current_user)


@views.route("/nhl-tickets")
def nhl_tickets():
    return render_template("tickets_nhl.html", user_active=current_user)
