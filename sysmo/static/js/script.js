var search = window.location.href;
var search = search.split("/");
var dashboard = ["dashboard", "host"];
console.log(search[search.length - 2]);

if (search[search.length - 2] == "group") {
  document.getElementById("nav-group").classList.add("active");
} else if (dashboard.includes(search[search.length - 2])) {
  document.getElementById("nav-dashboard").classList.add("active");
} else if (search[search.length - 2] == "policy") {
  document.getElementById("nav-policy").classList.add("active");
}
// const navlink = document.querySelector(".nav-link");

// navlink.addEventListener("click", function () {
//   navlink.classList.remove("active");
// });
