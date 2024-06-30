
# API Reference
Details of API usage: including request body (payload), request type, headers, etc


## Create Order
#### Request Type
```http
POST /orders
```

#### Request Body
```javascript
{
  "order": [
    {
      "product": "sandwich",
      "size": "big",
      "quantity": 1
    }
  ]
}
```

#### Response
```javascript
{
  "order": [
    {
      "product": "sandwich",
      "size": "big",
      "quantity": 1
    }
  ]
}
```

## Get all orders
#### Request Type
```http
GET /orders
```
#### Response
```javascript
{
    "orders": [
        {
            "order": [
                {
                    "product": "coffee",
                    "size": "small",
                    "quantity": 2
                },
                {
                    "product": "iced tea",
                    "size": "small",
                    "quantity": 1
                }
            ],
            "id": "0f401a96-9353-44dc-956d-c1e9d19aeda6",
            "created": "2024-06-30T05:49:35.325609",
            "status": "created"
        },
        {
            "order": [
                {
                    "product": "sandwich",
                    "size": "big",
                    "quantity": 1
                }
            ],
            "id": "8c907951-11a9-4139-9e03-78b1f022f54b",
            "created": "2024-06-30T05:54:13.206774",
            "status": "progress"
        }
    ]
}
```


## Get one particular order details
#### Request Type
```http
  GET /orders/{order_id}
```
#### Response
```javascript
{
    "order": [
        {
            "product": "sandwich",
            "size": "big",
            "quantity": 1
        }
    ],
    "id": "8c907951-11a9-4139-9e03-78b1f022f54b",
    "created": "2024-06-30T05:54:13.206774",
    "status": "progress"
}
```

## Pay for an order
#### Request Type 
```http
  POST /orders/{order_id}/pay
```

#### Response
```javascript
{
    "order": [
        {
            "product": "sandwich",
            "size": "big",
            "quantity": 1
        }
    ],
    "id": "8c907951-11a9-4139-9e03-78b1f022f54b",
    "created": "2024-06-30T05:54:13.206774",
    "status": "progress"
}
```


## Cancel an order
#### Request Type 
```http
  POST /orders/{order_id}/cancel
```

#### Response
```javascript
{
    "order": [
        {
            "product": "sandwich",
            "size": "big",
            "quantity": 1
        }
    ],
    "id": "8c907951-11a9-4139-9e03-78b1f022f54b",
    "created": "2024-06-30T05:54:13.206774",
    "status": "cancelled"
}
```

## Delete an order
#### Request Type 
```http
  DELETE /orders/{order_id}
```


## Update an order
#### Request Type 
```http
  PUT /orders/{order_id}
```
#### Request
```javascript
{
  "order": [
    {
      "product": "croissant",
      "size": "small",
      "quantity": 1
    }
  ]
}
```
#### Response
```javascript
{
    "order": [
        {
            "product": "croissant",
            "size": "small",
            "quantity": 1
        }
    ],
    "id": "0ffda170-3c0c-4b98-9364-15c1d4f9f35b",
    "created": "2024-06-30T06:56:14.415320",
    "status": "created"
}
```



