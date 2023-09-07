// User diets delete




const table = document.querySelector("table");

table.addEventListener("click", (event) => {
  if (event.target.classList.contains("button-danger")) {
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





// window

    document.querySelectorAll('.tableRow').forEach(item => {
      item.addEventListener('submit', (event) => {
        event.preventDefault();
        const diet_value = document.getElementById('diet_options').value;
        tr = event.target.closest("tr");
        console.log(tr.dataset);
        axios.put(`/diets/update/${diet_value}`, tr.dataset).then((response) => {
          console.log(response.data)
          window.location = `/diets/${diet_value}`
          console.log("Food added in diet!");
        });
      })
    })



const deleteFood = (dietId, foodId) => {
  axios
    .delete(`/diets/${dietId}/foods/${foodId}`)
    .then((response) => {
      console.log(response);
      window.location.reload();
    })
    .catch((error) => {
      console.log(error);
    });
};

const deleteButtons = document.querySelectorAll(".deletefoodbutton");
deleteButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const dietId = window.location.href.split("/").pop();
    const foodId = button.closest(".userfoodstablerow").dataset.id;
    deleteFood(dietId, foodId);
  });
});