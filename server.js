const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Cinebooker Backend is running 🚀");
});

app.get("/movies", (req, res) => {
  res.json([
    { id: 1, name: "Avatar", price: 200 },
    { id: 2, name: "Inception", price: 180 }
  ]);
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});
