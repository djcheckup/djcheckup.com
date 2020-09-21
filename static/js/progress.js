// VanillaJS!!
function update_progress() {
  var current_status_div = document.querySelector("#current_status");
  var progress_div = document.querySelector("#progressbar");
  var completed_div = document.querySelector("#completed_status");
  fetch(status_url)
    .then(function (response) {
      // The API call was successful!
      if (response.ok) {
        return response.json();
      }
      // There was an error
      return Promise.reject(response);
    })
    .then(function (data) {
      // This is the JSON from our response
      current_status = data["current_status"];
      if (data["progress"] == null) {
        progress = "0";
      } else {
        progress = data["progress"];
      }

      current_status_div.textContent = status;
      progress_div.setAttribute("aria-valuenow", progress);
      progress_div.textContent = progress + "%";
      progress_div.style.width = progress + "%";

      // Checks if the script is finished
      if (data["status"] == "failed") {
        completed_div.innerHTML =
          "An error occurred during the scan and it could not be completed. <a href='/'>Please try again</a>.";
        progress_div.textContent = "100%";
        progress_div.style.width = "100%";
        progress_div.classList.add("bg-danger");
      } else if (data["status"] == "finished" && !data["check_id"]) {
        completed_div.innerHTML =
          "An error occurred during the scan and it could not be completed. <a href='/'>Please try again</a>.";
        progress_div.textContent = "100%";
        progress_div.style.width = "100%";
        progress_div.classList.add("bg-danger");
      } else if (data["status"] == "finished" && data["check_id"]) {
        console.log(
          "<a href='" +
            data["check_id"] +
            "' class='btn btn-primary btn-lg' role='button'>View your results here.</a>"
        );
        completed_div.innerHTML =
          "<a href='" +
          data["check_id"] +
          "' class='btn btn-primary btn-lg' role='button'>View your results here.</a>";
        progress_div.textContent = "100%";
        progress_div.style.width = "100%";
        progress_div.classList.add("bg-success");
      } else {
        setTimeout(function () {
          update_progress();
        }, 800);
      }
    })
    .catch(function (err) {
      // There was an error
      console.warn("Something went wrong.", err);
    });
}
update_progress();
