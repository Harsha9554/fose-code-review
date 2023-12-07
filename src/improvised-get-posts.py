def get_posts(user_id=None):
    """
    Retrieves all posts from the Post collection in MongoDB and returns them in JSON format.

    :param user_id: (optional) The ObjectId of the user to filter posts by.
    :return: A list of posts.
    """

    query = {"user_id": ObjectId(user_id)} if user_id else {}
    posts_cursor = mongo.db.Post.find(query)
    posts_list = [post for post in posts_cursor]

    # Get all unique user IDs from comments
    user_ids = {
        ObjectId(comment[0]) for post in posts_list for comment in post["comments"]
    }
    # Retrieve all users at once and store them in a dictionary
    users = {
        str(user["_id"]): user["username"]
        for user in mongo.db.User.find({"_id": {"$in": list(user_ids)}})
    }

    for post in posts_list:
        post["_id"] = str(post["_id"])
        post["user"] = str(post["user"])
        post["user_id"] = str(post["user_id"])
        for comment in post["comments"]:
            comment[0] = str(comment[0])
            comment.append(users[comment[0]])

    return posts_list
