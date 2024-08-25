import math
import re
from .firebase import firebase_engine
from firebase_admin import firestore_async
from google.cloud.firestore_v1.base_query import FieldFilter

class BaseCRUD:
    def __init__(self, collection: str = None) -> None:
        self.database = firebase_engine
        if collection:
            self.collection = self.database.set_collection(collection)
            self.collection_name = collection
            
    async def set_collection(self, collection: str):
        self.collection = self.base.set_collection(collection)
        self.collection_name = collection
        
    async def count_documents(self, query: dict = None) -> int:
        if query is None:
            query_ref = self.collection
        else:
            query_ref = self.collection
            for key, value in query.items():
                query_ref = query_ref.where(key, '==', value)

        documents = query_ref.stream()
        return len([doc async for doc in documents])

    async def build_field_projection(self, fields_limit: list | str = None) -> list:
        """
        Constructs a list of field names to be used with Firestore's select() method.
    
        Args:
            fields_limit (list | str): A list or string of field names to include in the projection.
                                For example, ["name", "age", "address"], "name,age,address".
    
        Returns:
            list: A list of field names to include in the Firestore query results. If no fields are specified,
                  an empty list is returned.
        """
        if not fields_limit:
            return []
        if isinstance(fields_limit, str):
            fields_limit = fields_limit.split(",")
        
        fields = [field.strip() for field in fields_limit]
        return fields
    
    def convert_bools(self, value: dict | list | str) -> dict | list | str:
        """
        Converts string representations of booleans ("true" or "false") to actual boolean values (True, False) in a given data structure.

        Args:
            value (dict | list | str): The data structure containing the values to be converted.
                                       It can be a dictionary, list, or string.

        Returns:
            dict | list | str: The data structure with boolean string values converted to actual booleans.

        """
        bool_map = {"false": False, "true": True}
        if isinstance(value, dict):
            return {key: self.convert_bools(value=value) for key, value in value.items()}
        elif isinstance(value, list):
            return [self.convert_bools(value=item) for item in value]
        elif isinstance(value, str):
            return bool_map.get(value, value)
        return value

    def replace_special_chars(self, value: dict | str) -> dict | str:
        """
        Escapes special characters in strings within a given dictionary or string.
        
        
        This function finds special characters that have specific meanings in regular expressions 
        (e.g., *, +, ?, ^, $, {, }, (, ), |, [, ], \\) and escapes them by prefixing them with a backslash.
        This is useful when these characters need to be used in regular expression patterns or in other contexts 
        where they should be treated as literal characters.

        Args:
            value (dict | str): The input dictionary or string containing special characters.

        Returns:
            dict | str: The input dictionary with all string values having special characters escaped,
                        or a single string with special characters escaped using a backslash.
        """
        # Define the pattern for special characters
        pattern = r"([*+?^${}()|[\]\\])"
        # Replace the special characters with //
        if isinstance(value, dict):
            return {key: self.replace_special_chars(value=value) for key, value in value.items()}
        elif isinstance(value, str):
            return re.sub(pattern, r"\\\1", value)
        return value

    async def save(self, data: dict) -> str:
        """
        Inserts a single document into the Firestore collection.

        Args:
            data (dict): The document to be inserted into the collection.

        Returns:
            str: The ID of the inserted document as a string.
        """
        _, document_ref = await self.collection.add(data)
        return document_ref.id


    async def save_many(self, data: list) -> list | None:
        """
        Inserts multiple documents into the Firestore collection.

        Args:
            data (list): A list of documents to be inserted into the collection.

        Returns:
            list: A list of inserted document IDs as strings, or None if the insertion fails.
        """
        if not data:
            return None

        results = []
        for document in data:
            document_id = await self.save(data=document)
            results.append(document_id)

        return results if results else None


    async def save_unique(self, data: dict, unique_field: list | str) -> str | bool:
        """
        Saves a document into the Firestore collection if it does not already exist based on unique fields.

        Args:
            data (dict): The document to be inserted into the collection.
            unique_field (list | str): The field or list of fields that should be unique.
                                       If a document with the same values for these fields exists,
                                       the new document will not be inserted.

        Returns:
            str | bool: The ID of the inserted document as a string if insertion is successful,
                        False if a document with the same unique fields already exists.
        """
        # Check if unique_field is a list of fields that need to be unique
        if isinstance(unique_field, list):
            query_ref = self.collection  # Start with a query reference pointing to the root collection
            # This loop adds `where` conditions to the query for each field in unique_field
            for field in unique_field:
                # Each where call creates a new query based on the previous one
                query_ref = query_ref.where(field, '==', data[field])
        elif isinstance(unique_field, str):
            # If unique_field is a string, simply add a single where condition
            query_ref = self.collection.where(unique_field, '==', data[unique_field])
        else:
            raise ValueError("The type of unique_field must be list or str")

        # Check if any document exists with the given conditions
        documents = query_ref.stream()
        is_exist = any([True async for _ in documents])

        # If a document exists with the same unique_field values, do not save the new document and return False
        if is_exist:
            return False

        # If no duplicate document exists, save the new document and return its ID
        result = await self.save(data=data)
        return result

    async def update_by_id(self, _id: str, data: dict, query: dict = None) -> bool:
        """
        Updates a document in the Firestore collection based on its ID and an optional query.

        Args:
            _id (str): The ID of the document to be updated.
            data (dict): The data to update in the document.
            query (dict, optional): Additional query criteria for the update operation.

        Returns:
            bool: True if the document was successfully updated (i.e., at least one field was modified), 
                  False if no changes were made to the document or the document did not exist.
        """
        # Start with the document reference using the provided ID
        document_ref = self.collection.document(_id)

        # If an additional query is provided, verify that the document meets the query criteria
        if query:
            document_snapshot = await document_ref.get()
            if not document_snapshot.exists:
                return False  # Document does not exist

            # Check if the document satisfies the additional query criteria
            doc_data = document_snapshot.to_dict()
            for key, value in query.items():
                if doc_data.get(key) != value:
                    return False  # Document does not meet the query criteria

        # Perform the update operation
        try:
            result = await document_ref.update(data)
            return True  # Return True if update was successful
        except Exception as e:
            print(f"Update failed: {e}")
            return False  # Return False if update failed or no fields were modified

    async def delete_by_id(self, _id: str, query: dict = None) -> bool:
        """
        Deletes a document from the Firestore collection based on its ID and an optional query.

            Args:
                _id (str): The ID of the document to be deleted.
                query (dict, optional): Additional query criteria for the delete operation.

            Returns:
                bool: True if the document was successfully deleted, False otherwise.
            """
            # Start with the document reference using the provided ID
        document_ref = self.collection.document(_id)

        # If an additional query is provided, verify that the document meets the query criteria
        if query:
            document_snapshot = await document_ref.get()
            if not document_snapshot.exists:
                return False  # Document does not exist

            # Check if the document satisfies the additional query criteria
            doc_data = document_snapshot.to_dict()
            for key, value in query.items():
                if doc_data.get(key) != value:
                    return False  # Document does not meet the query criteria

        # Perform the delete operation
        try:
            await document_ref.delete()
            return True  # Return True if deletion was successful
        except Exception as e:
            print(f"Deletion failed: {e}")
            return False  # Return False if deletion failed

    async def get_by_id(self, _id: str, fields_limit: list = None, query: dict = None) -> dict | None:
        """
        Retrieves a document from the Firestore collection based on its ID, with optional field limitations and additional query.

        Args:
            _id (str): The ID of the document to be retrieved.
            fields_limit (list, optional): A list of field names to include in the result.
                                           If None, all fields are included.
            query (dict, optional): Additional query criteria to further refine the search.

        Returns:
            dict | None: The retrieved document, or None if no document is found.
        """
        # Start by referencing the document using its ID
        document_ref = self.collection.document(_id)

        # If fields_limit is provided, use select to limit the fields returned
        if fields_limit:
            fields_limit = await self.build_field_projection(fields_limit=fields_limit)
            document_ref = document_ref.select(*fields_limit)

        # Retrieve the document snapshot
        document_snapshot = await document_ref.get()

        # Check if the document exists
        if not document_snapshot.exists:
            return None

        # Convert the document to a dictionary
        result = document_snapshot.to_dict()

        # If additional query criteria are provided, verify the document meets them
        if query:
            for key, value in query.items():
                if result.get(key) != value:
                    return None  # Return None if the document doesn't match the query criteria
        result['_id'] = _id
        return result


    async def get_by_field(self, data: str, field_name: str, fields_limit: list = None, query: dict = None) -> dict | None:
        """
        Retrieves a document from the Firestore collection based on a specific field value, with optional field limitations and additional query.

        Args:
            data (str): The value to search for in the specified field.
            field_name (str): The name of the field to search in.
            fields_limit (list, optional): A list of field names to include in the result.
                                           If None, all fields are included.
            query (dict, optional): Additional query criteria to further refine the search.

        Returns:
            dict | None: The retrieved document, or None if no document is found.
        """
        # Build the initial query based on the specified field and its value
        query_ref = self.collection.where(filter=FieldFilter(field_name, "==", data))

        # If additional query criteria are provided, add them to the query
        if query:
            for key, value in query.items():
                query_ref = query_ref.where(filter=FieldFilter(key, "==", value))

        # If fields_limit is provided, use select to limit the fields returned
        if fields_limit:
            fields_limit = await self.build_field_projection(fields_limit=fields_limit)
            query_ref = query_ref.select(*fields_limit)

        # Execute the query and get the document
        documents = query_ref.stream()

        # Fetch the first document that matches the query
        document = None
        async for doc in documents:
            document = doc.to_dict()
            document['_id'] = doc.id
            break
        
        return document

    async def get_all(self, query: dict = None, search: str = None, search_in: str = None, page: int = None, limit: int = None, fields_limit: list = None, sort_by: str = None, order_by: str = None) -> dict:
        """
        Retrieves all documents from the Firestore collection based on various query, pagination, sorting, and field limitations.

        Args:
            query (dict, optional): The query criteria for querying the collection.
            search (str): A string to search for in the search_in fields.
            search_in (sre, optional): A fields to search in if a search query is provided.
            page (int, optional): The page number for pagination.
            limit (int, optional): The number of documents per page.
            fields_limit (list, optional): A list of field names to include in the results.
                                           If None, all fields are included.
            sort_by (str, optional): The field name to sort the results by.
            order_by (str, optional): The order to sort the results, either "asc" for ascending or "desc" for descending.

        Returns:
            dict: A dictionary containing the results, total number of items, total pages, and records per page.
        """
        common_params = {"search", "search_in", "page", "limit", "fields", "sort_by", "order_by"}
        query = {k: v for k, v in (query or {}).items() if k not in common_params}
        
        query_ref = self.collection

        # Handle additional query criteria
        if query:
            for key, value in query.items():
                query_ref = query_ref.where(key, '==', value)

        # Handle sorting    
        if sort_by:
            order_by_direction = firestore_async.Query.DESCENDING if order_by == "desc" else firestore_async.Query.ASCENDING
            query_ref = query_ref.order_by(sort_by, direction=order_by_direction)

        # Handle field limitations
        if fields_limit:
            query_ref = query_ref.select(*fields_limit)

        # Handle pagination
        if page and limit:
            offset = (page - 1) * limit
            query_ref = query_ref.offset(offset).limit(limit)
        elif limit:
            query_ref = query_ref.limit(limit)

        # Execute the query and gather results
        documents = query_ref.stream()
        results = []
        print(search_in)
        async for document in documents:
            doc_dict = document.to_dict()
            # Handle search functionality
            if search and search_in:
                if search not in doc_dict.get(search_in):
                    continue
            doc_dict['_id'] = document.id
            results.append(doc_dict)

        # Total records count (Firestore doesn't have a direct count operation; you may need to keep a separate count in another document or use a different approach)
        total_records = len(results)  # Simplified approach to get total records count for the current query; may need adjustment
        total_page = math.ceil(total_records / limit) if limit else 1

        return {
            "total_items": total_records,
            "total_page": total_page,
            "records_per_page": len(results),
            "results": results
        }

