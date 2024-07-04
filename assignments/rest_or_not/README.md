# REST or NOT

Got through the API description and answer if the API described is a REST API or not. Also provide the reasoning behind the same
### Q1

```bash
The API uses HTTP methods such as GET, POST, PUT, and DELETE to perform CRUD (Create, Read, Update, Delete) operations
```

### Q2

```bash
The API requires a custom header for all operations, which specifies the type of operation (create, read, update, delete) to be performed.
```


### Q3

```bash
The API endpoints are designed as resources, for example, /users, /orders, /products.
```


### Q4

```bash
The API maintains the client’s session state on the server and relies on this state to process requests
```


### Q5

```bash
The API uses URIs to identify resources and query parameters to filter and sort these resources, for example, /users?age=30&sort=name.
```


### Q6

```bash
The API responses include hypermedia links to facilitate navigation to related resources.
```


### Q7

```bash
The API can only be accessed using a proprietary client application and network protocols and not through standard web browsers or HTTP clients.
```


### Q8

```bash
The API responses are typically in JSON or XML format.
```


### Q9

```bash
The API allows for creating completely new resource which did not exist earlier by making a PUT request to the resource’s URI.
```
