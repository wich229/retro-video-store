# Wave 3: Enhancements & Deployment

### Query Parameters
All customer endpoints which return a list should accept 3 _optional_ query parameters:

| Name   | Value   | Description
|--------|---------|------------
| `sort` | string  | Sort objects by this field, in ascending order
| `n`    | integer | Number of responses to return per page
| `p`    | integer | Page of responses to return

So, for an API endpoint like `GET /customers`, the following requests should be valid:
- `GET /customers`: All customers, sorted by ID
- `GET /customers?sort=name`: All customers, sorted by name
- `GET /customers?n=10&p=2`: Customers 11-20, sorted by ID
- `GET /customers?sort=name&n=10&p=2`: Customers 11-20, sorted by name

Things to note:
- Possible sort fields:
  - Customers can be sorted by `name`, `registered_at` and `postal_code`
- If the client requests both sorting and pagination, pagination should be relative to the sorted order
- Check out the [paginate method](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate)

### Extra Endpoint: Inventory Management
This endpoint should support all 3 query parameters. All fields are sortable.

#### `GET /customers/<id>/history`
List the videos a customer has checked out _in the past_

URI parameters:
- `id`: Customer ID

Fields to return:
- `title`
- `checkout_date`
- `due_date`

## Deployment

Deploy this project to Heroku.

Then, add some Customer, Video, and Rental records to the production database.

Be sure to grab the URL of your deployed app. It will be submitted at the time of project submission.

### Tips
- When unexpected issues come up, employ all of your debugging skills:
  - Write down what step/command created teh issue
  - Write down how you observe the issue
  - Attempt to recreate the issue locally
  - Use Postman, the browser, and the debugger tools
  - Use the Heroku logs
  - Research error messages
  - Rubber duck and ask for help 


