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

agent_type = $("#agent_type-selected-code").val();
$(`#agent_type-select option[value='${agent_type}']`).attr(
  "selected",
  "selected"
);

$("#agent_type-select").bind("change", function () {
  // bind change event to select
  var agent_type_ = $(this).val(); // get selected value

  if (agent_type_ != "") {
    // require a URL
    url = new URL(window.location);
    var search_params = url.searchParams;
    search_params.set("agent_type", agent_type_);
    search_params.set("page", 1);
    url.search = search_params.toString();
    var new_url = url.toString();
    window.location = url;
  }
  return false;
});