
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
![image](https://user-images.githubusercontent.com/110551396/231226248-f48937cb-086e-4316-9486-ae3a93d7d4ed.png)
![image](https://user-images.githubusercontent.com/110551396/231226436-30eda211-29f7-4e29-b74c-03693e5c7541.png)

![image](https://user-images.githubusercontent.com/110551396/231226145-1dc4f6c9-b15e-4254-b26e-41c99aeda167.png)
![image](https://user-images.githubusercontent.com/110551396/231226490-0558a914-20ed-4e57-900b-3f3390b29a4d.png)


![image](https://user-images.githubusercontent.com/110551396/231225910-c1c6b667-66a1-4ae7-8780-44a5f2a7d9f1.png)


## Project Link

https://diet-playlist.herokuapp.com/

## Team members
Pablo Mora
Raymond Maroun



## License

[MIT](https://choosealicense.com/licenses/mit/)
