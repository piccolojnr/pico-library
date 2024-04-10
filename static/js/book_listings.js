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
    window.location = new_url;
  }
});

