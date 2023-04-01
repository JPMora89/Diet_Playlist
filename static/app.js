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



// User deletes foods from specific diet

// const userfoodtable = document.getElementById("displaydietstable");

// userfoodtable.addEventListener("click", (event) => {
//   if (event.target.classList.contains("deletefoodbutton")) {
//     const tr = event.target.closest("tr");
//     tr.parentNode.removeChild(tr);
//   }
// });


// const getformData = document.getElementById('user_diets');

// getformData.addEventListener("submit", (event) => {
//     event.preventDefault();
//     const diet_value = document.getElementById('diet_options').value;
//     const getFoodData = document.getElementById('foodItem').getAttribute('value');
//     const tr = event.target.closest("tr");

//     // add a foreach method for this tr? 
//     const apiId = event.target.dataset.apiId;
//     const userId = event.target.dataset.userId;
//     console.log(tr.id);
//     console.log(tr.dataset);
//     console.log(apiId);
//     console.log(userId);
//     console.log(diet_value);
//     // console.log(getFoodData)
//     // const formData = new FormData('user_diets')
//     console.log(diet_value)
//     // axios
//     // .put(`/diets/update/${diet_value}`, tr.dataset)
//     // .then(response) 
//     // console.log([diet_value])
//     axios.put(`/diets/update/${diet_value}`, tr.dataset).then((response) => {
//       console.log("Food added in diet!");
//     });
//     console.log([diet_value]);
  
//     // .then((response) => {
//     //   console.log(response.data)
//     //   console.log(response.status)
//     //     console.log("success adding food to diet");
//     })
  

  
//  function getDiet_id() {
//   const diet_value = document.getElementById('diet_options').value;
//   console.log(diet_value);
//   axios.put(`/diets/${diet_value}`, diet_value)
//   .then(response => {
//     console.log(response.data);
//   })
//   .catch(error => {
//     console.log(error);
//   });
//  } 





    document.querySelectorAll('.tableRow').forEach(item => {
      item.addEventListener('submit', (event) => {
        event.preventDefault();
        const diet_value = document.getElementById('diet_options').value;
        tr = event.target.closest("tr");
        console.log(tr.dataset);
        axios.put(`/diets/update/${diet_value}`, tr.dataset).then((response) => {
          console.log("Food added in diet!");
        });
      })
    })



// const form = document.querySelector("user_diets");

// form.addEventListener("click", (event) => {
//   if (event.target.classList.contains("submitbutton")) {
//     const id = event.target.dataset.id;
//     const diet_value = document.getElementById('diet_options').value;
//     axios
//       .get(`/search_food`, diet_value)
//       .then((response) => {
//         console.log('diet value sent successfully')
//       })
//       .catch((error) => {
//         console.error(error);
//         alert("Error deleting data.");
//       });
//   }
// });

const $ = document;
let container = $.getElementsByClassName("cont")[0];

const random = (min, max) => Math.floor(Math.random() * max + min);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let drops = [];

const snow = () => {
  let w = random(1, 15),
    op = Math.random(),
    lef = random(0, 100),
    del = random(0, 15);
  sec = random(5, 15);
  let drop = `<div style="position: absolute; width: ${w}px; height: ${w}px; opacity: ${op}; top: -2rem; left: ${lef}rem;animation: snow ${sec}s ${del}s linear; border-radius: 50%;z-index: 1000;filter: drop-shadow(0 0 10px white);background-color: #fff"></div>`;

  drops.push(drop);
};

const main = async () => {
  while (true) {
    for (let i = 0; i < random(50, 100); i++) snow();
    for (let i = 0; i < drops.length; i++) container.innerHTML += drops[i];
    await sleep(30000);
    container.innerHTML = "";
  }
};

main();
