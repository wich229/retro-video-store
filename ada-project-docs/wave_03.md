# Wave 3: Enhancements & Deployment

## Query Parameters
The following 3 _optional_ query parameters:

| Name          | Value   | Description
|---------------|---------|------------
| `sort`        | string  | Sort objects by this field, in ascending order
| `per_page`    | integer | Number of responses to return per page
| `page`        | integer | Page of responses to return

should be accepted by the following three endpoints:
- `GET /customers`
- `GET /customers/<id>/rentals`
- `GET /videos/<id>/rentals`

So, for an API endpoint like `GET /customers`, the following requests should be valid:
- `GET /customers`: All customers, sorted by ID
- `GET /customers?sort=name`: All customers, sorted by name
- `GET /customers?per_page=10&page=2`: Customers 11-20, sorted by ID
- `GET /customers?sort=name&per_page=10&page=2`: Customers 11-20, sorted by name

Things to note:
- Possible sort fields:
  - Customers can be sorted by `name`, `registered_at` and `postal_code`
  - Videos can be sorted by `title` and `release_date`
- If the client requests both sorting and pagination, pagination should be relative to the sorted order
- Check out the [paginate method](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate)


#### Errors and Edge Cases to Check

- The API should default to sorting by `id` if no `sort` parameter is specified
- The API should default to sorting by `id` if a value other than `name`, `registered_at`, or `postal_code` is passed in for the parameter `sort`
- The API should default to returning all customers in a single page if no number of per page responses is specified
- The API should default to returning all customers in a single page if an invalid number of per page responses is specified
- The API should default to returning the first page if no page is specified
- The API should default to returning the first page if an invalid page is specified

## Extra Endpoint: Inventory Management
This endpoint should support all 3 query parameters. All fields are sortable.

### `GET /customers/<id>/history`
List the videos a customer has checked out _in the past_. Current rentals should not be included.                                                                                  

URI parameters:
- `id`: Customer ID

Fields to return:
- `title`
- `checkout_date`
- `due_date`

#### Errors and Edge Cases to Check
- The API should return back detailed errors and a status `404: Not Found` if the customer does not exist
- The API should return an empty list if the customer has no rental history

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


