# OPTIONAL Wave 4: Enhancements

These really are **optional** - if you've gotten here and you have time left, that means you're moving speedy fast!

## Enhancements

### More Query Parameters
The following 3 _optional_ query parameters:

| Name          | Value   | Description
|---------------|---------|------------
| `sort`        | string  | Sort objects by this field, in ascending order
| `count`       | integer | Number of responses to return per page
| `page_num`    | integer | Page of responses to return

should additionally be accepted by the following three endpoints:
- `GET /video`
- `GET /customers/<id>/history`
- `GET /videos/<id>/history`

So, for an API endpoint like `GET /videos`, the following requests should be valid:
- `GET /videos`: All videos, sorted by ID
- `GET /videos?sort=name`: All customers, sorted by name
- `GET /videos?count=10&page_num=2`: Customers 11-20, sorted by ID
- `GET /videos?sort=name&count=10&page_num=2`: Customers 11-20, sorted by name

Add your own Wave 04 tests to verify functionality.

### More Inventory Management
All these endpoints should support all 3 query parameters. All fields are sortable.

#### `GET /rentals/overdue`
List all customers with overdue videos

Fields to return:
- `video_id`
- `title`
- `customer_id`
- `name`
- `postal_code`
- `checkout_date`
- `due_date`


## CLI

Create a Command Line Interface (CLI) program as a client for the Retro Video Store API.