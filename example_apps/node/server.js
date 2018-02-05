let express = require("express");

const port = "80";
let app = express();

// Respond to root request
app.get("/", (req, res) => {
    res.send("Hello from Mbed Linux");
});

// Start server
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
