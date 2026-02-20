#!/bin/bash

# Clear all uploaded documents and database entries
# This allows you to re-upload and re-analyze documents

echo "🗑️  Clearing documents..."

# Clear uploaded files
rm -f backend/uploads/*.pdf backend/uploads/*.jpg backend/uploads/*.png 2>/dev/null
echo "✓ Cleared uploaded files"

# Clear MongoDB documents collection
backend/venv/bin/python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['homerights']
result = db.documents.delete_many({})
print(f'✓ Cleared {result.deleted_count} documents from database')
"

echo ""
echo "✅ Done! You can now upload documents again."
echo ""
