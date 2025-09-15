# from flask import Blueprint, request, jsonify
# from extensions import db
# from models.post import Post
# from flask_jwt_extended import jwt_required
# from datetime import datetime

# posts_bp = Blueprint("posts_bp", __name__)

# # GET all posts
# @posts_bp.route("/", methods=["GET"])
# def get_posts():
#     posts = Post.query.order_by(Post.postTime.desc()).all()
#     return jsonify([{
#         "id": p.id,
#         "userName": p.userName,
#         "userRole": p.userRole,
#         "avatar": p.avatar,
#         "postText": p.postText,
#         "postImage": p.postImage,
#         "postTime": p.postTime.isoformat()
#     } for p in posts])

# # CREATE post
# @posts_bp.route("/", methods=["POST"])
# def create_post():  # temporarily remove jwt_required for testing
#     data = request.get_json()
#     post = Post(
#         user_id=data.get("user_id"),
#         user_name=data.get("user_name", "Unknown"),
#         user_role=data.get("user_role", "Community Member"),
#         avatar=data.get("avatar"),
#         post_text=data.get("post_text"),
#         post_image=data.get("post_image"),
#         post_time=datetime.utcnow() )


#     db.session.add(post)
#     db.session.commit()
#     return jsonify({
#     "id": post.user_id,
#     "userName": post.user_name,
#     "userRole": post.user_role,
#     "avatar": post.avatar,
#     "postText": post.post_text,
#     "postImage": post.post_image,
#     "postTime": post.post_time.isoformat()
# }), 201


# # UPDATE post
# @posts_bp.route("/<int:post_id>", methods=["PUT"])
# @jwt_required()
# def update_post(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({"msg": "Post not found"}), 404
#     data = request.get_json()
#     post.postText = data.get("postText", post.postText)
#     post.postImage = data.get("postImage", post.postImage)
#     db.session.commit()
#     return jsonify({
#         "id": post.id,
#         "postText": post.postText,
#         "postImage": post.postImage
#     })

# # DELETE post
# @posts_bp.route("/<int:post_id>", methods=["DELETE"])
# @jwt_required()
# def delete_post(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({"msg": "Post not found"}), 404
#     db.session.delete(post)
#     db.session.commit()
#     return jsonify({"msg": "Deleted"})
from flask import Blueprint, request, jsonify
from extensions import db
from models.post import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

posts_bp = Blueprint("posts_bp", __name__)


# GET all posts
@posts_bp.route("/", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.post_time.desc()).all()
    return jsonify(
        [
            {
                "id": p.id,
                "userId": p.user_id,
                "userName": p.user_name,
                "userRole": p.user_role,
                "avatar": p.avatar,
                "postText": p.post_text,
                "postImage": p.post_image,
                "postTime": p.post_time.isoformat(),
            }
            for p in posts
        ]
    )


# CREATE post
@posts_bp.post("")
@posts_bp.post("/")
def create_post():  # add @jwt_required() later
    data = request.get_json()
    post = Post(
        user_id=data.get("user_id"),  # ⚠️ must not be None
        user_name=data.get("user_name", "Unknown"),
        user_role=data.get("user_role", "Community Member"),
        avatar=data.get("avatar"),
        post_text=data.get("post_text"),
        post_image=data.get("post_image"),
        post_time=datetime.utcnow(),
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(
        {
            "id": post.id,
            "userId": post.user_id,
            "userName": post.user_name,
            "userRole": post.user_role,
            "avatar": post.avatar,
            "postText": post.post_text,
            "postImage": post.post_image,
            "postTime": post.post_time.isoformat(),
        }
    ), 201


# UPDATE post
@posts_bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404

    data = request.get_json()
    post.post_text = data.get("post_text", post.post_text)
    post.post_image = data.get("post_image", post.post_image)

    db.session.commit()
    return jsonify(
        {"id": post.id, "postText": post.post_text, "postImage": post.post_image}
    )


# DELETE post
@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Deleted"})
