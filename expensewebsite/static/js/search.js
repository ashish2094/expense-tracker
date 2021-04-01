const searchField = document.querySelector("#searchField");
const table_output = document.querySelector(".table-output");
const pagination = document.querySelector(".pagination-container");
const app_table = document.querySelector(".app-table");
const table_body = document.querySelector(".search-table-body");
table_output.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  if (searchValue.trim().length > 0) {
    console.log("searchValue ", searchValue);
    table_body.innerHTML = "";
    fetch("/expenses/search-expense/", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    }).then((res) =>
      res.json().then((data) => {
        console.log(("data", data));
        table_output.style.display = "block";
        pagination.style.display = "none";
        app_table.style.display = "none";
        if (data.length === 0) {
          table_output.innerHTML = `<p style="color : red;">No Result Found</p>`;
        } else {
          i = 1;
          data.forEach((item) => {
            table_body.innerHTML += `
            <tr scope="row">
            <td>${i}</td>
            <td>${item.date}</td>
            <td>${item.category}</td>
            <td>${item.amount}</td>
            <td>${item.description}</td>
            </tr>`;
            i++;
          });
        }
      })
    );
  } else {
    pagination.style.display = "block";
    app_table.style.display = "block";
    table_output.style.display = "none";
  }
});
