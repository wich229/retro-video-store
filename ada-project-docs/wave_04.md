# OPTIONAL Wave 4: Enhancements

These really are **optional** - if you've gotten here and you have time left, that means you're moving speedy fast!

## Enhancements

### More Query Parameters
| Name   | Value   | Description
|--------|---------|------------
| `sort` | string  | Sort objects by this field, in ascending order
| `n`    | integer | Number of responses to return per page
| `p`    | integer | Page of responses to return


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