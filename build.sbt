name := "recipe-importer"

version := "0.0.1"

scalaVersion := "2.11.6"

resolvers ++= Seq(
  "anormcypher" at "http://repo.anormcypher.org/",
  "Typesafe Releases" at "http://repo.typesafe.com/typesafe/releases/"
)

libraryDependencies ++= Seq(
  "org.anormcypher" %% "anormcypher" % "0.6.0",
  "org.json4s" %% "json4s-jackson" % "3.2.11"
)

