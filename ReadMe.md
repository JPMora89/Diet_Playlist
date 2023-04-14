
# Diet Playlist

The application allows users to create different diets based on their dietary needs. The user is able to add food to specific diets from thousands of options and able to retrieve nutritional information for each item. The user is able to keep track of their favorite foods and insert them into different diets based on their needs.

## Userflow

The user creates an account using Name & Email. They then have the option to read more into the different types of Diets available, from there they create their very own diet. The user can then look up from thousands of options certain foods which would fit that specific diet. The user will then have access to all their chosen foods in specific diets to be able to keep track of their dietary needs. 

## Technologies

HTML, CSS, JavaScript, Python, Flask, PostgreSQL, & Bootstrap 

## Server Routes Table

| Method | Route                                    | Description                           |
|--------|------------------------------------------|---------------------------------------|
| GET    | '/search_food'                           | Retrieves the food queried by user    |
| POST   | '/search_food'                           | Adds chosen food to specific diet     |
| POST   | '/create_diets'                          | Allows user to create a new diet      |
| GET    | '/diets'                                 | Shows all user created diets          |
| PUT    | '/diets/update/<int:id>'                 | Updates diet with user selected foods |
| DELETE | '/diets/delete/<int:id>'                 | Deletes selected diet                 |
| GET    | '/diets/<int:id>'                        | Shows a specific diet and its content |
| DELETE | '/diets/<int:id>/foods/<string:food_id>' | Deletes specific foods from a diet    |
|        |                                          |                                       |

## API

The application utilizes https://www.edamam.com. The Food Database API allows you to search for nutrition and diet information within their Food Database.

## Models

The database models includes one for the User, the Foods available, the user-created Diets as well as Food_in_Diet which shows all of the foods a user has inserted into specific diets. 

## Images


## Project Link


## Team members
Pablo Mora
Raymond Maroun



## License

[MIT](https://choosealicense.com/licenses/mit/)