


function populateFileSelectAndOptions() {
   var fileSelect = document.getElementById("fileSelect");
 

    files.forEach(function(file, index) {
        var option = document.createElement("option");
        option.text = file.name;
        fileSelect.appendChild(option);

        /*var li = document.createElement("li");
        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = "fileOption_" + index;
        checkbox.value = file.name;
        var label = document.createElement("label");
        label.htmlFor = "fileOption_" + index;
        label.textContent = file.name;
        li.appendChild(checkbox);
        li.appendChild(label);
        fileOptions.appendChild(li);*/
    });

/*var triggerTabList = [].slice.call(document.querySelectorAll('#myTab a'))
triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})*/
}

// Populate file select dropdown and file options list initially
populateFileSelectAndOptions();




