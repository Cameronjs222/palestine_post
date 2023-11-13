function filterFunction(list_container, input_label) {
    var input, filter, ul, li, a, i;
    input = document.getElementById(input_label);
    filter = input.value.toUpperCase();
    div = document.getElementById(list_container);
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }