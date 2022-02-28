# Flask Vue Study

Trying to use Flask and Vue to build a simple application and learn more on both technologies.


# Backend endpoints

**All messages follows the given pattern:**

    {
	    "success": True,
	    "message": "You managed to login \o/",
	    "data": {
		    ...
	    }
    }
**On this doc only whats inside `data` will be represented as a response.**

## Authentication

### [POST] auth/
Performs the login.
**Body:**

    {
	    "username": "teste",
	    "password": "teste"
    }

**Response:**

    {
		"_id": "ffffffffffffffffffffffff",
		"password": "...",
		"roles": [
			"default"
		],
		"token": "...",
		"username": "my_beautiful_username"
	}
	
### [DELETE] auth/
*Requires a Authorization header*
Performs the logout.

### [GET] auth/ 
*Admin only*
*Requires a Authorization header*
Its a `Who am I`
**Gives the same response as [POST] auth/**

### [POST] auth/register
Register a new user
**Body:**

    {
		"username": "test-user",
		"password": "test-password"
	}

## Photos

### [GET] photos/
*Requires a Authorization header*
Gets a list of approved photos.
**Response:**

	[
		{
			"_id": "ffffffffffffffffffffffff",
			"analysed_by": "ffffffffffffffffffffffff",
			"comment_count": 0,
			"comments": [],
			"created_at": "Mon, 28 Feb 2022 17:11:33 GMT",
			"deleted": false,
			"i_liked": true,
			"image_uri": ".......",
			"like_count": 1,
			"status": "accepted",
			"title": "Gonna be a unforgettable marriage",
			"uploaded_by": "ffffffffffffffffffffffff"
		},
		{
			"_id": "ffffffffffffffffffffffff",
			"analysed_by": "ffffffffffffffffffffffff",
			"comment_count": 1,
			"comments": [
				{
					"message": "pretty",
					"user_id": "ffffffffffffffffffffffff",
					"username": "test-commenter"
				}
			],
			"created_at": "Mon, 28 Feb 2022 17:09:36 GMT",
			"deleted": false,
			"i_liked": false,
			"image_uri": "....",
			"like_count": 2,
			"status": "accepted",
			"title": "Its An Awesome Picture",
			"uploaded_by": "ffffffffffffffffffffffff"
		}
	]
*Paging was implemented but for simplicity it was commented out*

### [POST] photos/
*Requires a Authorization header*
Submits a new photo to approval.
**Response:**

	{
		"title": "An Awesome Title",
		"file": {
			"data": "data:image/png;base64,iVBORw0KGgoAA...5CYII="
		}
	}

### [GET] photos/\<string:photo_id\>
*Requires a Authorization header*
Fetches a single photo.
**Response:**

		{
			"_id": "ffffffffffffffffffffffff",
			"analysed_by": "ffffffffffffffffffffffff",
			"comments": [
				{
					"message": "pretty",
					"user_id": "ffffffffffffffffffffffff",
					"username": "test-commenter"
				}
			],
			"created_at": "Mon, 28 Feb 2022 17:09:36 GMT",
			"deleted": false,
			"image_uri": "....",
			"status": "accepted",
			"title": "No one takes pictures better then i do",
			"uploaded_by": "ffffffffffffffffffffffff"
		}

### [GET] photos/pending
*Requires a Authorization header*
*Admin only*
Fetches all images pending approval
**Response:**
Actually its the same of **[GET] photos/**

### [POST] photos/pending/\<string:photo_id\>
*Requires a Authorization header*
*Admin only*
Sets a photo to `Approved` or `Denied`.
**Body:**

	{
		"status": "accepted" | "rejected"
	}


### [DELETE] photos/\<string:photo_id\>
*Requires a Authorization header*
*Not implemented*
Deletes a given photo.

### [POST] photos/\<string:photo_id\>/comment
*Requires a Authorization header*
Submits a comment to a photo.
**Body:**
	
	{
		"message": "Wow that's such a nice picture! Such a great event! 10/10, would go again."
	}

### [DELETE] photos/\<string:photo_id\>/comment/\<string:comment_id\>
*Requires a Authorization header*
*Not implemented*
Deletes a comment.

### [POST] photos/\<string:photo_id\>/react
*Requires a Authorization header*
Adds a reaction to a given photo, fixed on `like`'s for now.

### [DELETE] photos/\<string:photo_id\>/react
*Requires a Authorization header*
Removes a reaction, fixed on `like`'s for now.
