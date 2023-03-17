let diet_selection_form = document.querySelector('#user_diets')

diet_selection_form.addEventListener('submit', function(e) {
    e.preventDefault();
    user_selection = document.getElementById('user_diets').value
    const apiId = e.target.dataset.apiId;
    const userId = e.target.dataset.userId;
})

// var deleteButton = document.getElementById('delete-button');
// deleteButton.addEventListener('click', function() {
//     var itemId = deleteButton.getAttribute('data-id');
//     var xhr = new XMLHttpRequest();
//     xhr.open('DELETE', '/diets/delete/' + itemId);
//     xhr.onload = function() {
//         if (xhr.status === 200) {
//             // Handle success
//             return "successful deletion"
//         } else {
//             // Handle error
//             return "Oops "
//         }
//     };
//     xhr.send();
// });

// Get all the delete buttons on the page
// var deleteButtons = document.querySelectorAll('.delete-btn');

// // Loop through each button and add an event listener to handle the click
// deleteButtons.forEach(function(button) {
//     button.addEventListener('click', function() {
//         // Get the ID of the diet to delete from the data-id attribute on the button
//         var dietId = button.getAttribute('data-id');

//         // Send an AJAX request to the server to delete the diet
//         var xhr = new XMLHttpRequest();
//         xhr.open('DELETE', '/diets/delete/' + dietId);
//         xhr.onload = function() {
//             if (xhr.status === 200) {
//                 // If the deletion was successful, remove the diet from the page
//                 button.parentNode.parentNode.removeChild(button.parentNode);
//             } else {
//                 // If there was an error, display an error message
//                 alert('There was a problem deleting the diet.');
//             }
//         };
//         xhr.send();
//     });
// });

// Get all the delete buttons on the page

// var deleteButton = document.getElementById('delete-button');

// // Loop through each button and add an event listener to handle the click
// deleteButton.forEach(function(button) {
//     button.addEventListener('click', function() {
//         // Get the ID of the diet to delete from the data-id attribute on the button
//         var dietId = button.getAttribute('data-id');

//         // Send an AJAX request to the server to delete the diet
//         var xhr = new XMLHttpRequest();
//         xhr.open('DELETE', '/diets/delete/' + dietId);
//         xhr.onload = function() {
//             if (xhr.status === 200) {
//                 // If the deletion was successful, remove the diet from the page
//                 var dietRow = button.parentNode.parentNode;
//                 dietRow.parentNode.removeChild(dietRow);
//             } else {
//                 // If there was an error, display an error message
//                 alert('There was a problem deleting the diet.');
//             }
//         };
//         xhr.send();
//     });
// });

// $(document).ready(function() {
//     $('.delete-button').click(function() {
//         const dietId = $(this).data('id');
//         $.ajax({
//             url: '/diets/delete/' + dietId,
//             type: 'DELETE',
//             headers: {
//                 // include the CSRF token in the headers
//                 'X-CSRF-TOKEN': csrfToken,
//             success: function() {
//                 window.location.reload();
//             },
//             error: function() {
//                 alert('There was a problem deleting the diet.');
//             }
//         });
//     });
// });

$(document).ready(function() {
    $('.delete-button').click(function() {
        const dietId = $(this).data('id');
        $.ajax({
            url: '/diets/delete/' + dietId,
            type: 'DELETE',
            headers: {
                // include the CSRF token in the headers
                'X-CSRF-TOKEN': csrfToken,
            },
            success: function() {
                window.location.reload();
            },
            error: function() {
                alert('There was a problem deleting the diet.');
            }
        });
    });
});
