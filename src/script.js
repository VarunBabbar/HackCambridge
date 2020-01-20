var locationslist = ["Sydney2", "Sydney1", "Sydney2"];
var locations = [
  "-33.8479255,150.651098",
  "-33.8569,151.2152",
  "-33.8479255,150.651098"
];
var modes = ["driving", "bicycling", "walking", "transit"];
var efficiency = [
  ["score1", "score2", "score3", "score4"],
  ["score1", "score2", "score3", "score4"]
];
var length = [
  ["time1", "time2", "time3", "time4"],
  ["time1", "time2", "time3", "time4"]
];
function mapGenerate(index, mode) {
  var link =
    "https://www.google.com/maps/embed/v1/directions?key=AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo";
  var origin = locations[index];
  var destination = locations[parseInt(index) + 1];
  var modenew = mode;
  var el = document.getElementById("frame" + index.toString());
  el.setAttribute(
    "src",
    link +
      "&origin=" +
      origin +
      "&destination=" +
      destination +
      "&mode=" +
      modenew
  );
  var el2 = document.getElementById("div" + index.toString());
  el2.innerHTML =
    "<br></br>" +
    "Length is : " +
    length[index][modes.indexOf(mode)] +
    "<br></br>" +
    "With efficiency score " +
    efficiency[index][modes.indexOf(mode)];
}
function tableCreate() {
  var body = document.getElementsByTagName("body")[0];
  var tbl = document.createElement("table");
  tbl.style.width = "100%";
  tbl.setAttribute("border", "1");
  var tbdy = document.createElement("tbody");
  for (var i = 0; i < locations.length - 1; i++) {
    var tr = document.createElement("tr");
    for (var j = 0; j < 3; j++) {
      var td = document.createElement("td");
      td.appendChild(document.createTextNode("\u0020"));
      tr.appendChild(td);
      if (j == 0) {
        td.innerHTML =
          "Journey from " + locationslist[i] + " to " + locationslist[i + 1];
      }
      if (j == 1) {
        var list = document.createElement("select");
        list.setAttribute("id", "list" + i.toString());
        list.setAttribute("index", i);
        list.addEventListener("change", function() {
          mapGenerate(this.getAttribute("index"), this.value);
        });
        //list.setAttribute("onchange","mapGenerate(this.index, this.value)")
        for (var k = 0; k < modes.length; k++) {
          var item = document.createElement("option");
          item.setAttribute("value", modes[k]);
          item.innerHTML = modes[k]; //+" - " +length[i][k]+""+efficiency[i][k];
          //item.appendChild(document.createTextNode(modes[k]+" - " +length[i][k]+efficiency[i][k]));
          list.appendChild(item);
        }
        td.appendChild(list);
        var div = document.createElement("div");
        div.setAttribute("id", "div" + i);
        div.innerHTML =
          "<br></br>" +
          "Length is : " +
          length[i][modes.indexOf(list.value)] +
          "<br></br>" +
          "With efficiency score " +
          efficiency[i][modes.indexOf(list.value)];
        td.appendChild(div);
      }
      if (j == 2) {
        var link =
          "https://www.google.com/maps/embed/v1/directions?key=AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo";
        var origin = locations[i];
        var destination = locations[i + 1];
        var mode = modes[0];
        var iframe = document.createElement("iframe");
        iframe.setAttribute("id", "frame" + i.toString());
        iframe.setAttribute(
          "src",
          link +
            "&origin=" +
            origin +
            "&destination=" +
            destination +
            "&mode=" +
            mode
        );
        iframe.width = "500px";
        iframe.height = "250px";
        td.appendChild(iframe);
      }
    }
    tbdy.appendChild(tr);
  }
  tbl.appendChild(tbdy);
  body.appendChild(tbl);
}
