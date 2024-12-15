document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("filterForm").addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent form submission (page reload)

      // Get filter values from input fields
      var categoryFilter = document.getElementById("category").value.toLowerCase();
      var organizationFilter = document.getElementById("organization").value.toLowerCase();
      var dateFilter = document.getElementById("date").value; // The date input will still be in YYYY-MM-DD format

      // Convert the date filter to MM/DD/YYYY format to match the table format
      var formattedDateFilter = formatDate(dateFilter);

      // Get all rows in the table
      var rows = document.querySelectorAll("#incidentTable tbody tr");

      // Loop through each row and hide/show based on filters
      rows.forEach(function(row) {
          var category = row.querySelector(".category").textContent.toLowerCase();
          var organization = row.querySelector(".organization").textContent.toLowerCase();
          var reportedDate = row.querySelector(".reported-date").textContent.trim();

          // Match each filter (if the filter is empty, it should always match)
          var matchesCategory = category.includes(categoryFilter);
          var matchesOrganization = organization.includes(organizationFilter);
          var matchesDate = dateFilter ? reportedDate === formattedDateFilter : true;

          // Show or hide the row based on matches
          if (matchesCategory && matchesOrganization && matchesDate) {
              row.style.display = "";
          } else {
              row.style.display = "none";
          }
      });
  });
});

// Function to convert the date filter (YYYY-MM-DD) to MM/DD/YYYY format
function formatDate(dateString) {
  if (!dateString) return '';
  var date = new Date(dateString);
  var month = (date.getMonth() + 1).toString().padStart(2, '0');  // Get the month and ensure it's two digits
  var day = date.getDate().toString().padStart(2, '0');  // Get the day and ensure it's two digits
  var year = date.getFullYear();

  return month + '/' + day + '/' + year;
}
