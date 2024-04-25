// Simulated file data for demonstration purposes
var files = [
    { name: "fichier1.txt", permissions: "Lecture seule", owner: "John Doe", modified: false, creationDate: "2024-04-22", path: "/path/to/file1.txt" },
    { name: "fichier2.txt", permissions: "Lecture/Écriture", owner: "Jane Smith", modified: true, creationDate: "2024-04-20", path: "/path/to/file2.txt" },
    { name: "fichier3.txt", permissions: "Lecture seule", owner: "Alice Johnson", modified: false, creationDate: "2024-04-18", path: "/path/to/file3.txt" }
];


// Function to display file details
function displayFileDetails() {
    var fileSelect = document.getElementById("fileSelect");
    var selectedIndex = fileSelect.selectedIndex;
    if (selectedIndex !== -1) {
        var selectedFile = files[selectedIndex];
        var filePropertiesDiv = document.getElementById("fileProperties");
        filePropertiesDiv.innerHTML = "<p><span>Nom du fichier:</span> " + selectedFile.name + "</p>" +
                                    "<p><span>Autorisations:</span> " + selectedFile.permissions + "</p>" +
                                    "<p><span>Propriétaire:</span> " + selectedFile.owner + "</p>" +
                                    "<p><span>Modifié:</span> " + (selectedFile.modified ? "Oui" : "Non") + "</p>" +
                                    "<p><span>Date de création:</span> " + selectedFile.creationDate + "</p>" +
                                    "<p><span>Chemin du fichier:</span> " + selectedFile.path + "</p>";
    }
}

// Function to populate file select dropdown and file options list
function populateFileSelectAndOptions() {
   var fileSelect = document.getElementById("fileSelect");
    //var fileOptions = document.getElementById("fileOptions");

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



