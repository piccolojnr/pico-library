$("#search-bar").bind("submit", function (e) {
  e.preventDefault();
  var q = e.currentTarget.getElementsByTagName("input")[0].value;
  if (q != "") {
    url = new URL(window.location);
    var search_params = url.searchParams;
    search_params.set("q", q);
    search_params.set("page", 1);
    url.search = search_params.toString();
    var new_url = url.toString();
    window.location = url;
  }
});

lan = $("#language-selected-code").val();
$(`#language-select option[value='${lan}']`).attr("selected", "selected");

$("#language-select").bind("change", function () {
  // bind change event to select
  var lan_ = $(this).val(); // get selected value

  if (lan_ != "") {
    // require a URL
    url = new URL(window.location);
    var search_params = url.searchParams;
    search_params.set("lan", lan_);
    search_params.set("page", 1);
    url.search = search_params.toString();
    var new_url = url.toString();
    window.location = url;
  }
  return false;
});