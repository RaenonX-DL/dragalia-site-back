# `/posts/quest`

## Description

Get the quest post list.

This only returns

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
