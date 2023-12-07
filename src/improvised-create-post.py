@staticmethod
def create_post(post_data):
    """
    Creates a new post in the Post collection in MongoDB with the provided post data.

    :param post_data: A dictionary containing the data for the new post.
    :return: A Flask response object with a JSON payload indicating success and the ID of the created post.
    """
    # Validate post_data before using it
    if not post_model.Post.is_valid(post_data):
        return jsonify({"message": "Invalid post data!"}), 400

    try:
        new_post = post_model.Post(**post_data)
        post_id = new_post.save()
        return (
            jsonify({"message": "Post created successfully!", "post_id": str(post_id)}),
            201,
        )
    except Exception as e:
        return jsonify({"message": "Failed to create post: " + str(e)}), 500
