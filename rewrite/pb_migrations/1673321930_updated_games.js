migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("vhw5l92xi87grl2")

  collection.viewRule = ""

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "xpqi3ikw",
    "name": "state",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("vhw5l92xi87grl2")

  collection.viewRule = null

  // remove
  collection.schema.removeField("xpqi3ikw")

  return dao.saveCollection(collection)
})
