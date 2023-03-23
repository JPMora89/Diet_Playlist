


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
=   console.log(tr.dataset)
    console.log(apiId)
    console.log(userId)
    console.log(diet_value)
    // console.log(getFoodData)
    // const formData = new FormData('user_diets')
    console.log(diet_value)
    axios
    .put(`/diets/update/${diet_value}`, tr.dataset)
    .then(response) 
    console.log([diet_value])
  
    // .then((response) => {
    //   console.log(response.data)
    //   console.log(response.status)
    //     console.log("success adding food to diet");
    })
  

  
 function getDiet_id() {
  const diet_value = document.getElementById('diet_options').value;
  console.log(diet_value);
  axios.put(`/diets/${diet_value}`, diet_value)
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.log(error);
  });
 } 






// const foodTable = document.querySelector("table");

// foodTable.addEventListener("click", (event) => {

//   if (event.target.classList.contains("tableRow")) {
//   const id = event.target.dataset.id;
//   const diet_value = document.getElementById('diet_options').value;
//   const tr = event.target.closest("tr")
//   const apiId = event.target.dataset.apiId;
//   const userId = event.target.dataset.userId;
//   console.log(apiId)
//   console.log(userId)
//   console.log(tr.dataset)
//   axios
//   .put(`/diets/update/${diet_value}`, tr.dataset)
//   .then((response) => {
//       console.log("Data added successfully!");

//     })
//     .catch((error) => {
//       console.error(error);
//       alert("Error updating data.");
//     });
// }
// });





// const diet_value = document.getElementById('diet_options').value;
// axios.get(`/diets/${diet_value}`)

// const getformData = document.getElementById('user_diets');

// getformData.addEventListener("submit", (event) => {
//     event.preventDefault();
//     const diet_value = document.getElementById('diet_options').value;
//     const getFoodData = document.getElementById('foodItem').getAttribute('value')
//     const tr = event.target.closest("tr")
//     const apiId = event.target.dataset.apiId;
//     const userId = event.target.dataset.userId;
//     console.log(tr.id)
//     console.log(tr.dataset.name)
//     console.log(tr.dataset.image)
//     console.log(tr.dataset)
//     console.log(apiId)
//     console.log(userId)
//     // console.log(getFoodData)
//     // const formData = new FormData('user_diets')
//     console.log(diet_value)
//     axios.all([
//     axios.put(`/diets/update/${diet_value}`, tr.dataset),
//     axios.put(`/diets/${diet_value}`, diet_value)


//     ])
    
//     .then(responseArr => {


//       console.log(responseArr[0])
//       console.log(responseArr[1])
//       console.log([diet_value])
//     }) 
    
//     // axios.post(`/diets/${diet_value}`, 
//     // )
//     // .then((response) => {
//     //     console.log("success adding food to diet");
//     // })
//     // .catch((error) => {
//     //     console.error(error);
//     //     alert("Error deleting data.");
//     //   });
// })