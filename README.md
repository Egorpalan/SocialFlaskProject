# SocialNetworkAPI

A project implementing an API for a social network platform for text posts. Functions provided by the API

+ Creates a user (checks the mail for correctness) who can write posts, put reactions (heart, like, dislike, boom, ...) to posts of other users
+ Provides data for a specific user
+ Creates a post
+ Provides data for a specific post
+ The user puts a reaction to the post
+ Displays all user posts sorted by the number of reactions
+ Generates a list of users sorted by the number of reactions
+ Generates a graph of users by the number of reactions

# Requests and Responses

- Creating a user `POST /users/create

Request example:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
}
```

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number"
  "posts": []
}
```


- Getting data for a specific user `GET /users/<user_id>`

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number",
  "posts": [
    "number",
    ...
  ]
}
```


- Creating a post `POST /posts/create`

Request example:
```json
{
  "author_id": "number",
  "text": "string",
}
```

Response example:
```json
{
  "id": "number",
  "author_id": "number",
  "text": "string",
  "reactions": [
  	"string",
    ...
  ] 
}
```


- Getting data for a specific post `GET /posts/<post_id>`

Response example:
```json
{
  "id": "number",
  "author_id": "number",
  "text": "string",
  "reactions": [
  	"string",
    ...
  ] 
}
```


- Put a reaction to the post `POST /posts/<post_id>/reaction`

Request example:
```json
{
  "user_id": "number",
  "reaction": "string"
}
```

Response example: (empty, only the response code)


- Getting all user posts sorted by the number of reactions `GET/users/<user_id>/posts`

The value `asc` stands for `ascending' (ascending), the parameter `desc` stands for `descending' (descending)

Request example:
```json
{
  "sort": "asc/desc"
}
```

Response example:
```json
{
	"posts": [
    	{
  			"id": "number",
  			"author_id": "string",
  			"text": "string",
  			"reactions": [
  				"string",
    			...
  			] 
  		},
        {
        	...
        }
    ]
}
```


- Getting all users sorted by the number of reactions `GET/users/leaderboard`

The value `asc` stands for `ascending' (ascending), the parameter `desc` stands for `descending' (descending)

Request example:
```json
{
  "type": "list",
  "sort": "asc/desc"
}
```

Response example:
```json
{
	"users": [
    	{
          "id": "number",
          "first_name": "string",
          "last_name": "string",
          "email": "string",
          "total_reactions": "number"
		},
        {
        	...
        }
    ]
}
```


- Getting a graph of users by the number of reactions `GET /users/leaderboard`

Request example:
```json
{
  "type": "graph",
}
```

Response example:
```html
<img src="path_to_graph">
```