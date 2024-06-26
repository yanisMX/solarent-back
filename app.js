const createError = require("http-errors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const sequelize = require("./sequelize");
const cors = require("cors");
const indexRouter = require("./routes/index");
const citiesRouter = require("./routes/cities"); // Importez le routeur pour les villes
const departmentsRouter = require("./routes/departments");
const projectsRouter = require("./routes/projects");
const statesRouter = require("./routes/states");

const app = express();
app.use(cors({ origin: "http://localhost:3000" || "http://localhost:5174" }));
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "jade");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

app.use("/", indexRouter);
app.use("/cities", citiesRouter); // Utilisez le routeur pour les villes
app.use("/departments", departmentsRouter);
app.use("/projects", projectsRouter);
app.use("/states", statesRouter);

app.use(function (req, res, next) {
  next(createError(404));
});

app.use(function (err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};
  res.status(err.status || 500);
  res.render("error");
});

sequelize
  .sync()
  .then(() => {
    console.log("Database synchronized");
  })
  .catch((err) => {
    console.error("Unable to synchronize the database:", err);
  });

module.exports = app;

console.log("c'est moi qu'est ce que tu fais sur mon ordi ?");
