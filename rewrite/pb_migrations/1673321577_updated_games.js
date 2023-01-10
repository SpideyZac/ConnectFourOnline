migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("vhw5l92xi87grl2")

  // remove
  collection.schema.removeField("hlndc3pf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "gywyiznm",
    "name": "player1",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "maxSelect": 1,
      "collectionId": "_pb_users_auth_",
      "cascadeDelete": false
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "xkouy41b",
    "name": "player2",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "maxSelect": 1,
      "collectionId": "_pb_users_auth_",
      "cascadeDelete": false
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("vhw5l92xi87grl2")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "hlndc3pf",
    "name": "field",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // remove
  collection.schema.removeField("gywyiznm")

  // remove
  collection.schema.removeField("xkouy41b")

  return dao.saveCollection(collection)
})
