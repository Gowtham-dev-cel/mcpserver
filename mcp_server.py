from fastmcp import FastMCP
import httpx

# 1. Create the server
mcp = FastMCP("myserver")


BASE_API_URL = "https://roascraft.onrender.com"


# 2. Add a tool
@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

@mcp.tool("get_all_user_lists")
def fetch_user_lists(api_key: str) -> dict:
    """
    Fetches all user lists from the local API using a provided API key.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        dict: JSON response containing user lists with details like id, name, totalContacts, fileUrl, etc.
    """
    url = "http://localhost:3000/api/lists"
    headers = {
        "x-api-key": api_key
    }

    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool("get_user_list_by_id")
def fetch_list_by_id(list_id: int, api_key: str) -> dict:
    """
    Fetches a specific user list by its list ID from the API.
    """
    url = f"{BASE_API_URL}/lists/{list_id}"
    headers = {"x-api-key": api_key}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


@mcp.tool("get_contacts_for_list")
def fetch_list_contacts(list_id: int, api_key: str) -> dict:
    """
    Fetches all contacts for a specific list by its list ID from the API.

    Args:
        list_id (int): The ID of the list to fetch contacts from.
        api_key (str): Your API key for authentication.

    Returns:
        dict: JSON response containing contacts of the requested list.
    """
    url = f"{BASE_API_URL}/lists/{list_id}/contacts"
    headers = {"x-api-key": api_key}
    
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool("get_sample_list_csv")
def get_sample_list_csv(api_key: str) -> dict:
    """
    Fetches a sample CSV structure showing the format for uploading a user list.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        dict: JSON response containing the sample CSV structure.
    """
    url = f"{BASE_API_URL}/lists/template/sample"
    headers = {"x-api-key": api_key}
    
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool("get_credits_for_list_enrichment")
def get_credits_for_list_enrichment(list_id: int, api_key: str) -> dict:
    """
    Fetches the number of credits required to enrich a specific user list.

    Args:
        list_id (int): The ID of the list for which enrichment credits are to be fetched.
        api_key (str): Your API key for authentication.

    Returns:
        dict: JSON response containing the credits required for enriching the requested list.
    """
    url = f"{BASE_API_URL}/lists/{list_id}/credits"
    headers = {"x-api-key": api_key}
    
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


@mcp.tool("get_available_filters_for_list")
def get_available_filters_for_list(list_id: int, api_key: str) -> dict:
    """
    Fetches the available filters for a specific user list that can be applied 
    while creating an audience.

    Args:
        list_id (int): The ID of the list for which available filters are to be fetched.
        api_key (str): Your API key for authentication.

    Returns:
        dict: JSON response containing the filters that can be applied to the list.
    """
    url = f"{BASE_API_URL}/lists/{list_id}/filters"
    headers = {"x-api-key": api_key}
    
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# 3. Add a static resource
@mcp.resource("resource://config")
def get_config() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}

# 4. Add a resource template for dynamic content
@mcp.resource("greetings://{name}")
def personalized_greeting(name: str) -> str:
    """Generates a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP server."

# 5. Make the server runnable
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)