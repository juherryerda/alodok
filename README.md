# alodok

List of API

- POST /tokens

Authorization: Basic Auth

Description:
Get session token for further access, valid for 100 sec

Response: application/json

-------------------------------------------------------------------------

- GET /api/v1/cart/detail/<userid>

Authorization: Bearer Token

Description:
Get cart information from user

Response: application/json

-------------------------------------------------------------------------

- POST /api/v1/cart/checkout

Authorization: Bearer Token

Description:
Submit checkout process

Request Body: application/json
Request Body Format: {"user_id":""}

Response: application/json
-------------------------------------------------------------------------

- POST /api/v1/add_to_cart
Authorization: Bearer Token

Description:
Insert cart Data

Request Body: application/json
Request Body Format: {"user_id":"","product_id",""}

Response: application/json
-------------------------------------------------------------------------

- GET /api/v1/detail/<id>

Description:
Get detail product

Response: application/json
-------------------------------------------------------------------------

- GET /api/v1/lists

Description:
List all product

Response: application/json
