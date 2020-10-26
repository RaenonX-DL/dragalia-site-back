# `/user/login`

## Description

Request will be sent here upon user login.

The backend will the use the sent data to log the login.

If the user has not been registered to the database yet, register it.

## Method

`POST`

## Arguments

Parameter Name | Name | Required/Optional | Description
:---: | :---: | :---: | :---:
`google_uid` | Google UID | Required | UID of the logged in Google user.
`google_email` | Google Email | Required | Email of the logged in Google user.

## Response

Parameter Name | Name | Type | Description
:---: | :---: | :---: | :---:
`code` | Response code | `int` | Check [this](/doc/response_code.md) for more details.
`success` | Success | `bool` | If the response is successful.
`isAdmin` | Is Admin | `bool` | If the user is site admin.
`posts` | Posts | `Posts` | List of posts with truncated information.

### `Posts`

Parameter Name | Name | Type | Description
:---: | :---: | :---: | :---:
`title` | Post title | `string` | Title of the post.
`seq_id` | Sequential ID | `int` | Sequential ID of the post.
`modified` | Last Modified | `datetime` | Last modified timestamp.
`published` | Published | `datetime` | Published timestamp.
