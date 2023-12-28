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

  function alertFunction(btnId, btnTitle, official) {
    const appendAlert = (message, type) => {
        console.log("creating div");
        const wrapper = document.getElementById('alertsContainer');
        wrapper.innerHTML = ''
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible" id="${btnId}_alert" role="alert">`,
            `   <button type="button" class="btn-close" aria-label="Close" onclick="closeAlert('${btnId}_alert')"></button>`,
            `   <div>${message}</div>`,
            '</div>'
        ].join('');
    };

    const alertTrigger = document.getElementById(btnId);
    if (alertTrigger) {
        alertTrigger.addEventListener('click', () => {
            appendAlert(`${official}'s ${btnTitle} is not linked. Please check back later`, 'success');
        });
    }
}

function closeAlert(id) {
    const alert = document.getElementById(id);
    if (alert) {
        alert.remove();
        console.log('done');
    }
}