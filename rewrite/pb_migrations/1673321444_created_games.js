migrate((db) => {
  const collection = new Collection({
    "id": "vhw5l92xi87grl2",
    "created": "2023-01-10 03:30:44.746Z",
    "updated": "2023-01-10 03:30:44.746Z",
    "name": "games",
    "type": "base",
    "system": false,
    "schema": [
      {
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
      }
    ],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("vhw5l92xi87grl2");

  return dao.deleteCollection(collection);
})
