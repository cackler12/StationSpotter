
document.getElementById("location-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    const data = {
        lat: formData.get("lat"),
        long: formData.get("long"),
        timezone: formData.get("timezone")
    };

    handleRequest(data);
});

function handleRequest(data) {
    console.log("User input:", data);
}