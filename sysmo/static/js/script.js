var search = window.location.href;
var search = search.split("/");
var dashboard = ["dashboard", "host"];

if (search[search.length - 2] == "group") {
  document.getElementById("nav-group").classList.add("active");
} else if (dashboard.includes(search[search.length - 2])) {
  document.getElementById("nav-dashboard").classList.add("active");
} else if (search[search.length - 2] == "policy") {
  document.getElementById("nav-policy").classList.add("active");
}

var json = document.querySelectorAll(".tojson");

for (index = 0; index < json.length; index++) {
  var json_list = "";
  f_json = JSON.parse(json[index].innerHTML.replace(/'/g, '"'));
  for (key in f_json) {
    json_list += "<tr><td>" + key + "\t:</td><td>" + f_json[key] + "<td></tr>";
  }
  json[index].innerHTML = "<td><table>" + json_list + "</td></table>";
  // console.log(json[index].innerHTML);
}

var disk_json = document.querySelectorAll(".diskjson");
for (index = 0; index < disk_json.length; index++) {
  disk_list = "<table><tbody><tr>";
  var format_diskjson =
    disk_json[index].innerHTML == "None"
      ? (disk_json.innerHTML = "None")
      : (format_diskjson = Object.entries(
          JSON.parse(disk_json[index].innerHTML.replace(/'/g, '"'))
        ));
  if (format_diskjson != "None") {
    for (d_index = 0; d_index < format_diskjson.length; d_index++) {
      format_disk = format_diskjson[d_index];
      disk_list +=
        "<td><table><tbody><tr><td>Mount\t:</td><td>" +
        format_disk[0] +
        "</td></tr>";
      for (
        x_index = 0;
        x_index < Object.entries(format_disk[1]).length;
        x_index++
      ) {
        format_policy = Object.entries(format_disk[1])[x_index];
        disk_list +=
          "<tr><td>" +
          format_policy[0] +
          "\t:</td><td>" +
          format_policy[1] +
          "</td></tr>";
      }
      disk_list += "</tbody></table></td>";
    }
    disk_json[index].innerHTML = disk_list + "</tr></tbody></table>";
  }
  // console.log(disk_json[index].innerHTML);
}

var group = document.querySelector(".grouplist");
