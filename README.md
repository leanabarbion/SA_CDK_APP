Add function API
POST:[url]/prod/items
body:{
"id": "4728",
"name": "Deck_2",
"course": "OS",
"year": "2021"
}

Delete function API by ID
Give ID
DELETE: [url]/prod/items/{id}

Get item by ID
Give ID
GET: [url]/prod/items/{id}

Get all items
GET: [url]/prod/items

Get item by course
Give course
GET: [url]/prod/items/course/{course}

Get items by year
Give year
GET: [url]/prod/items/year/{year}
