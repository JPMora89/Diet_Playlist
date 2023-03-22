


// create logic for submission
// const diet_value $(this).data(value)

// const table = documents.querySelector("table");

// table.addEventListener("click", (event) => {
//     if (event.target.classList.contains("delete-button")) {
//         const id = event.target.dataset.id;
//         axios
//             .delete('/diets/delete/${id}')
//             .then((response) => {
//                 console.log("Data deleted successfully!");
//                 const tr = event.target.closest("tr");
//                 tr.parentNode.removeChild(tr);
//             })
//             .catch((error) => {
//                 alert("Error deleting data");
//             });
//     }
// });



const table = document.querySelector("table");

table.addEventListener("click", (event) => {
  if (event.target.classList.contains("delete-button")) {
    const id = event.target.dataset.id;
    axios
      .delete(`/diets/delete/${id}`)
      .then((response) => {
        console.log("Data deleted successfully!");
        const tr = event.target.closest("tr");
        tr.parentNode.removeChild(tr);
      })
      .catch((error) => {
        console.error(error);
        alert("Error deleting data.");
      });
  }
});

const getformData = document.getElementById('user_diets');

getformData.addEventListener("submit", (event) => {
    event.preventDefault();
    const diet_value = document.getElementById('diet_options').value;
    const getFoodData = document.getElementById('foodItem').getAttribute('value')
    const tr = event.target.closest("tr")
    const apiId = event.target.dataset.apiId;
    const userId = event.target.dataset.userId;
    console.log(tr.id)
    console.log(tr.dataset.name)
    console.log(tr.dataset.image)
    console.log(tr.dataset)
    console.log(apiId)
    console.log(userId)
    // console.log(getFoodData)
    // const formData = new FormData('user_diets')
    console.log(diet_value)
    axios
    .put(`/diets/update/${diet_value}`)
    .then(response) 
    console.log([diet_value])
    // axios.post(`/diets/${diet_value}`, 
    // )
    // .then((response) => {
    //     console.log("success adding food to diet");
    // })
    // .catch((error) => {
    //     console.error(error);
    //     alert("Error deleting data.");
    //   });
})

