## Explanation of storage

### Post

```bash
curl --location 'http://localhost:5000/upload' \
--header 'Content-Type: application/json' \
--data '{
  "id": "example_id",
  "thumbnails": [
    {"id": "thumb1", "url": "https://example.com/thumb1.jpg"},
    {"id": "thumb2", "url": "https://example.com/thumb2.jpg"}
  ],
  "description": "This is an example description.",
  "readme": "This is an example readme."
}'
```

### Get