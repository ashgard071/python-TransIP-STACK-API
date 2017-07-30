# TransIP STACK API
Unofficial wrapper for the TransIP STACK API, written in Python 3.

## Installation
PIP installation coming soon, for now just clone the repository

## Usage

```python
from io import BytesIO

from transip_stack import Stack, StackException


with Stack(username="foo", password="bar", hostname="stack.example.com") as stack:
    for file in stack.files:
        print(file.name)
        
    for file in stack.cd("/").ls("foo"):
        print(file.name)
        
    for file in stack.cd("/foo").files:
        if not file.is_shared:
            file.share()
            
        print(file.share_url)
        
    user = stack.user("admin")
    user.set_name("John Doe")
    
    user = stack.user_or_create_new(name="Someone Else", username="someone", password="foo", disk_quota=5 * 1000 * 1000)


with Stack(username="someone", password="foo", hostname="stack.example.com") as stack:
    stack.upload("foo.txt")
    stack.download("foo.txt", "example.txt")
    
    buff = BytesIO()
    stack.download_into("foo.txt", buffer=buff)
    print(buff.getvalue().decode())

```

Without context managers:

```python
from transip_stack import Stack


stack = Stack(username="foo", password="bar", hostname="stack.example.com")
stack.login()

stack.cd("/foo")

for file in stack.files:
    file.unshare()

stack.logout()  # Important
```

---

## API endpoints

### Logging in
* POST `/login`
  * Query
    * *None*
  * Body
    * username: str
    * password: str
  * Response
    * Success: HTTP 302
    * Failure: HTTP 200

### Logging out
* GET `/logout`
  * Query
    * *None*
  * Body
    * *None*
  * Response
    * Success: HTTP 302
    * Failure: *N/A*

### Listing files
* GET `/api/files`
  * Query
    * dir: str = "/"
    * type: str = "files"
    * public: bool = false
    * offset: int = 0
    * limit: int = 1
    * sortBy: str = "default"
    * order: str = "asc"
    * query: str = ""
  * Body
    * *None*

### Sharing a file
* POST `/api/files/update`
  * Headers
    * CSRF-Token
  * Query
    * *None*
  * Body (JSON)
    * Array of:
      * action: str = "share"
      * path: str = "<full path to file, see node.path>"
      * active: bool = true
        * true: File will be shared and get assigned a token
        * false: File will no longer be shared
      * allowWrites: bool = false
      * updatePassword: bool = true
        * *Set to true if you want to set a password*
      * sharePassword: str = "<your share password>"
        * *Required when setting a password*
      * updateExpireDate: bool = true
        * *Set to true if you want to set an expiry date
      * expireDate: date = "<your share expiry date>"
        * *Required when setting an expiry date*

### Deleting a file
* POST `/api/files/update`
 * Headers
   * CSRF-Token
  * Query
    * *None*
  * Body (JSON)
    * Array of:
      * action: str = "delete"
      * path: str = "<full path to file, see node.path>"
      * query: str = ""
        * *Not sure why this is added, possibly for mass file deletion*

### Getting file information
* GET `/api/pathinfo`
  * Query
    * path: str = "<full path to file>"
  * Body
    * *None*

### Marking a file as favorited
* POST `/api/files/update`
 * Headers
   * CSRF-Token
  * Query
    * *None*
  * Body (JSON)
    * Array of:
      * action: str = "favorite"
      * active: bool
        * True = Favorited
        * False = Unfavorited
      * path: str = "<full path to file, see node.path>"
      * query: str = ""
        * *Not sure why this is added, possibly for mass file deletion*

### List users
* GET `/api/users`
  * Body
    * *None*
  * Query
    * public: bool = false
    * offset: int = 0
    * limit: int = 50
    * query str = ""
    
### Delete a user
* POST `/api/users/update`
  * Body (JSON)
    * Array of:
      * action: str = "delete"
      * user: User 
        * *The entire user object you got from `GET /api/users`
  * Query
    * *None*
    
### Update a user's properties
* POST `/api/users/update`
  * Body (JSON)
    * Array of:
      * action: str = "update"
      * user: User
  * Query
    * *None*

## Headers
* CSRF-Token
  * Found in `/files` in a meta tag with the name `csrf-token`

## Types
* Node (Dict)
    * fileId: int
    * path: str
    * mimetype: str
    * etag: str
    * shareToken: str
    * expirationDate: str
    * hasSharePassword: bool
    * shareTime: int
    * canUpload: bool
    * fileSize: int
    * isFavorited: bool
    * mtime: int
    * isPreviewable: bool
    * width: int
    * height: int

* User (Dict)
    * username: str
    * displayName: str
    * quota: int
    * used: int
    * isAdmin: bool
    * isPremium: bool
    * language: str