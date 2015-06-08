package com.munchcal.recipeimporter

import java.util.UUID

import com.munchcal.recipeimporter.Models._
import org.anormcypher._
import org.anormcypher.CypherParser._
import org.json4s._
import org.json4s.jackson.JsonMethods._

import scala.io.{BufferedSource, Source}
import scala.util.control.NonFatal

object Main extends App {

  implicit val connection = Neo4jREST("localhost", 7474, "/db/data/", "neo4j", "password")
  implicit val formats = DefaultFormats

  def newId() = UUID.randomUUID()
  def getResource(name: String): BufferedSource = Source.fromInputStream(getClass.getResourceAsStream(name))

  def createRecipe(obj: JValue) = {
    val name = (obj \ "name").extract[String]
    val authorName = (obj \ "author" \"name").extract[String]
    val sourceUrl = (obj \ "source" \ "url").extractOpt[String]
    val sourceName = (obj \ "source" \ "name").extractOpt[String]
    val imageUrl = (obj \ "image" \ "url").extractOpt[String]
    val description = (obj \ "description").extractOpt[String]

    try {
      val imageUrlString = imageUrl map (s => s""",image_url:"$s"""") getOrElse ""
      val sourceUrlString = sourceUrl map (s => s""",source_url:"$s"""") getOrElse ""
      val sourceNameString = sourceName map (s => s""",source_name:"$s"""") getOrElse ""
      val descriptionString = description map (s => s""",description:"$s"""") getOrElse ""

      val createString =
        s"""create(r:Recipe{
         |id:"${newId()}",
         |name:"$name",
         |author_name:"$authorName"
         |$imageUrlString
         |$sourceNameString
         |$sourceUrlString
         |$descriptionString
         |})
         |return r.id""".stripMargin

      val recipeId = Cypher(createString).as(str("r.id") *).head

      val ingredients = (obj \ "ingredients").extract[List[Ingredient]]
      ingredients.map(_.name).toSet flatMap mergeIngredient foreach {
        case (_, id) => createIngredientRelationship(recipeId, id)
      }

    } catch {
      case NonFatal(e) => e.printStackTrace()
    }
  }

  /*
   * This could be optimised by caching the results, and only merging the missing ones
   */
  def mergeIngredient(ingredientName: String): List[(String, String)] = {
    Cypher(
      s"""merge(f:Food{name:"$ingredientName"})
         |on create set f.id = "${newId()}"
         |return f.name, f.id;
       """.stripMargin).as((str("f.name") ~ str("f.id")).map(flatten) *)
  }

  def createIngredientRelationship(recipeId: String, ingredientId: String) = {
    //println(s"creating relationship between recipe[$recipeId] and food[$ingredientId]")
    Cypher(
      s"""MATCH (r:Recipe {id: "$recipeId"}),(f:Food {id: "$ingredientId"})
         |CREATE (r)-[:CONTAINS]->(f)
         """.stripMargin
    )()
  }

  parse(getResource("/evolutions/1.json").mkString) match {
    case JArray(arr) => arr foreach createRecipe
    case x =>
      println("oh noes")
      println(x)
  }

  Thread.sleep(1000)
}
