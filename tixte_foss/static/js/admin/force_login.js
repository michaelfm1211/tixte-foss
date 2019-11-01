if (sessionStorage.getItem("admin_key") == null || sessionStorage.getItem("admin_key") === "") {
    location = document.getElementById("url_for_admin");
}
document.getElementById("admin_key").value = sessionStorage.getItem("admin_key");